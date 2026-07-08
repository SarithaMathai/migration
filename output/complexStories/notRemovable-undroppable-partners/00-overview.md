# Complex Story — `notRemovablePartnerIds` & `unDroppablePartners`

> **Summary —** Work out which partners can’t be removed yet by asking each domain “do you still reference this partner?” and unioning the answers (a cross-domain read).
> **Spike:** `SPARK-SPIKE-04` · **Status:** 🔴 Open — decision pending
> **Use this folder:** the problem brief — the research so far for this case. Product Owner → §1 (the problem) · Engineer → §2 (what must be decided).

> **Home domains:** product (`plm-product`) + workspace (`plm-workspace`) · **Stub story:** `SPARK-PROD-E01` (partner drop/undrop) + `SPARK-WS-E01`

> **Migrates (source resolvers → this case):** product **FR `notRemovablePartnerIds`** (`SPARK-PROD-G11`) +
> **FR `unDroppablePartners`** (`SPARK-PROD-G07`) + helpers `getProductPartnersNotRemovable` /
> `getUnDroppablePartners`; workspace **FR `notRemovablePartnerIds`/`unDroppablePartners`** (`SPARK-WS-G05`).

## 1. The problem (grounded in the legacy code)

**What this read does:**
- Before an admin removes or drops a partner, the UI must grey out the ones still in use — a partner who still owns samples, participates in discussions, holds claims, or is named on attachments cannot simply be taken off.
- Answering "is this partner still in use anywhere?" means asking each of those domains and combining the answers.

Two fields on **Product** and **Workspace** answer "which partners can the user **not** remove / **not** drop
from this resource, because they're still referenced by a child?" Both are **cross-domain aggregations** today.

### `Product.notRemovablePartnerIds` — `getProductPartnersNotRemovable` (utils/removePartnerUtils.js:57)
Unions partner IDs gathered from **five** sources:
| Source | How (legacy) | Owning subgraph (target) |
|---|---|---|
| discussions | `discussionsV2` (elastic) → `partnerId + droppedPartnerIds + designPartnerId` | plm-discussion |
| attachments **+ components** | `attachmentsV3` + `components` → `detailIds` → ACL batch → grantees | plm-attachment |
| samples | `samples` → `partnerId` | plm-sample |
| watchlists | search product watchlists in workspace → ACL batch → grantees | plm-product (watchlist, co-located) |
| owning | `product.owningPartnerId` | plm-product |

### `Workspace.notRemovablePartnerIds` — `getWorkspacePartnersNotRemovable` (utils/removePartnerUtils.js:38)
Same shape, fewer sources: `discussionsV2` + `attachmentsWithMetaData` (→ ACL grantees) + `workspace.owningPartnerId`.

### `Product`/`Workspace.unDroppablePartners(isDesignPartner)` — `getUnDroppablePartners` (utils/commonLoaders.js:836)
1. `getAssociatedChildrensFromResouceId` → **Relationship Service** returns every child id (discussions,
   attachments, BOMs, packaging BOMs, samples, measurement sets, claims, + the product itself).
2. `getChunkedPermissions` → ACL permissions for all of them.
3. Keep resources whose ACL group is **not** `dps` (design-partner-security), return the **unique grantees**.

**Why it is hard (same root cause as TechPack):** Relationship-Service full traversal + chunked ACL across
every child, all in one monolith utility. No domain owns its slice.

## 2. What the spike must decide

- The contribution each domain exposes for the partner aggregation.
- Where the union is computed.
- **Proposal so far (light, to validate):** each domain contributes its own partner slice; the entity owner combines them.

---

*This folder holds the problem brief only — the research so far. The decision and the detailed design/task breakdown are produced by the spike and land here when it concludes.*
