# plm-microservice-security — Architecture & Flow Documentation

---

## 1. High-Level Purpose

This library is a **shared Spring Security plug-in** imported as a dependency by every Spark PLM microservice. It:

- Intercepts every HTTP request and validates the caller's identity via a JWT auth token.
- Builds a `UserProfile` and places it in the Spring `SecurityContext`.
- Optionally attaches resource-level ACL permissions from a separate capability JWT (`SPARK-CAPABILITY-TOKEN`).
- Provides annotations, role-based guards, and an argument resolver so controllers can receive `UserProfile` directly.

---

## 2. Package Structure

```
com.tgt.spark.security
├── acl/                    → IAccessControlService (outbound interface for ACL token generation)
├── annotations/            → Role-guard meta-annotations (@IsAdmin, @IsInternal, etc.)
├── aspects/                → SystemRoleAspect (AOP for temporary system role elevation)
├── configuration/          → SecurityConfig, MethodSecurityConfig, WebConfig, SystemRole, SparkAuthenticationEntryPoint
├── constants/              → CommonConstant (header names, role strings)
├── exceptions/             → BadRequestException, UnauthorizedException, InvalidCapabilityException, TokenGenerationException
├── expressions/            → ResourcePermissionEvaluator, IResourcePermission, IAllResourcePermission
├── filter/                 → XssFilter, RequestWrapper
├── jwtsecurity/
│   ├── authtokens/         → JWTAuthenticationToken
│   ├── filters/            → JWTAuthFilter (core request interceptor)
│   ├── Action.java
│   ├── JWTAuthenticationManager.java
│   ├── JWTSecurityConfiguration.java
│   ├── SecurityAppConfig.java
│   ├── SparkSecurityFilterContributor.java  (extension point)
│   └── SparkSecurityService.java
├── model/                  → UserProfile, UserResourcesPermissions, ResourcePermission, JWTUtil, XssSanitizer, etc.
├── optionssecurity/        → OptionsSecurityConfiguration (CORS preflight bypass)
├── reactive/               → Reactive/WebFlux support
└── rest/                   → UserProfileHandlerMethodArgumentResolver
```

---

## 3. Spring Security Filter Chain — Boot-time Setup

Two `SecurityFilterChain` beans are registered in priority order:

| Order | Config Class | Purpose |
|-------|---|---|
| `@Order(1)` | `OptionsSecurityConfiguration` | Handles **HTTP OPTIONS** (CORS preflight) — permits all, bypasses JWT auth |
| `@Order(2)` | `JWTSecurityConfiguration` | Handles **every other request** — enforces JWT auth |

Activation of `JWTSecurityConfiguration` is conditional:

```properties
spark.jwt.security.enabled=true   # default: true
```

### Paths Excluded from Security (WebSecurityCustomizer)

```
/
/error
/health
/actuator/health
/actuator/prometheus
/actuator/hystrix/**
/info
/graphiql/**
/swagger-ui/**
/v2/api-docs/**
/v3/api-docs/**
/webjars/**
```

---

## 4. `JWTSecurityConfiguration` — The Core Security Config

**File:** `jwtsecurity/JWTSecurityConfiguration.java`

```
JWTSecurityConfiguration
  ├── registers JWTAuthFilter          (after LogoutFilter)
  ├── registers SparkSecurityFilterContributor beans (after AnonymousAuthenticationFilter)
  ├── session = STATELESS
  ├── all requests must be authenticated
  └── custom entry point: SparkAuthenticationEntryPoint
```

`JWTAuthenticationManager` is a pass-through `AuthenticationProvider` — the real authentication logic lives entirely inside `JWTAuthFilter`.

Key constructor parameters (from application properties):

| Property | Default | Purpose |
|---|---|---|
| `spark.security.id2auth.enabled` | `false` | Enable internal id2auth (x-tgt-*) header path |
| `spark.security.id2auth.group` | `OAUTH-EXAMPLE-GROUP-NAME` | Required AD group for id2auth |
| `spark.security.sparkMember.group` | `APP-OAUTH2-PDEX-NPE` | Secondary allowed AD group |

---

## 5. `JWTAuthFilter` — The Request Interceptor

**File:** `jwtsecurity/filters/JWTAuthFilter.java`
Extends `SecurityContextHolderAwareRequestFilter`.

### Request Processing Flow

```
Incoming Request
     │
     ▼
isSecuredUrl?  ──No──► chain.doFilter (skip — reduces log noise for health/swagger/etc.)
     │ Yes
     ▼
extractToken(request)
  Priority order:
  1. X-AUTH-TOKEN header
  2. Authorization: Bearer <token>  (Bearer prefix stripped)
  3. Cookie: X-AUTH-TOKEN
  4. Cookie: Authorization
  └── throws UnauthorizedException if none found
     │
     ▼
Is X-AUTH-TOKEN present? (header or cookie)
  ├── YES  →  External / Business Partner path
  │               │
  │               ├── Check for SPARK-CAPABILITY-TOKEN header
  │               │     └── if present:
  │               │           sparkSecurityService.getACLPermissions(aclToken)
  │               │             → deserialize → UserResourcesPermissions
  │               │           VALIDATE: atHash == authToken  ← anti man-in-the-middle
  │               │           throw InvalidCapabilityException if mismatch
  │               │
  │               └── sparkSecurityService.loginForCurrentThread(authToken, userResourcesPermissions)
  │                     → JWTUtil.getUserProfile(token) → UserProfile
  │                     → UserProfile.setUserResourcesPermissions(aclPerms)
  │                     → JWTAuthenticationToken → SecurityContextHolder
  │
  └── NO   →  Internal / id2auth path
                  │
                  ├── id2auth enabled? (spark.security.id2auth.enabled)
                  │     NO → throw UnauthorizedException
                  │
                  ├── validateGroups(x-tgt-memberof)
                  │     parse CN=... LDAP string → list of group names
                  │     at least one must match memberOf or sparkMemberOf
                  │     throw UnauthorizedException if no match
                  │
                  ├── buildUserProfileFromXTgtHeaders(request)
                  │     x-tgt-lanid   → userId, userProfileId, lanId
                  │     x-tgt-firstname → firstName
                  │     x-tgt-lastname  → lastName
                  │     x-tgt-mail      → email
                  │     x-tgt-memberof  → adGroups (parsed)
                  │     nuid = true, internal = false
                  │
                  └── sparkSecurityService.loginForCurrentThread(userProfile)
                        → AD groups mapped to GrantedAuthority via spark.ldap.groups config
                        → JWTAuthenticationToken → SecurityContextHolder
     │
     ▼
request.setAttribute("userProfile", userProfile)   ← for GraphQL context access
MDC.put("userId", userProfile.getUserProfileIdString())
MDC.put("customfield2", userProfile.getUserProfileIdString())
     │
     ▼
chain.doFilter(req, res)
     │
     ▼
[finally]  MDC.remove("userId"), MDC.remove("customfield2")
```

---

## 6. `SparkSecurityService` — SecurityContext Population

**File:** `jwtsecurity/SparkSecurityService.java`
`@Service`, `@ConfigurationProperties("spark.ldap")`

### Key Methods

| Method | Description |
|--------|---|
| `loginForCurrentThread(token, userResourcesPermissions)` | Parses auth JWT → `UserProfile`, attaches ACL permissions, creates `JWTAuthenticationToken`, sets `SecurityContextHolder` |
| `loginForCurrentThread(UserProfile)` | id2auth path — re-generates token from profile, maps AD groups → `GrantedAuthority` |
| `updateCurrentUserPermissions(capabilityToken)` | Post-auth update: decodes a new capability token and refreshes the current thread's security context |
| `getACLPermissions(token)` | Decodes a `SPARK-CAPABILITY-TOKEN` → `UserResourcesPermissions` |
| `doAsUser(profile, action)` | Utility: temporarily log in as a given profile, run an `Action`, then log out |
| `logoutForCurrentThread()` | Clears `SecurityContextHolder` |
| `getCurrentUser()` | Returns `UserProfile` from current `SecurityContextHolder` (private) |

### Authority Generation

From `UserProfile` fields, `GrantedAuthority` roles are assigned:

| Condition | Authority Granted |
|---|---|
| `isInternal() == true` | `Internal` |
| `isInternal() == false` | `External` |
| `isSystem()` | `System` |
| `isAdmin()` | `ROLE_Admin` |
| `isMerchandiseVendor()` | `ROLE_MerchVendor` |
| `isFabricSupplier()` | `ROLE_FabricSupplier` |
| `isDesignPartner()` | `ROLE_DesignPartner` |
| `isTrimSupplier()` | `ROLE_TrimSupplier` |

For id2auth users, AD groups from `x-tgt-memberof` are additionally mapped to roles via `spark.ldap.groups` configuration:

```yaml
spark:
  ldap:
    groups:
      - adGroup: APP-MY-AD-GROUP
        roleName: Admin
```

---

## 7. `JWTUtil` — JWT Encoding / Decoding

**File:** `model/JWTUtil.java`
`@Component` — handles all JWT cryptographic operations using `io.jsonwebtoken`.

### Two Token Types

| Token Type | Header | TTL | Subject (`sub`) Payload |
|---|---|---|---|
| Auth token | `X-AUTH-TOKEN` / `Authorization` | `spring.ttl_millis` | `UserProfile` as JSON |
| Capability token | `SPARK-CAPABILITY-TOKEN` | 60 seconds (fixed) | `UserResourcesPermissions` as JSON |

### Signing Keys

Two signing keys support a rolling migration:

| Key | Selection | Raw secret |
|---|---|---|
| **Deprecated key** | No `kid` header in JWT | `id:secret` → Base64-decoded → HMAC-SHA256 |
| **Current key** (v2) | `kid=v2` header | `id:secret` → raw UTF-8 bytes → HMAC-SHA256 |

Enable new key signing with:
```properties
spring.jwt.sign_with_new_key=true
```

The `JwtParser` uses a `Locator<Key>` to auto-select the correct key at parse time based on the `kid` header — so both old and new tokens are accepted simultaneously during migration.

### Key Methods

| Method | Description |
|---|---|
| `getUserProfile(token)` | Parse auth JWT → `UserProfile` |
| `getACLPermissions(token)` | Parse capability JWT → `UserResourcesPermissions` |
| `getToken(UserProfile)` | Generate new auth JWT from `UserProfile` |
| `createACLJWT(UserResourcesPermissions)` | Generate new capability JWT |

---

## 8. `JWTAuthenticationToken` — The Authentication Object

**File:** `jwtsecurity/authtokens/JWTAuthenticationToken.java`
Extends `AbstractAuthenticationToken`.

| Field | Exposed as | Contents |
|---|---|---|
| `userProfile` | `getPrincipal()` | Full `UserProfile` object |
| `token` | `getCredentials()` | Raw JWT string |
| `authorities` | `getAuthorities()` | Computed `GrantedAuthority` list |
| `userProfile.userId` | `getName()` | User identifier string |

---

## 9. `UserProfile` — The Principal Model

**File:** `model/UserProfile.java`

Central domain object. Serialized as JSON into JWT `sub` claim and placed in `SecurityContext` as the principal.

### Core Fields

| Field | Type | Description |
|---|---|---|
| `userId` | `String` | Primary user identifier |
| `lanId` | `String` | Target LAN ID (also JWT `jti`) |
| `userProfileId` | `String` | Profile ID used for MDC logging |
| `email` | `String` | User email |
| `internal` | `boolean` | True if Target associate |
| `nuid` | `boolean` | True if NUID (non-LAN-ID) user |
| `roles` | `List<String>` | Explicit role strings (Admin, System) |
| `adGroups` | `List<String>` | AD groups (id2auth users) |
| `approvedVMMRoles` | `List<Integer>` | Business partner role codes (VMM system) |
| `currentVMMRole` | `Integer` | Active role code when user has multiple |
| `accreditations` | `List<Accreditation>` | Training/certification completions |
| `userResourcesPermissions` | `UserResourcesPermissions` | ACL capability permissions (not in JWT) |

### Business Partner Roles (`BusinessPartnerRole` enum)

| Role | `isMerchandiseVendor()` | `isFabricSupplier()` | `isDesignPartner()` | `isTrimSupplier()` |
|---|---|---|---|---|
| Logic | `approvedVMMRoles` contains MERCHANDISE_VENDOR code AND (`currentVMMRole == null` OR matches) | Same pattern | Same pattern | Same pattern |

### Static Utilities

```java
UserProfile.getCurrentUserProfile()  // fetch from SecurityContextHolder anywhere in code
UserProfile.getSystemProfile()       // create a synthetic system user profile
UserProfile.getSystemProfile(id)     // system profile with a specific userProfileId
```

---

## 10. `UserProfileHandlerMethodArgumentResolver`

**File:** `rest/UserProfileHandlerMethodArgumentResolver.java`
**Registration:** `WebConfig.addArgumentResolvers()`

Allows any Spring MVC controller to receive `UserProfile` as a method parameter automatically — no manual SecurityContextHolder access needed:

```java
@GetMapping("/my-endpoint")
public ResponseEntity<?> myEndpoint(UserProfile userProfile) {
    // userProfile is the authenticated principal, injected automatically
}
```

### How It Works

1. `supportsParameter()` — returns `true` when parameter type is exactly `UserProfile.class`.
2. `resolveArgument()` — reads `SecurityContextHolder`, verifies `Authentication` is a `JWTAuthenticationToken`, returns `authentication.getPrincipal()` cast to `UserProfile`.
3. Returns `null` if not authenticated or wrong token type (request will be rejected by Spring Security before it reaches the controller anyway).

---

## 11. `OptionsSecurityConfiguration`

**File:** `optionssecurity/OptionsSecurityConfiguration.java`

`@Order(1)` — fires **before** JWT security for **HTTP OPTIONS requests only**.

- `BasicAuthenticationRequest` matcher: `request.getMethod().equalsIgnoreCase("OPTIONS")`
- Disables CSRF, permits all `OPTIONS /**` without authentication.
- Ensures CORS preflight requests are never rejected by the JWT auth filter.

---

## 12. XSS Protection — `XssFilter` & `RequestWrapper`

**File:** `filter/XssFilter.java`, `filter/RequestWrapper.java`
**Registration:** `WebConfig.xssFilter()` — conditional bean:

```properties
spark.xss.filter.enabled=true   # default: true
```

### XssFilter Flow

```
Incoming Request
     │
     ├── Content-Type: multipart/form-data?
     │     YES → checkHeaders only (URL + query params)
     │     NO  → wrap request in RequestWrapper (buffers body)
     │            → checkHeaders (URL + query params)
     │            → checkBody (request body)
     │
     └── XssSanitizer.checkXss(value) returns true?
           YES → throw BadRequestException("Invalid request")
           NO  → chain.doFilter(wrappedRequest, response)
```

### `RequestWrapper`

Subclass of `HttpServletRequestWrapper` that reads the entire request body into a `String` at construction time, then re-serves it from a `ByteArrayInputStream` on subsequent `getInputStream()` / `getReader()` calls. This is required because the Servlet `InputStream` is one-shot — once read, it cannot be replayed.

---

## 13. ACL / Resource Permission System

### `UserResourcesPermissions`

```java
class UserResourcesPermissions {
    List<ResourcePermission> resourcePermissions;  // per-resource permissions
    String userId;                                  // owner of these permissions
    String atHash;                                  // hash of auth token (anti-MITM binding)
}
```

### `ResourcePermission`

```java
class ResourcePermission {
    String resourceId;           // the resource this applies to
    Set<Permission> permissions; // what the user can do
}
```

### Permission Hierarchy (numeric, higher subsumes lower)

```
READ(10) < ASSOCIATE(20) < READ_WRITE(30) < READ_WRITE_DELETE(40) < ADMIN(50)
```

`hasAccess(permission)` passes if any granted permission has `numVal >= requested.numVal`.

### `ResourcePermissionEvaluator`

**File:** `expressions/ResourcePermissionEvaluator.java`
Implements Spring's `PermissionEvaluator`. Plugged into `MethodSecurityConfig` via `DefaultMethodSecurityExpressionHandler`.

Used in method security expressions:

```java
@PreAuthorize("hasPermission(#styleId, 'READ_WRITE')")
public Style updateStyle(String styleId, ...) { }

@PreAuthorize("hasPermission(#resourceIds, 'READ')")
public List<Item> getItems(List<String> resourceIds) { }
```

Supports:
- Single resource ID (`String`)
- List or array of IDs (passes if **any** match)
- `IResourcePermission` — custom object-based matching (implement `isPermissionEqual(resourceId)`)
- `IAllResourcePermission` — custom cross-resource validation (implement `isAllPermissionsValid(userResourcesPermissions, permission)`)

### `IAccessControlService`

**File:** `acl/IAccessControlService.java`

```java
public interface IAccessControlService {
    String getUserAccessToken(List<String> resourceIds);
}
```

**This is an outbound integration interface.** The library defines it; downstream microservices provide an implementation (typically an ACL client library bean) that calls a separate ACL service. The returned string is a signed JWT (`SPARK-CAPABILITY-TOKEN`) containing `UserResourcesPermissions`.

---

## 14. Does the Library Auto-Call ACL and Add the Capability Token?

**Short answer: No — the capability token must be provided by the client on the inbound request.**

The library **consumes** a capability token if already present as `SPARK-CAPABILITY-TOKEN` on the inbound request. It does **not** proactively call an ACL service during filter processing.

### The Designed Flow

```
Client / API Gateway
     │
     ├── Obtain auth token  (X-AUTH-TOKEN)
     ├── Call ACL service via IAccessControlService.getUserAccessToken(resourceIds)
     │     └── returns SPARK-CAPABILITY-TOKEN (JWT, 60s TTL, atHash = authToken)
     │
     └── Send HTTP request with BOTH headers:
           X-AUTH-TOKEN: <auth-jwt>
           SPARK-CAPABILITY-TOKEN: <capability-jwt>
     │
     ▼
Microservice JWTAuthFilter
     ├── Validate X-AUTH-TOKEN → build UserProfile
     ├── Validate SPARK-CAPABILITY-TOKEN
     │     ├── Decode → UserResourcesPermissions
     │     └── Verify: atHash == X-AUTH-TOKEN  (ties capability to this user's token)
     └── Attach UserResourcesPermissions to UserProfile in SecurityContext
     │
     ▼
Controller @PreAuthorize("hasPermission(#id, 'READ_WRITE')")
     └── ResourcePermissionEvaluator checks UserProfile.userResourcesPermissions
```

### Mid-Request ACL Update

`SparkSecurityService.updateCurrentUserPermissions(capabilityToken)` can be called from within the application (e.g., after fetching a new capability token during request processing) to refresh the current thread's security context without re-authenticating.

---

## 15. Pluggable Filters — `SparkSecurityFilterContributor`

**File:** `jwtsecurity/SparkSecurityFilterContributor.java`

```java
public interface SparkSecurityFilterContributor extends Filter { }
```

Any Spring bean implementing this interface is **automatically discovered and added to the JWT security filter chain after `AnonymousAuthenticationFilter`**. This is the primary extension point for microservices to inject additional per-request security logic (e.g., audit logging, additional header validation) without modifying the library.

---

## 16. `SystemRoleAspect` — Temporary Role Elevation

**File:** `aspects/SystemRoleAspect.java`
`@Aspect`, `@Component`

AOP around-advice triggered by `@SystemRole` annotation. Temporarily adds the `"System"` role to any `UserProfile` argument before the method executes, then removes it in `finally`.

```java
@SystemRole
public void someInternalOperation(UserProfile user) {
    // user.getRoles() contains "System" only during this method
}
```

---

## 17. Annotation-Based Role Guards

Meta-annotations in `annotations/` package, each wrapping `@PreAuthorize`:

| Annotation | Expression |
|---|---|
| `@IsInternal` | `hasAuthority('Internal')` |
| `@IsExternal` | `hasAuthority('External')` |
| `@IsAdmin` | `hasRole('Admin')` |
| `@IsDesignPartner` | `hasRole('DesignPartner')` |
| `@IsMerchVendor` | `hasRole('MerchVendor')` |
| `@IsFabricSupplier` | `hasRole('FabricSupplier')` |
| `@IsTrimSupplier` | `hasRole('TrimSupplier')` |
| `@IsNonNuid` | custom non-NUID check |
| `@IsInternalOrDesignPartner` | `hasAuthority('Internal') or hasRole('DesignPartner')` |
| `@IsNotFabricSupplier` | negated fabric supplier check |

---

## 18. Configuration Reference

### Required Properties

```yaml
spring:
  client_id: <your-app-id>
  client_secret: <your-app-secret>
  ttl_millis: 3600000    # auth token TTL in milliseconds
```

### Optional Properties

```yaml
spring:
  jwt:
    sign_with_new_key: false   # set true to use HMAC-SHA256 v2 signing key

spark:
  jwt:
    security:
      enabled: true            # disable to turn off JWT security entirely

  security:
    id2auth:
      enabled: false           # enable internal x-tgt-* header auth path
      group: OAUTH-EXAMPLE-GROUP-NAME
    sparkMember:
      group: APP-OAUTH2-PDEX-NPE

  xss:
    filter:
      enabled: true            # disable to turn off XSS scanning

  ldap:
    groups:                    # map AD groups to Spring Security roles (id2auth)
      - adGroup: APP-MY-GROUP
        roleName: Admin
```

---

## 19. Complete End-to-End Request Flow

```
Client HTTP Request
     │
     ├── HTTP OPTIONS ──► OptionsSecurityConfiguration (Order 1)
     │                         └── permit all → respond → done
     │
     └── All other methods:
           │
           ▼
         XssFilter  (GenericFilterBean, outside Spring Security chain)
           ├── multipart? → check URL + params only
           └── other     → wrap body in RequestWrapper → check URL + params + body
                           throw BadRequestException on XSS detection
           │
           ▼
         JWTSecurityConfiguration (Order 2) → JWTAuthFilter
           │
           ├── skip if non-secured URL (/health, /actuator, /swagger, etc.)
           │
           ├── extractToken() from X-AUTH-TOKEN header → Authorization header → cookies
           │
           ├── X-AUTH-TOKEN present?
           │   YES (external user):
           │     SPARK-CAPABILITY-TOKEN present?
           │       YES: decode → UserResourcesPermissions
           │            verify atHash == authToken  (MITM protection)
           │     SparkSecurityService.loginForCurrentThread(authToken, aclPerms)
           │       → JWTUtil.getUserProfile(token)  → UserProfile
           │       → UserProfile.setUserResourcesPermissions(aclPerms)
           │       → generateAuthorities(userProfile) → GrantedAuthority list
           │       → JWTAuthenticationToken → SecurityContextHolder
           │
           │   NO (internal id2auth user):
           │     id2auth enabled? NO → throw UnauthorizedException
           │     validateGroups(x-tgt-memberof) → must match configured AD group
           │     buildUserProfileFromXTgtHeaders() → UserProfile from x-tgt-* headers
           │     SparkSecurityService.loginForCurrentThread(userProfile)
           │       → AD groups mapped to GrantedAuthority via spark.ldap.groups
           │       → JWTAuthenticationToken → SecurityContextHolder
           │
           ├── request.setAttribute("userProfile", userProfile)   [for GraphQL context]
           ├── MDC.put("userId", userProfileId)
           └── chain.doFilter()
                 │
                 ▼
               SparkSecurityFilterContributor beans  (after AnonymousAuthenticationFilter)
               [custom filters contributed by the consuming microservice]
                 │
                 ▼
               Spring MVC DispatcherServlet
                 │
                 ▼
               UserProfileHandlerMethodArgumentResolver
                 └── injects UserProfile into controller method parameters
                       │
                       ▼
                     Controller method
                       │
                       ├── @IsInternal / @IsAdmin / etc. → hasAuthority / hasRole check
                       └── @PreAuthorize("hasPermission(#id, 'READ_WRITE')")
                               └── ResourcePermissionEvaluator
                                     └── checks UserProfile.userResourcesPermissions
                                           └── ResourcePermission.hasAccess(permission)
```

---

## 20. Security Token Header Reference

| Header | Direction | Contents | Purpose |
|---|---|---|---|
| `X-AUTH-TOKEN` | Inbound | Signed JWT (`UserProfile` in `sub`) | Primary user authentication |
| `Authorization` | Inbound | `Bearer <jwt>` (same JWT) | Alternative to X-AUTH-TOKEN |
| `SPARK-CAPABILITY-TOKEN` | Inbound | Signed JWT (`UserResourcesPermissions` in `sub`, 60s TTL) | Resource-level ACL authorization |
| `x-tgt-lanid` | Inbound (id2auth) | LAN ID string | Internal user identity |
| `x-tgt-memberof` | Inbound (id2auth) | LDAP DN string with CN= groups | AD group membership |
| `x-tgt-firstname` | Inbound (id2auth) | First name | Profile population |
| `x-tgt-lastname` | Inbound (id2auth) | Last name | Profile population |
| `x-tgt-mail` | Inbound (id2auth) | Email address | Profile population |

