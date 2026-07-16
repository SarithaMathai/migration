# GraphQL Query & Mutation Inventory

> Auto-generated inventory of all GraphQL queries, mutations, fragments, and subscriptions across the pdex-ui-react codebase.
> Organized by domain. Each entry lists the defining source file and all files that reference it.

---

## Summary

| Stat | Count |
|------|-------|
| Total GQL definitions | 951 |
| Queries | 514 |
| Mutations | 217 |
| Fragments | 220 |
| Subscriptions | 0 |
| Definitions with at least 1 usage | 784 |
| Domains covered | 35 |
| Source files scanned | 111 |

---

## Table of Contents

- [Claims](#claims)
- [Core — Activity Log](#core--activity-log)
- [Core — Base](#core--base)
- [Core — Discussions](#core--discussions)
- [Core — Favorites](#core--favorites)
- [Core — File Management](#core--file-management)
- [Core — Tags](#core--tags)
- [Product — Common](#product--common)
- [Product — Details](#product--details)
- [Product — Packaging](#product--packaging)
- [Product — Queries](#product--queries)
- [Samples](#samples)
- [App Base](#app-base)
- [Artwork](#artwork)
- [Color](#color)
- [Combination](#combination)
- [Common Components](#common-components)
- [Fabric](#fabric)
- [Insights](#insights)
- [Legacy (Spark)](#legacy-spark)
- [Materials](#materials)
- [Materials — Shared GQL](#materials--shared-gql)
- [Materials Hub](#materials-hub)
- [Packaging — Base](#packaging--base)
- [Packaging — Library](#packaging--library)
- [Palette](#palette)
- [Resources](#resources)
- [Rules](#rules)
- [Static / Temp](#static--temp)
- [Trim — UI](#trim--ui)
- [Trim — GQL](#trim--gql)
- [UI Admin](#ui-admin)
- [Wash](#wash)
- [Watchlist](#watchlist)
- [Workspaces](#workspaces)

---

## Claims

**13 definitions** — 6 queries, 5 mutations, 2 fragments

### `src/libs/claims/src/graphql/ClaimQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `CLAIM_DETAILS_FRAGMENT` | `src/libs/claims/index.ts`, `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` |
| 🧩 Fragment | `CLAIM_WORKSPACE_PRODUCT_FRAGMENT` | `src/libs/claims/index.ts` |
| ✏️ Mutation | `ADD_CLAIMS` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimNewTemplate.tsx`, `src/libs/spark-fabric/src/utils/fabricClaimsUtils.ts`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateClaimClone.tsx` |
| ✏️ Mutation | `BULK_UPDATE_CLAIM` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimBulkUpdate.tsx` |
| ✏️ Mutation | `LOCK_CLAIM` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimViewTemplate.tsx` |
| ✏️ Mutation | `UNLOCK_CLAIM` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimViewTemplate.tsx` |
| ✏️ Mutation | `UPDATE_CLAIM` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimViewTemplate.tsx`, `src/libs/spark-fabric/src/utils/fabricClaimsUtils.ts`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateClaimEdit.tsx` |
| 🔍 Query | `GET_CLAIMS_AND_CHANNELS` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimNewTemplate.tsx`, `src/libs/product/src/components/ImportProductDetailsSection.tsx` |
| 🔍 Query | `GET_CLAIM_VERSION` | `src/libs/claims/index.ts`, `src/libs/claims/src/customHooks/useClaimQuery.ts`, `src/libs/claims/src/routes/ClaimViewRoute.test.tsx` |
| 🔍 Query | `GET_COMMUNICATION_CHANNELLS` | `src/libs/claims/index.ts` |
| 🔍 Query | `GET_EXTERNAL_CLAIMS` | `src/libs/claims/index.ts`, `src/libs/claims/src/components/ClaimFormSection.tsx`, `src/libs/spark-fabric/src/components/ClaimFormSection.tsx` |
| 🔍 Query | `GET_PRODUCTS_WITH_IDS` | `src/libs/claims/index.ts`, `src/libs/claims/src/containers/ClaimBulkUpdate.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_WITH_IDS` | 11 files |

---

## Core — Activity Log

**2 definitions** — 2 queries

### `src/libs/core-activity-log/src/graphql/activityLogsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_ACTIVITY_FILTERS_COUNT` | `src/libs/core-activity-log/src/components/CoreActivityLogComponentWithFilters.tsx` |
| 🔍 Query | `GET_ACTIVITY_LOG` | `src/libs/core-activity-log/src/components/CoreActivityLogComponent.tsx` |

---

## Core — Base

**5 definitions** — 4 queries, 1 fragments

### `src/libs/core-base/src/graphql/coreBaseQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `ATTACHMENT_FRAGMENT` | `src/libs/samples/index.ts`, `src/libs/samples/src/components/workspace/BulkEvaluate/CombinationSamplesBulkEvaluate.tsx` |
| 🔍 Query | `GET_ATTACHMENTS_FROM_RELATED_RESOURCE` | `src/libs/core-base/index.ts` |
| 🔍 Query | `GET_TAGS_BY_TYPE` | 12 files |
| 🔍 Query | `GET_USER_SETTINGS` | 15 files |
| 🔍 Query | `SEARCH_ATTACHMENTS` | 17 files |

---

## Core — Discussions

**56 definitions** — 33 queries, 14 mutations, 9 fragments

### `src/libs/core-discussions/src/graphql/DiscussionFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `COMPONENT_DISCUSSION_PARTICIPANTS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `DISCUSSION_ATTACHMENT_DETAILS_FRAGMENT` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |
| 🧩 Fragment | `DISCUSSION_DETAILS_FRAGMENT_V3` | `src/libs/core-discussions/src/graphql/DiscussionMutations.ts`, `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |
| 🧩 Fragment | `DISCUSSION_LIST_FRAGMENT_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |
| 🧩 Fragment | `DISCUSSION_PARTICIPANTS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `DISCUSSION_PARTICIPANTS_FRAGMENT_NEW_WIP` | `src/libs/core-discussions/src/graphql/DiscussionMutations.ts` |
| 🧩 Fragment | `DISCUSSION_TEAMS_FRAGMENT` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |
| 🧩 Fragment | `REPLY_DETAILS_FRAGMENT_V2` | `src/libs/core-discussions/src/graphql/DiscussionMutations.ts`, `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🧩 Fragment | `USER_PROFILE_ATTRIBUTES_FRAGMENT` | `src/libs/core-discussions/src/graphql/DiscussionMutations.ts`, `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |

### `src/libs/core-discussions/src/graphql/DiscussionMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_DISCUSSION_REPLY_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx` |
| ✏️ Mutation | `CORE_ADD_DISCUSSION_V3` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx`, `src/libs/core-discussions/src/customHooks/useSparkDiscussionProps.tsx` |
| ✏️ Mutation | `CORE_DELETE_PARTICIPANTS_V3` | `src/libs/core-discussions/index.tsx`, `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyListing.tsx`, `src/libs/core-discussions/src/components/DiscussionReplyForm.tsx`, `src/libs/core-discussions/src/graphql/index.ts` |
| ✏️ Mutation | `CORE_UPDATE_DISCUSSION_V3` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx` |
| ✏️ Mutation | `CORE_UPDATE_PARTICIPANTS_V3` | `src/libs/core-discussions/index.tsx`, `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyListing.tsx`, `src/libs/core-discussions/src/components/DiscussionReplyForm.tsx`, `src/libs/core-discussions/src/graphql/index.ts` |
| ✏️ Mutation | `DELETE_ATTACHMENTS` | 8 files |
| ✏️ Mutation | `DELETE_DISCUSSION_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx` |
| ✏️ Mutation | `DELETE_REPLY_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| ✏️ Mutation | `DISCUSSION_READ_BY_USERS` | `src/libs/core-discussions/src/containers/DiscussionComponent.tsx`, `src/libs/core-discussions/src/containers/DiscussionReply.tsx` |
| ✏️ Mutation | `UPDATE_AS_CRITICAL` | `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyHeader.tsx`, `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyListing.tsx` |
| ✏️ Mutation | `UPDATE_DISCUSSION_EDITABLE` | `src/libs/core-discussions/src/containers/DiscussionComponent.tsx`, `src/libs/core-discussions/src/containers/DiscussionReply.tsx` |
| ✏️ Mutation | `UPDATE_REPLY_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| ✏️ Mutation | `UPDATE_TAG_EXISTING` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx` |

### `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `BULK_UPDATE_PRODUCT_PROPS` | `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyListing.tsx` |
| 🔍 Query | `CORE_GET_DISCUSSION_ON_RESOURCE_EDITABLE_CHECK` | `src/libs/core-discussions/src/components/DiscussionModalReplyForm.tsx` |
| 🔍 Query | `CORE_GET_DISCUSSION_V2` | `src/libs/core-discussions/src/NewLayout/components/DiscussionReplyHeader.tsx`, `src/libs/core-discussions/src/containers/DiscussionReply.tsx`, `src/libs/core-discussions/src/customHooks/useSparkEditDiscussionProps.tsx`, `src/libs/core-discussions/src/utilities/functionsReplyDiscussion.tsx` |
| 🔍 Query | `CORE_GET_DISCUSSION_V2_EDITABLE_CHECK` | `src/libs/core-discussions/src/components/DiscussionModalReplyForm.tsx` |
| 🔍 Query | `GET_ARTWORK_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_COLOR_ARCHROMA_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_COLOR_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_COMBINATION_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_DISCUSSIONS_V2` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_DISCUSSION_ON_RESOURCE` | 10 files |
| 🔍 Query | `GET_FABRIC_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_FILES` | 10 files |
| 🔍 Query | `GET_HUB_MATERIAL_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_HUB_MATERIAL_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_PALETTE_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_PRODUCT_TEAMS` | 10 files |
| 🔍 Query | `GET_SPARK_ARTWORK_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_COLOR_ARCHROMA_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_COLOR_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_COMBINATION_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_FABRIC_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_PALETTE_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_PRODUCT_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts`, `src/libs/product/src/components/ImportProductDetailsSection.tsx` |
| 🔍 Query | `GET_SPARK_PRODUCT_V2` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/core-discussions/src/utilities/functionsNewDiscussion.tsx`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts`, `src/libs/workspaces/src/routes/products/components/ProductsListItem.tsx` |
| 🔍 Query | `GET_SPARK_TRIM_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_WASH_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_WORKSPACE_BP` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_SPARK_WORKSPACE_V2` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/core-discussions/src/utilities/functionsNewDiscussion.tsx`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_TRIM_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_VERSIONED_DISCUSSIONS` | `src/libs/core-discussions/src/molecules/DiscussionDraftEditHistory.tsx` |
| 🔍 Query | `GET_VERSIONED_DISCUSSION_THREADS` | `src/libs/core-discussions/src/molecules/DiscussionDraftEditHistory.tsx` |
| 🔍 Query | `GET_WASH_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS` | 8 files |
| 🔍 Query | `GET_WORKSPACE_TEAMS` | `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product-queries/src/queries/ProductQueries.tsx` |

---

## Core — Favorites

**4 definitions** — 2 queries, 2 mutations

### `src/libs/core-favorites/src/graphql/FavoriteQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_FAVORITE` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/mocks/index.ts`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsMutations.ts` |
| ✏️ Mutation | `DELETE_FAVORITE` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/mocks/index.ts`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsMutations.ts` |
| 🔍 Query | `GET_FAVORITE_TYPES_FOR_CURRENT_USER` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/mocks/index.ts`, `src/libs/core-favorites/src/molecules/FavoritesMenu.tsx` |
| 🔍 Query | `IS_ENTITY_FAVORITE` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/mocks/index.ts` |

---

## Core — File Management

**6 definitions** — 6 mutations

### `src/libs/core-file-management/src/OrganizationAndFindability/graphql/coreFileManagementQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ARCHIVE_ATTACHMENT` | 11 files |
| ✏️ Mutation | `ARCHIVE_ATTACHMENT_V2` | _not referenced_ |
| ✏️ Mutation | `FILES_BULK_UPDATE` | 6 files |
| ✏️ Mutation | `UPDATE_ATTACHMENT_MARK_3D_FINAL` | `src/libs/core-file-management/src/OrganizationAndFindability/OrganizationAndFindability.tsx`, `src/libs/product-common/src/components/files/use3DFileUtils.ts`, `src/libs/spark-legacy/components/attachments/graphql/ComponentAttachmentsMutations.ts` |
| ✏️ Mutation | `UPDATE_TAGS` | `src/libs/core-file-management/src/OrganizationAndFindability/components/AttachmentTagsModal.tsx` |
| ✏️ Mutation | `UPDATE_TAGS_V3` | `src/libs/core-file-management/src/OrganizationAndFindability/components/AttachmentTagsModal.tsx` |

---

## Core — Tags

**1 definitions** — 1 queries

### `src/libs/core-tags/src/graphql/CoreTagsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_TAGS_BY_TYPE` | 12 files |

---

## Product — Common

**57 definitions** — 34 queries, 19 mutations, 4 fragments

### `src/libs/product-common/src/components/PermissionsMultiselect.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_DISCUSSION_ON_RESOURCE` | 10 files |

### `src/libs/product-common/src/queries/MeasurementQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `DELETE_SAMPLE_MEASUREMENT` | `src/libs/product-common/index.ts`, `src/libs/samples/src/components/SampleCompare.tsx`, `src/libs/samples/src/pages/Sample.tsx` |
| ✏️ Mutation | `LOCK_MEASUREMENT_SET` | `src/libs/measurement-sets/src/templates/MeasurementSetTemplate.tsx`, `src/libs/product-common/index.ts` |
| ✏️ Mutation | `PUT_SAMPLE_MEASUREMENT` | `src/libs/product-common/index.ts`, `src/libs/samples/src/components/SampleCompare.tsx`, `src/libs/samples/src/graphql/SampleNew.tsx`, `src/libs/samples/src/pages/Sample.tsx`, `src/libs/samples/src/templates/SampleMeasurementEditTemplate.tsx` |
| ✏️ Mutation | `UNLOCK_MEASUREMENT_SET` | `src/libs/measurement-sets/src/templates/MeasurementSetTemplate.tsx`, `src/libs/product-common/index.ts` |
| 🔍 Query | `GET_MEASUREMENTS` | `src/libs/product-common/index.ts`, `src/libs/samples/src/components/ImportMeasurementSet.tsx` |
| 🔍 Query | `GET_MEASUREMENTS_META_DATA` | `src/libs/measurement-sets/src/containers/MeasurementQueries.testHelper.ts`, `src/libs/product-common/index.ts`, `src/libs/product-common/src/helpers/withMeasurementsMetaData.tsx` |
| 🔍 Query | `GET_MEASUREMENT_BY_IDS` | 6 files |
| 🔍 Query | `GET_MEASUREMENT_SET_STATUS` | `src/libs/measurement-sets/src/templates/TightFitTemplateEditLayout.tsx`, `src/libs/product-common/index.ts` |
| 🔍 Query | `GET_MEASURMENT_VERSION` | `src/libs/measurement-sets/src/templates/MeasurementSetTemplate.test.tsx`, `src/libs/measurement-sets/src/templates/MeasurementSetTemplate.tsx`, `src/libs/product-common/index.ts` |
| 🔍 Query | `GET_UNITS_OF_MEASURE` | 5 files |
| 🔍 Query | `MEASUREMENT_FIELDS_FRAGMENT` | `src/libs/product-common/index.ts` |
| 🔍 Query | `SAMPLE_MEASUREMENT_FRAGMENT` | `src/libs/samples/index.ts`, `src/libs/samples/src/components/workspace/BulkEvaluate/CombinationSamplesBulkEvaluate.tsx` |
| 🔍 Query | `SEARCH_POM_SUGGESTIONS` | `src/libs/product-common/index.ts` |

### `src/libs/product-common/src/queries/TightFitQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `TIGHT_FIT_FRAGMENT` | 5 files |
| ✏️ Mutation | `ADD_TIGHT_FIT` | `src/libs/measurement-sets/src/templates/TightFitTemplateNewLayout.tsx`, `src/libs/product-common/index.ts` |
| ✏️ Mutation | `UPDATE_TIGHT_FIT` | `src/libs/measurement-sets/src/templates/TightFitTemplateEditLayout.tsx`, `src/libs/product-common/index.ts` |
| 🔍 Query | `GET_TIGHT_FITS` | 5 files |

### `src/libs/product-common/src/queries/WorkspacePlanQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `BID_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `COMPARE_VERSIONS` | `src/libs/workspaces/src/routes/plan/containers/WorkspacePlanContainer.tsx` |
| ✏️ Mutation | `MOVE_PRODUCTS_TO` | `src/libs/workspaces/src/routes/plan/components/MoveDrawer.tsx` |
| ✏️ Mutation | `PRODUCT_ASK_ASSOCIATION` | `src/libs/product/src/containers/ProductNew.tsx`, `src/libs/workspaces/src/routes/plan/components/AssociateProductModal.tsx` |
| ✏️ Mutation | `REMOVE_PRODUCTS` | `src/libs/workspaces/src/routes/plan/components/MoveDrawer.tsx` |
| ✏️ Mutation | `UPDATE_RECOMMENDATION_STATUS` | `src/libs/workspaces/src/routes/plan/components/WorkspacePlanGrid.tsx` |
| 🔍 Query | `FIND_PRODUCT_ASKS_PLM` | `src/libs/workspaces/src/routes/plan/containers/WorkspacePlanContainer.tsx` |
| 🔍 Query | `GET_BUSINESS_PARTNER_BY_ID` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/specifications/components/FabricSpecificationForm.tsx`, `src/libs/spark-materials/src/customHooks/useMVRelatedSuppliers.ts`, `src/libs/workspaces/src/routes/plan/components/HistoryDrawer.tsx` |
| 🔍 Query | `GET_PRODUCT_ASK` | `src/libs/product/src/containers/ProductNew.tsx`, `src/libs/workspaces/src/routes/plan/components/CostingCellRenderer.tsx`, `src/libs/workspaces/src/routes/plan/components/MoveDrawer.tsx`, `src/libs/workspaces/src/routes/plan/components/WorkspacePlanGrid.tsx` |
| 🔍 Query | `GET_PRODUCT_ASK_PLM` | _not referenced_ |
| 🔍 Query | `GET_USERS_BY_IDS` | _not referenced_ |
| 🔍 Query | `GET_WORKSPACE_ASK_IDS` | `src/libs/workspaces/src/routes/plan/containers/WorkspacePlanContainer.tsx` |
| 🔍 Query | `GET_WORKSPACE_PLAN` | `src/libs/workspaces/src/routes/plan/containers/WorkspacePlanContainer.tsx` |
| 🔍 Query | `SEARCH_ASK_ACTIVITY` | `src/libs/workspaces/src/routes/plan/context/ProductPlan.tsx` |

### `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `SAMPLE_LIST_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `WORKSPACE_PRODUCT_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `BULK_GENERATE_TECHPACK` | `src/libs/spark-mock-data-builders/src/builders/product.ts`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGenerateProductPacketModal.tsx`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGenerateReleasePacketModal.tsx` |
| ✏️ Mutation | `EXPORT_PACKAGING` | `src/libs/workspaces/src/routes/products/components/WorkspaceDownloadDropdown.tsx` |
| ✏️ Mutation | `EXPORT_WORKSPACE` | `src/libs/workspaces/src/routes/products/components/WorkspaceDownloadDropdown.tsx` |
| ✏️ Mutation | `EXPORT_WORKSPACE_EXCEL` | `src/libs/workspaces/src/routes/products/components/WorkspaceDownloadDropdown.tsx` |
| ✏️ Mutation | `MANAGE_PRODUCT_WORKSPACES` | `src/libs/product/src/components/ManageComponentWorkspacesModal.tsx` |
| ✏️ Mutation | `PACKAGING_EXCEL_EXPORT` | `src/libs/workspaces/src/routes/products/components/WorkspaceDownloadDropdown.tsx` |
| ✏️ Mutation | `PRODUCT_BULK` | `src/libs/workspaces/src/routes/products/containers/ProductBulkCreate.tsx` |
| ✏️ Mutation | `PRODUCT_BULK_UPDATE` | `src/libs/workspaces/src/routes/products/containers/ProductBulkUpdate.tsx` |
| 🔍 Query | `BULK_TECHPACK_COUNTS` | `src/libs/spark-mock-data-builders/src/builders/product.ts`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGenerateProductPacketModal.tsx`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGenerateReleasePacketModal.tsx` |
| 🔍 Query | `GET_BULK_CREATE_FORM_DATA` | `src/libs/workspaces/src/routes/products/containers/ProductBulkCreate.tsx` |
| 🔍 Query | `GET_FILES` | 10 files |
| 🔍 Query | `GET_FILES_WITH_METADATA` | `src/libs/workspaces/src/routes/products/components/BulkEditModal/utils/handleUpdateSubmit.tsx` |
| 🔍 Query | `GET_PRODUCTS_BY_ID_LIST` | `src/libs/workspaces/src/routes/products/containers/ProductBulkUpdate.tsx` |
| 🔍 Query | `GET_PRODUCT_SAMPLES` | _not referenced_ |
| 🔍 Query | `GET_SAMPLES_BY_ID_LIST` | `src/libs/workspaces/src/routes/products/components/ProductsListItem.tsx` |
| 🔍 Query | `GET_WORKSPACE_CATEGORY` | `src/libs/product-common/src/components/ProductListSideFilterForm.tsx`, `src/libs/spark-legacy/routes/users/components/UserListSideFilterForm.tsx` |
| 🔍 Query | `GET_WORKSPACE_CATEGORY_CLAZZ` | `src/libs/product-common/src/components/ProductListSideFilterForm.tsx` |
| 🔍 Query | `GET_WORKSPACE_DASHBOARD_STATUSES` | `src/libs/workspaces/src/components/workspaceDashboard/WorkspaceDashboard.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_HIDDEN` | `src/libs/workspaces/src/routes/products/components/WorkspaceProductsListBody.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_IDS` | `src/libs/workspaces/src/routes/products/containers/WorkspaceProducts.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_WITH_IDS` | 11 files |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_WITH_IDS_NO_SAMPLES_NO_COUNTS` | `src/libs/product-packaging/src/organisms/bulk/PackagingBulkSelectProducts.tsx` |
| 🔍 Query | `SEARCH_WORKSPACE_PRODUCTS_SUGGESTIONS` | `src/libs/workspaces/src/routes/products/containers/WorkspaceProducts.tsx` |

---

## Product — Details

**18 definitions** — 8 queries, 8 mutations, 2 fragments

### `src/libs/product-details/src/graphql/SpecificationQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PRODUCT_DETAILS_DATA_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `SPECIFICATION_TEMPLATE_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `CLONE_PDTL_ATTACHMENTS` | `src/libs/product-details/src/templates/ProductDetailClone.tsx` |
| ✏️ Mutation | `CREATE_CATEGORY_SECTION` | `src/libs/product-details/src/containers/ProductDetailsTemplateList.tsx` |
| ✏️ Mutation | `CREATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/src/containers/ProductDetailsSetNew.tsx`, `src/libs/product-details/src/templates/ProductDetailClone.tsx` |
| ✏️ Mutation | `CREATE_SPECIFICATIONS` | `src/libs/product-details/src/containers/ProductDetailsTemplateNew.tsx` |
| ✏️ Mutation | `PRODUCT_DETAILS_LOCK_UNLOCK` | `src/libs/product-details/src/templates/ProductDetailsViewTemplate.tsx` |
| ✏️ Mutation | `UPDATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/index.ts`, `src/libs/product-details/src/templates/ProductDetailsViewTemplate.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateProductDetailsEdit.tsx` |
| ✏️ Mutation | `UPDATE_PRODUCT_DETAIL_COMPONENT_STATUS` | `src/libs/product-details/src/templates/ProductDetailsViewTemplate.tsx` |
| ✏️ Mutation | `UPDATE_SPECIFICATIONS` | `src/libs/product-details/src/containers/ProductDetailsTemplateEdit.tsx` |
| 🔍 Query | `GET_MASTER_DATA_AND_SPECIFICATION_TEMP_BY_ID` | `src/libs/product-details/src/containers/ProductDetailsTemplateEdit.tsx` |
| 🔍 Query | `GET_PRODUCT_DETAILS_SET_BY_IDS` | 6 files |
| 🔍 Query | `GET_PRODUCT_DETAILS_VERSION` | `src/libs/product-details/src/templates/ProductDetailsViewTemplate.tsx` |
| 🔍 Query | `GET_SPECIFICATIONS` | `src/libs/product-details/src/containers/ProductDetailsTemplateEdit.tsx`, `src/libs/product-details/src/containers/ProductDetailsTemplateNew.tsx` |
| 🔍 Query | `GET_SPECIFICATIONS_MASTER_DATA` | 6 files |
| 🔍 Query | `GET_SPECIFICATION_BY_ID` | `src/libs/product-details/src/containers/ProductDetailsTemplateView.tsx` |
| 🔍 Query | `PRODUCT_DETAILS_TEMPLATE_SEARCH` | `src/libs/product-details/index.ts`, `src/libs/product-details/src/containers/ProductDetailsTemplateList.tsx`, `src/libs/spark-legacy/components/grid/productDetails/ProductDetailsDetailEditor.tsx` |
| 🔍 Query | `PRODUCT_DETAILS_TEMPLATE_SEARCH_SUGGESTION` | `src/libs/product-details/src/containers/ProductDetailsTemplateList.tsx` |

---

## Product — Packaging

**25 definitions** — 14 queries, 10 mutations, 1 fragments

### `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PACKAGING_PACKET_INFORMATION_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `ADD_PACKAGING_DETAIL` | `src/libs/product-packaging/src/templates/PackagingDetailsCloneTemplate.tsx`, `src/libs/product-packaging/src/templates/PackagingDetailsNewTemplate.tsx` |
| ✏️ Mutation | `BULK_ADD_PACKAGING_DETAILS` | `src/libs/product-packaging/src/pages/PackagingBulkCreate.tsx` |
| ✏️ Mutation | `BULK_UPDATE_PACKAGING_DETAILS` | `src/libs/product-packaging/src/pages/PackagingBulkUpdate.tsx` |
| ✏️ Mutation | `EVALUATE_DIELINE` | `src/libs/product-packaging/src/molecules/PackagingEvaluationButton.tsx` |
| ✏️ Mutation | `GENERATE_PACKAGING_PACKET` | `src/libs/product-packaging/src/organisms/GeneratePackagingPacketModal.tsx` |
| ✏️ Mutation | `GENERATE_PACKAGING_PACKETS_BULK` | `src/libs/product-packaging/index.ts`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGeneratePackagingPacketModal.tsx` |
| ✏️ Mutation | `LOCK_PACKAGING` | `src/libs/product-packaging/src/templates/PackagingDetailsTemplate.tsx` |
| ✏️ Mutation | `UNLOCK_PACKAGING` | `src/libs/product-packaging/src/templates/PackagingDetailsTemplate.tsx` |
| ✏️ Mutation | `UPDATE_PACKAGING_COMPONENT_STATUS` | `src/libs/product-packaging/src/templates/PackagingDetailsTemplate.tsx` |
| ✏️ Mutation | `UPDATE_PACKAGING_DETAIL` | `src/libs/product-packaging/src/templates/PackagingDetailsTemplate.tsx` |
| 🔍 Query | `GET_DIELINES` | `src/libs/product-packaging/src/customHooks/useFetchDielines.ts` |
| 🔍 Query | `GET_DIELINE_STATUS_LIST` | `src/libs/product-packaging/src/customHooks/useFetchDielineStatusList.tsx` |
| 🔍 Query | `GET_FILES` | 10 files |
| 🔍 Query | `GET_LOCATION_INFO` | `src/libs/product-packaging/src/customHooks/useLocationInfo.tsx` |
| 🔍 Query | `GET_PACKAGING_DETAIL` | _not referenced_ |
| 🔍 Query | `GET_PACKAGING_DETAILS_BY_PARENTS` | _not referenced_ |
| 🔍 Query | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/spark-packaging-base/index.ts`, `src/libs/spark-packaging-base/src/customHooks/usePackagingDetailsByParent.tsx`, `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts` |
| 🔍 Query | `GET_PACKAGING_DETAIL_WITH_INTERNAL_DATA` | `src/libs/product-packaging/index.ts`, `src/libs/product-packaging/src/customHooks/usePackagingDetail.test.tsx`, `src/libs/product-packaging/src/customHooks/usePackagingDetail.tsx` |
| 🔍 Query | `GET_PACKAGING_PACKETS_INFORMATION` | `src/libs/product-packaging/index.ts`, `src/libs/spark-mock-data-builders/src/builders/product.ts`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGeneratePackagingPacketModal.tsx` |
| 🔍 Query | `GET_PACKAGING_PACKET_INFORMATION` | `src/libs/product-packaging/src/helpers/PackagingPacketUtils.ts` |
| 🔍 Query | `GET_PACKAGING_SUPPLIERS` | `src/libs/product-packaging/src/molecules/PackagingDetailsElementsPrintersSection.tsx` |
| 🔍 Query | `GET_PRINTER_INFORMATION` | `src/libs/product-packaging/src/customHooks/usePrinterInformation.tsx` |
| 🔍 Query | `GET_WORKSPACES_DESCRIPTION` | `src/libs/product-packaging/index.ts`, `src/libs/product-packaging/src/pages/PackagingBulkCreate.tsx` |
| 🔍 Query | `USE_DPCI_INFO` | `src/libs/product-packaging/src/customHooks/useDpciInformation.tsx` |

---

## Product — Queries

**167 definitions** — 95 queries, 30 mutations, 42 fragments

### `src/libs/product-queries/src/queries/BomQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `BASE_IMPRESSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_ACCESS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_COLOR_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_COMBO_SLIM_DETAILS` | _not referenced_ |
| 🧩 Fragment | `BOM_COMBO_SUPPLIER_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_DETAILS_FRAGMENT` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` |
| 🧩 Fragment | `BOM_ELASTIC_HUB_MATERIAL_FIELDS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_ELASTIC_TRIM_FIELDS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_ELASTIC_WASH_FIELDS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_FABRIC_SPEC_DETAILS` | _not referenced_ |
| 🧩 Fragment | `BOM_HUB_BASE_MATERIAL_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_HUB_MATERIAL_COMPOSITION_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_HUB_MATERIAL_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `BOM_HUB_MATERIAL_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `FABRIC_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `ORIGIN_COMPOSITION_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `TRIM_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `TRIM_SUPPLIER_DETAILS` | _not referenced_ |
| 🧩 Fragment | `TRIM_ZIPPER_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `VMM_LOCATION_FIELDS` | `src/libs/spark-fabric-graphql/index.ts` |
| 🧩 Fragment | `WASH_IMPRESSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `WEIGHT_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `ADD_BOM` | `src/libs/bill-of-materials/src/routes/clone/BomCloneTemplate.tsx`, `src/libs/bill-of-materials/src/routes/create/BomCreateTemplate.tsx` |
| ✏️ Mutation | `LOCK_BOM` | `src/libs/bill-of-materials/src/routes/view/BomViewHeader.tsx` |
| ✏️ Mutation | `UNLOCK_BOM` | `src/libs/bill-of-materials/src/routes/view/BomViewHeader.tsx` |
| ✏️ Mutation | `UPDATE_BOM` | `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.tsx` |
| ✏️ Mutation | `UPDATE_BOM_COMPONENT_STATUS` | `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.tsx` |
| 🔍 Query | `BOM_SEARCH_HUB_MATERIAL_SLIM` | _not referenced_ |
| 🔍 Query | `BOM_SEARCH_MATERIALS` | 4 files |
| 🔍 Query | `BOM_SEARCH_TRIMS_SLIM` | _not referenced_ |
| 🔍 Query | `BOM_SEARCH_WASH_SLIM` | _not referenced_ |
| 🔍 Query | `GET_ATTACHMENTS_BY_RESOURCE` | `src/libs/bill-of-materials/src/BomForm.tsx`, `src/libs/bill-of-materials/src/packagingBom/PackagingBomForm.tsx`, `src/libs/spark-legacy/customHooks/useAttachmentsByResource.tsx` |
| 🔍 Query | `GET_BOMS_BY_IDS` | `src/libs/bill-of-materials/src/customHooks/useBomsByIds.ts`, `src/libs/bill-of-materials/src/routes/clone/BomCloneTemplate.tsx`, `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.test.tsx` |
| 🔍 Query | `GET_BOMS_BY_IDS_WITH_PRODUCT_INFO` | `src/libs/bill-of-materials/src/routes/view/BomViewRoute.test.tsx`, `src/libs/bill-of-materials/src/routes/view/BomViewRouteEdit.test.tsx`, `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.tsx` |
| 🔍 Query | `GET_BOMS_BY_PARENT_ID` | `src/libs/bill-of-materials/src/customHooks/useBomsByParentId.ts` |
| 🔍 Query | `GET_BOMS_FROM_ES_BY_PARENT_IDS` | `src/libs/bill-of-materials/src/customHooks/useBomsByParentIdsFromES.ts` |
| 🔍 Query | `GET_BOM_MATERIAL_TYPES` | `src/libs/bill-of-materials/src/customHooks/useBomMaterialTypes.test.tsx`, `src/libs/bill-of-materials/src/customHooks/useBomMaterialTypes.ts` |
| 🔍 Query | `GET_BOM_PACKAGING_MASTER_DATA` | `src/libs/bill-of-materials/src/customHooks/useBomMaterialTypes.test.tsx`, `src/libs/bill-of-materials/src/customHooks/useBomMaterialTypes.ts` |
| 🔍 Query | `GET_BOM_PACKAGING_SUBSTRATES` | `src/libs/bill-of-materials/src/helpers/grid/fetchPackagingSubstrateOptions.ts`, `src/libs/spark-packaging-library/src/graphql/PackagingLibraryQueries.testHelper.ts` |
| 🔍 Query | `GET_BOM_STATUS` | `src/libs/bill-of-materials/src/helpers/withBomStatuses.tsx` |
| 🔍 Query | `GET_BOM_VERSION` | `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.tsx` |
| 🔍 Query | `GET_COMBINATION_SUPPLIER_FOR_BOM` | `src/libs/bill-of-materials/src/utils/mapCombinationDataToMaterial.ts` |
| 🔍 Query | `GET_FILES_V3` | 5 files |
| 🔍 Query | `GET_HUB_MATERIALS_BY_IDS` | `src/libs/bill-of-materials/src/helpers/handleImportHubMaterials.test.ts`, `src/libs/bill-of-materials/src/helpers/handleImportHubMaterials.ts` |
| 🔍 Query | `GET_HUB_MATERIAL_INFO_OPTIONS` | `src/libs/bill-of-materials/src/context/MaterialTemplateConfigs.tsx`, `src/libs/spark-mock-data-builders/src/builders/bom.ts` |
| 🔍 Query | `GET_MATERIAL_TEMPLATE` | `src/libs/bill-of-materials/src/context/MaterialTemplateConfigs.tsx` |
| 🔍 Query | `GET_TRIMS_BY_ID` | `src/libs/bill-of-materials/src/helpers/handleImportTrims.test.ts`, `src/libs/bill-of-materials/src/helpers/handleImportTrims.ts` |
| 🔍 Query | `GET_TRIM_TYPES` | 6 files |
| 🔍 Query | `GET_TRIM_UNIT_OF_MEASURES` | `src/libs/bill-of-materials/src/customHooks/useBomTrimUnitOfMeasures.ts` |
| 🔍 Query | `GET_VALID_SUPPLIERS_FOR_BOM` | `src/libs/bill-of-materials/src/BomForm.tsx`, `src/libs/bill-of-materials/src/packagingBom/PackagingBomForm.tsx` |
| 🔍 Query | `GET_WASHES_BY_ID` | `src/libs/bill-of-materials/src/helpers/handleImportWash.test.ts`, `src/libs/bill-of-materials/src/helpers/handleImportWash.ts` |
| 🔍 Query | `SEARCH_FABRIC_SPEC_COMBOS` | _not referenced_ |

### `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `DISCUSSION_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `DISCUSSION_DETAILS_FRAGMENT_V2` | _not referenced_ |
| 🧩 Fragment | `LEGACY_DISCUSSION_ATTACHMENT_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `LEGACY_DISCUSSION_LIST_FRAGMENT_V2` | _not referenced_ |
| 🧩 Fragment | `LEGACY_DISCUSSION_PARTICIPANTS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `LEGACY_DISCUSSION_TEAMS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `LEGACY_USER_PROFILE_ATTRIBUTES_FRAGMENT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` |
| 🧩 Fragment | `REPLY_DETAILS_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `REPLY_DETAILS_FRAGMENT_V2` | `src/libs/core-discussions/src/graphql/DiscussionFragments.ts`, `src/libs/core-discussions/src/graphql/DiscussionMutations.ts`, `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` |
| ✏️ Mutation | `ADD_ATTACHMENTS` | _not referenced_ |
| ✏️ Mutation | `ADD_SAMPLE_DISCUSSION_V3` | _not referenced_ |
| ✏️ Mutation | `DELETE_ATTACHMENTS` | 8 files |
| ✏️ Mutation | `DELETE_PARTICIPANT_V2` | _not referenced_ |
| ✏️ Mutation | `DELETE_REPLY_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx`, `src/libs/core-discussions/src/graphql/DiscussionMutations.ts` |
| ✏️ Mutation | `UPDATE_REPLY_V2` | `src/libs/core-discussions/src/customHooks/useDiscussionMutations.tsx`, `src/libs/core-discussions/src/graphql/DiscussionMutations.ts` |
| 🔍 Query | `GET_ARTWORK_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_COLOR_ARCHROMA_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_COLOR_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_COMBINATION_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_DISCUSSIONS_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_FABRIC_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_HUB_MATERIAL_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_HUB_MATERIAL_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_PALETTE_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_PRODUCT_TEAMS` | 10 files |
| 🔍 Query | `GET_SPARK_ARTWORK_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_COLOR_ARCHROMA_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_COLOR_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_COMBINATION_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_FABRIC_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_PALETTE_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_PRODUCT_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/product/src/components/ImportProductDetailsSection.tsx` |
| 🔍 Query | `GET_SPARK_PRODUCT_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/core-discussions/src/utilities/functionsNewDiscussion.tsx`, `src/libs/workspaces/src/routes/products/components/ProductsListItem.tsx` |
| 🔍 Query | `GET_SPARK_TRIM_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_WASH_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_WORKSPACE_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_SPARK_WORKSPACE_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts`, `src/libs/core-discussions/src/utilities/functionsNewDiscussion.tsx` |
| 🔍 Query | `GET_TRIM_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `GET_USERS` | 9 files |
| 🔍 Query | `GET_WASH_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |

### `src/libs/product-queries/src/queries/ProductFilesQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `ATTACHMENT_V3_FRAGMENT` | `src/libs/product-queries/src/queries/WorkspaceFilesQueries.ts`, `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` |
| 🧩 Fragment | `PRODUCT_COMPONENT_FRAGMENT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts`, `src/libs/product-queries/src/queries/ProductQueries.tsx` |
| 🔍 Query | `GET_PRODUCT_COMPONENT_STATUS_COUNTS` | `src/libs/bill-of-materials/src/routes/view/BomViewTemplate.tsx`, `src/libs/product-queries/src/queries/ProductFilesQueries.testHelper.tsx`, `src/libs/product/src/containers/SpecsContainer.tsx` |
| 🔍 Query | `GET_PRODUCT_WITH_ATTACHMENTS_AND_COMPONENTS` | 17 files |
| 🔍 Query | `GET_RENDERS_FOR_ATTACHMENT_IDS` | `src/libs/spark-legacy/components/attachments/Carousel.tsx` |
| 🔍 Query | `GET_RENDERS_FOR_ATTACHMENT_V3_IDS` | `src/libs/spark-legacy/components/attachments/Carousel.tsx` |

### `src/libs/product-queries/src/queries/ProductFragments.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PRODUCT_BASE_INFO_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts`, `src/libs/product-queries/src/queries/ProductFilesQueries.tsx`, `src/libs/product-queries/src/queries/ProductQueries.tsx`, `src/libs/watchlist/src/graphql/WatchlistQueries.ts` |
| 🧩 Fragment | `PRODUCT_FULL_TEAM_FRAGMENT` | `src/libs/product-queries/src/queries/ProductQueries.tsx`, `src/libs/product-queries/src/queries/TeamTabQueries.ts` |
| 🧩 Fragment | `PRODUCT_VENDOR_ATTRIBUTES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` |
| 🧩 Fragment | `VMM_BUSINESS_PARTNER_ON_PRODUCT` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts`, `src/libs/product-queries/src/queries/ProductQueries.tsx`, `src/libs/product-queries/src/queries/TeamTabQueries.ts`, `src/libs/watchlist/src/graphql/WatchlistQueries.ts` |

### `src/libs/product-queries/src/queries/ProductQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `LINK_PRODUCT_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `PRODUCT_TEAMS_INFO` | `src/libs/product-queries/src/queries/workspaceQueries.tsx` |
| ✏️ Mutation | `ADD_PRODUCT` | `src/libs/product/src/containers/ProductNew.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateNew.tsx` |
| ✏️ Mutation | `ADD_WORKSPACE_RESOURCES` | `src/libs/product-common/index.ts`, `src/libs/product/src/components/carry-forward/SelectDepartmentModal.tsx`, `src/libs/product/src/customHooks/useAddWorkspace.tsx` |
| ✏️ Mutation | `CARRY_FORWARD_PRODUCT` | `src/libs/product/src/containers/ProductCarryForwardModal.tsx`, `src/libs/workspaces/src/routes/plan/components/WorkspacePlanGrid.tsx` |
| ✏️ Mutation | `CHANGE_PRODUCT_WORKSPACE` | `src/libs/product-queries/src/queries/ProductQueries.testHelper.tsx`, `src/libs/product/src/components/RemoveFromWorkspaceModal.tsx`, `src/libs/product/src/customHooks/useWorkspaceSelectorProps.tsx` |
| ✏️ Mutation | `CORE_GENERATE_PDF` | _not referenced_ |
| ✏️ Mutation | `LINK_PRODUCT` | `src/libs/product/src/components/ProductActionsDropDown.tsx` |
| ✏️ Mutation | `UNLINK_PRODUCT` | `src/libs/product/src/components/overview/Links.tsx`, `src/libs/spark-legacy/Spark-Components/ProductLinkRailListItem.tsx` |
| ✏️ Mutation | `UPDATE_COMPONENT_STATUS` | `src/libs/product-common/src/components/ComponentStatusDropdown.tsx`, `src/libs/spark-mock-data-builders/src/builders/bom.ts` |
| ✏️ Mutation | `UPDATE_COMPONENT_STATUSES` | `src/libs/product/src/components/overview/ProductComponentSetStatusesDropdown.tsx` |
| ✏️ Mutation | `UPDATE_PRODUCT` | 7 files |
| ✏️ Mutation | `UPDATE_PRODUCT_PACKET_PROPS` | `src/libs/product/src/components/AttachmentProductPacketButton.tsx` |
| ✏️ Mutation | `UPDATE_PRODUCT_STATUSES` | `src/libs/product/src/components/BPSelector.tsx`, `src/libs/product/src/helpers/withProductPartnerStatuses.tsx`, `src/libs/workspaces/src/routes/products/components/ProductsGridItem.tsx`, `src/libs/workspaces/src/routes/products/components/ProductsListItemHeader.tsx` |
| 🔍 Query | `GET_ALL_PRODUCTS` | _not referenced_ |
| 🔍 Query | `GET_CARRY_FORWARD_FORM_DATA` | `src/libs/product-queries/src/queries/ProductQueries.testHelper.tsx`, `src/libs/product/src/containers/ProductCarryForwardModal.tsx`, `src/libs/workspaces/src/routes/plan/containers/WorkspaceCarryForwardSpecsForm.tsx` |
| 🔍 Query | `GET_CARRY_FORWARD_FORM_PLM` | `src/libs/workspaces/src/routes/plan/containers/WorkspaceCarryForwardSpecsForm.tsx` |
| 🔍 Query | `GET_COUNT_V1` | `src/libs/product/src/components/GenerateTechPackModal.tsx`, `src/libs/product/src/components/ReleaseTechPackModal.tsx` |
| 🔍 Query | `GET_PRODUCT` | `src/libs/product/src/components/ImportProductDetailsModal.tsx`, `src/libs/product/src/containers/ProductEdit.tsx`, `src/libs/samples/index.ts`, `src/libs/spark-mock-data-builders/src/builders/product.ts` |
| 🔍 Query | `GET_PRODUCTS_WITH_SAMPLE_DETAILS` | `src/libs/samples/src/components/SampleCompare.tsx` |
| 🔍 Query | `GET_PRODUCT_AND_WORKSPACES` | `src/libs/product/src/components/ReleaseProductPacket.tsx`, `src/libs/watchlist/src/components/WatchlistForm.tsx`, `src/libs/watchlist/src/containers/WatchlistViewTemplate.tsx` |
| 🔍 Query | `GET_PRODUCT_AND_WORKSPACES_WITH_STATUS` | `src/libs/product/src/components/ReleaseTechPackModal.tsx` |
| 🔍 Query | `GET_PRODUCT_FOR_STATUS_UPDATE` | `src/libs/product-queries/src/queries/ProductQueries.testHelper.tsx`, `src/libs/product/src/helpers/withProductPartnerStatuses.tsx` |
| 🔍 Query | `GET_PRODUCT_MINIMAL` | 7 files |
| 🔍 Query | `GET_RELEASE_PACKET_HISTORY` | `src/libs/product/src/components/ReleaseTechPackModal.tsx` |
| 🔍 Query | `GET_SPARK_PRODUCT_SCAFFOLDING` | 14 files |
| 🔍 Query | `GET_TEAMS_PRODUCT_AND_WORKSPACE` | `src/libs/product-queries/src/queries/ProductQueries.testHelper.tsx`, `src/libs/product/src/molecules/ReplaceWorkspaceFieldset.tsx` |
| 🔍 Query | `GET_WORKSPACE` | `src/libs/product/src/containers/ProductNew.tsx` |
| 🔍 Query | `GET_WORKSPACES_ONLY` | `src/libs/watchlist/src/components/WatchlistForm.tsx`, `src/libs/watchlist/src/containers/WatchlistViewTemplate.tsx` |
| 🔍 Query | `GET_WORKSPACE_DESCRIPTION` | `src/libs/product-queries/src/queries/ProductQueries.testHelper.tsx`, `src/libs/product/src/helpers/withProductPartnerStatuses.tsx` |
| 🔍 Query | `GET_WORKSPACE_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts`, `src/libs/core-discussions/src/utilities/discussionsUtils.ts` |
| 🔍 Query | `SEARCH_PRODUCTS` | `src/libs/product/src/components/ImportProductDetailsSection.tsx` |
| 🔍 Query | `SEARCH_PRODUCT_SUGGESTIONS` | _not referenced_ |
| 🔍 Query | `SEARCH_TEAMS` | 11 files |
| 🔍 Query | `SEARCH_TEAMS_RESOURCE_TYPE` | `src/libs/spark-legacy/routes/products/routes/teams/components/ProductAddTeamsBody.tsx`, `src/libs/spark-materials/src/customHooks/useMaterialTeams.ts` |
| 🔍 Query | `SEARCH_TEAMS_SAMPLES_ADD` | _not referenced_ |
| 🔍 Query | `SEARCH_TEAMS_TYPE_CHECK` | `src/libs/spark-legacy/routes/products/routes/teams/components/ProductAddTeamsBody.tsx` |

### `src/libs/product-queries/src/queries/TeamTabQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_PARTNERS_PRODUCT_WITH_TYPE` | _not referenced_ |
| ✏️ Mutation | `ADD_TEAMS_PRODUCT` | `src/libs/product/src/components/BPSelector.tsx` |
| ✏️ Mutation | `ADD_TEAMS_WORKSPACE` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |
| ✏️ Mutation | `BUSINESS_PARTNER_ACTIONS_PRODUCT` | `src/libs/product/src/components/overview/Teams.tsx` |
| ✏️ Mutation | `BUSINESS_PARTNER_ACTIONS_WORKSPACE` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |
| 🔍 Query | `GET_PRODUCT_WITH_TEAMS` | `src/libs/product/src/components/BPSelector.tsx`, `src/libs/product/src/components/overview/Teams.tsx` |
| 🔍 Query | `GET_WORKSPACE_WITH_TEAMS` | `src/libs/spark-combination/src/containers/CombinationNew.tsx`, `src/libs/spark-legacy/routes/products/routes/teams/components/ProductAddTeamsBody.tsx` |

### `src/libs/product-queries/src/queries/WorkspaceFilesQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `ATTACHMENTS_WITH_META_DATA_FRAGMENT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts`, `src/libs/product-queries/src/queries/TeamTabQueries.ts` |
| ✏️ Mutation | `FILES_BULK_UPDATE` | 6 files |
| 🔍 Query | `GET_PRODUCT_WITH_META_DATA` | _not referenced_ |
| 🔍 Query | `GET_WORKSPACE_WITH_ATTACHMENTS` | `src/libs/workspaces/src/routes/files/containers/WorkspaceFilesQueries.testHelper.tsx` |
| 🔍 Query | `GET_WORKSPACE_WITH_ATTACHMENT_META_DATA` | _not referenced_ |

### `src/libs/product-queries/src/queries/legacyDiscussionFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `LEGACY_COMPONENT_DISCUSSION_PARTICIPANTS_FRAGMENT` | 6 files |
| 🧩 Fragment | `LEGACY_PRODUCT_TEAMS_FOR_COMPONENT_DISCUSSION_FRAGMENT` | `src/libs/claims/src/graphql/ClaimQueries.ts`, `src/libs/product-common/src/queries/MeasurementQueries.tsx`, `src/libs/product-details/src/graphql/SpecificationQueries.ts` |

### `src/libs/product-queries/src/queries/workspaceQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `SAMPLE_BULK_CREATE` | `src/libs/samples/src/containers/combination/CombinationSampleBulkCreate.tsx`, `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination-graphql/src/CombinationsMutations.ts` |
| 🔍 Query | `BULK_RELEASE_PACKET_HISTORY` | `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGenerateReleasePacketModal.tsx` |
| 🔍 Query | `EXPORT_COMBO_ICS_WORKSPACE` | _not referenced_ |
| 🔍 Query | `EXPORT_COMBO_WORKSPACE` | _not referenced_ |
| 🔍 Query | `GET_PRODUCT_SAMPLE_CONSTANTS` | `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/SampleBulkUpdate.tsx`, `src/libs/samples/src/graphql/workspace/SampleBulkEvaluateQueries.tsx` |
| 🔍 Query | `GET_PRODUCT_WORKSPACES_METRICS_REPORT_COUNT` | `src/libs/workspaces/src/containers/WorkspaceOverview.tsx` |
| 🔍 Query | `GET_WORKSPACES_PAGED` | 18 files |
| 🔍 Query | `GET_WORKSPACE_CLONE` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |
| 🔍 Query | `GET_WORKSPACE_EDIT` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |
| 🔍 Query | `GET_WORKSPACE_OVERVIEW` | `src/libs/product/src/containers/ProductCarryForwardModal.tsx`, `src/libs/workspaces/src/containers/WorkspaceOverview.tsx`, `src/libs/workspaces/src/containers/WorkspaceOverviewQueries.testHelper.tsx`, `src/libs/workspaces/src/routes/products/components/BulkUpdate/ProductBulkCarryForwardModal.tsx` |
| 🔍 Query | `GET_WORKSPACE_PACKAGING_ATTACHMENTS` | `src/libs/product-packaging/src/helpers/PackagingPacketUtils.ts`, `src/libs/workspaces/src/routes/products/components/BulkGenerateModal/BulkGeneratePackagingPacketModal.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS` | 8 files |
| 🔍 Query | `GET_WORKSPACE_WITH_DISCUSSIONS` | `src/libs/workspaces/src/routes/files/containers/WorkspaceFiles.tsx` |
| 🔍 Query | `SEARCH_WORKSPACE_SUGGESTIONS` | _not referenced_ |

---

## Samples

**10 definitions** — 5 queries, 5 mutations

### `src/libs/samples/src/graphql/MultiColorSampleEditBody.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `UPDATE_MCE_SAMPLE` | _not referenced_ |
| 🔍 Query | `GET_MCE_SAMPLE_WITH_TYPES` | _not referenced_ |

### `src/libs/samples/src/graphql/SampleNew.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_SAMPLE` | 6 files |

### `src/libs/samples/src/graphql/workspace/SampleBulkEvaluateQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `BULK_EVALUATE_SAMPLES` | `src/libs/samples/index.ts`, `src/libs/samples/src/components/workspace/BulkEvaluate/CombinationSamplesBulkEvaluate.tsx`, `src/libs/samples/src/containers/workspace/BulkEvaluate/SampleBulkEvaluateTemplate.tsx` |
| ✏️ Mutation | `CLONE_SAMPLE_ATTACHMENTS` | `src/libs/samples/index.ts`, `src/libs/samples/src/components/workspace/BulkEvaluate/cloneSampleEvalFilesUtil.ts` |
| ✏️ Mutation | `SAMPLE_BULK_UPDATE` | `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/SampleBulkUpdate.tsx` |
| 🔍 Query | `GET_PRODUCT_SAMPLE_CONSTANTS` | `src/libs/product-queries/src/queries/workspaceQueries.tsx`, `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/SampleBulkUpdate.tsx` |
| 🔍 Query | `GET_SAMPLE_BULK_EVAL_FORM_DATA` | `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/BulkEvaluate/SampleBulkEvaluateQueries.testHelper.tsx`, `src/libs/samples/src/containers/workspace/BulkEvaluate/SampleBulkEvaluateTemplate.tsx` |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS` | 8 files |
| 🔍 Query | `GET_WORKSPACE_PRODUCTS_SAMPLES` | `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/BulkEvaluate/SampleBulkEvaluateSelect.tsx` |

---

## App Base

**1 definitions** — 1 queries

### `src/libs/spark-app-base/src/SparkUserSettings.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_USER_ROLES` | _not referenced_ |

---

## Artwork

**1 definitions** — 1 fragments

### `src/libs/spark-artwork-graphql/src/queries/ArtworkFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `GET_ARTWORK_DETAIL` | _not referenced_ |

---

## Color

**3 definitions** — 3 queries

### `src/libs/spark-color-graphql/src/queries/bestMatchColorSearchQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `BEST_MATCH_COLOR_SEARCH` | `src/libs/spark-color-graphql/index.ts`, `src/libs/spark-color/src/components/BestMatchWidget/index-RTL.test.tsx`, `src/libs/spark-color/src/components/BestMatchWidget/index.tsx`, `src/libs/spark-palette/src/aseimport/SelectableColorList.tsx` |

### `src/libs/spark-color-graphql/src/queries/colorExportQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `EXPORT_COLOR` | `src/libs/spark-color-graphql/index.ts` |
| 🔍 Query | `EXPORT_COLOR_ON_PALETTE` | `src/libs/spark-color-graphql/index.ts` |

---

## Combination

**43 definitions** — 24 queries, 15 mutations, 4 fragments

### `src/libs/spark-combination-graphql/src/ClmPackageFragment.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `CLM_PACKAGE_FRAGMENT` | `src/libs/spark-combination-graphql/index.ts` |

### `src/libs/spark-combination-graphql/src/CombinationsFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `IMPRESSION_INTENT_LINE_DETAILS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination-graphql/src/CombinationsMutations.ts` |
| 🧩 Fragment | `SLIM_COMBINATION_DETAILS_FRAGMENT` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination-graphql/src/CombinationsQueries.ts` |
| 🧩 Fragment | `SLIM_FABRIC_SPEC_COMBO_DETAILS_FRAGMENT` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination-graphql/src/CombinationsQueries.ts` |

### `src/libs/spark-combination-graphql/src/CombinationsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_IMPRESSION_INTENT` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/AddImpressionIntentModal.tsx` |
| ✏️ Mutation | `ADD_IMPRESSION_INTENT_LINE` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/AddMerchVendorModal.tsx` |
| ✏️ Mutation | `ADD_PARTNERS` | 6 files |
| ✏️ Mutation | `ARCHIVE_FABRIC_SPEC_COMBO` | `src/libs/samples/src/components/combination/CombinationSampleListItem.tsx`, `src/libs/spark-combination-graphql/index.ts` |
| ✏️ Mutation | `BULK_ADD_MERCH_VENDOR_TO_BUCKETS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/BulkAddMerchVendorModal.tsx` |
| ✏️ Mutation | `BULK_UPDATE_COMBINATION` | `src/libs/spark-combination-graphql/index.ts` |
| ✏️ Mutation | `CREATE_FABRIC_SPEC_COMBOS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/containers/CombinationOverview.tsx` |
| ✏️ Mutation | `DELETE_IMPRESSION_INTENT_BUCKET` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentBucket.tsx` |
| ✏️ Mutation | `DELETE_IMPRESSION_INTENT_LINE` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentLineOptionsDropdown.tsx` |
| ✏️ Mutation | `SAMPLE_BULK_CREATE` | `src/libs/product-queries/src/queries/workspaceQueries.tsx`, `src/libs/samples/src/containers/combination/CombinationSampleBulkCreate.tsx`, `src/libs/spark-combination-graphql/index.ts` |
| ✏️ Mutation | `SEND_BULK_UPDATE_COMBINATIONS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/bulkEdit/CombinationBulkEditStepTwo.tsx` |
| ✏️ Mutation | `UPDATE_IMPRESSION_INTENT_BUCKET` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentBucket.tsx` |
| ✏️ Mutation | `UPDATE_IMPRESSION_INTENT_LINE` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentLine.tsx`, `src/libs/spark-combination/src/components/ImpressionIntentLineOptionsDropdown.tsx`, `src/libs/spark-combination/src/containers/CombinationEdit.tsx` |
| ✏️ Mutation | `UPDATE_IMPRESSION_INTENT_LINE_STATUS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentLine.tsx`, `src/libs/spark-combination/src/components/ImpressionIntentLineOptionsDropdown.tsx` |
| ✏️ Mutation | `UPDATE_TEAMS_COMBINATION` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/teams/CombinationTeams.tsx` |

### `src/libs/spark-combination-graphql/src/CombinationsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_ARTWORK_FOR_SAMPLE` | `src/libs/samples/src/components/combination/bulkCreate/stepTwo/CombinationSampleStepTwoSample.tsx`, `src/libs/spark-combination-graphql/index.ts` |
| 🔍 Query | `GET_BUSINESS_PARTNER_DETAILS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/FabricSpecificationAutocomplete.tsx`, `src/libs/spark-combination/src/components/bulkEdit/fabric/CombinationFabricSpecAutoComplete.tsx` |
| 🔍 Query | `GET_COMBINATIONS_DETAILS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/bulkEdit/CombinationBulkEditStepTwo.test.tsx`, `src/libs/spark-combination/src/components/bulkEdit/CombinationBulkEditStepTwo.tsx` |
| 🔍 Query | `GET_COMBINATION_STATUS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-legacy/routes/combinations/containers/Combination.tsx` |
| 🔍 Query | `GET_COMBINATION_TEAMS_AND_RELATED_SUPPLIERS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/SampleYardageFormSection.tsx` |
| 🔍 Query | `GET_FABRIC_DETAILS` | 5 files |
| 🔍 Query | `GET_FSC_IDS_FROM_COMBO_ID` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/FSCSamplesViewWrapper.test.tsx`, `src/libs/spark-combination/src/components/FSCSamplesViewWrapper.tsx` |
| 🔍 Query | `GET_IMPRESSION_INTENTS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/AddImpressionIntentModal.tsx`, `src/libs/spark-legacy/components/ImpressionIntentFormSection.tsx`, `src/libs/spark-legacy/components/graphql/ComponentsQueries.ts` |
| 🔍 Query | `GET_RELATED_SUPPLIERS` | `src/libs/spark-combination-graphql/index.ts` |
| 🔍 Query | `GET_SAMPLE_LIST_COMBINATION_EXTERNAL` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/CombinationSamplesView.tsx` |
| 🔍 Query | `GET_SAMPLE_LIST_COMBINATION_INTERNAL` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/CombinationSamplesView.tsx` |
| 🔍 Query | `GET_SAMPLE_OPTIONS` | `src/libs/samples/src/containers/combination/CombinationSamplesList.tsx`, `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-fabric/src/routes/specifications/containers/SpecificationsList.tsx`, `src/libs/workspaces/src/routes/combinations/containers/WorkspaceCombinations.tsx` |
| 🔍 Query | `GET_TEAMS` | 6 files |
| 🔍 Query | `GET_WORKSPACES_BY_IDS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/CombinationWorkspaceCard.tsx` |
| 🔍 Query | `GET_WORKSPACE_COMBINATIONS_SAMPLES` | `src/libs/samples/index.ts`, `src/libs/samples/src/containers/workspace/SampleBulkUpdate.tsx`, `src/libs/samples/src/graphql/workspace/SampleBulkEvaluateQueries.tsx`, `src/libs/spark-combination-graphql/index.ts`, `src/libs/workspaces/src/routes/combinations/containers/WorkspaceCombinations.tsx` |
| 🔍 Query | `REFRESH_PARTNERS` | 6 files |
| 🔍 Query | `REFRESH_TEAMS` | 6 files |
| 🔍 Query | `SEARCH_COMBINATIONS` | 5 files |
| 🔍 Query | `SEARCH_COMBINATION_SUGGESTIONS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/containers/CombinationList.tsx` |
| 🔍 Query | `SEARCH_MORE_MATERIALS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentBucket.tsx` |
| 🔍 Query | `SEARCH_MORE_MATERIALS_PROXY` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/ImpressionIntentBucket.tsx` |
| 🔍 Query | `SEARCH_SPECIFICATIONS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination/src/components/FabricSpecificationAutocomplete.tsx` |
| 🔍 Query | `SEARCH_SUGGESTIONS` | `src/libs/samples/src/containers/combination/CombinationSamplesList.tsx`, `src/libs/spark-combination-graphql/index.ts` |
| 🔍 Query | `SEARCH_TEAMS` | 11 files |

---

## Common Components

**6 definitions** — 6 queries

### `src/libs/spark-common-components/src/favorites/graphql/favoriteQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_FAVORITES_COMBINATIONS` | 5 files |
| 🔍 Query | `GET_FAVORITES_MATERIAL` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/containers/graphql/SidebarQueries.ts` |
| 🔍 Query | `GET_FAVORITES_PALETTE` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/containers/graphql/SidebarQueries.ts` |
| 🔍 Query | `GET_FAVORITES_PRODUCTS` | 5 files |
| 🔍 Query | `GET_FAVORITES_TEAMS` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/containers/graphql/SidebarQueries.ts` |
| 🔍 Query | `GET_FAVORITES_WORKSPACES` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx`, `src/libs/spark-legacy/containers/graphql/SidebarQueries.ts` |

---

## Fabric

**7 definitions** — 3 queries, 2 mutations, 2 fragments

### `src/libs/spark-fabric-graphql/src/FabricCostQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `FABRIC_COSTING_FRAGMENT` | `src/libs/spark-fabric-graphql/index.ts` |
| 🧩 Fragment | `FABRIC_COSTING_FRAGMENT_MINI` | `src/libs/spark-fabric-graphql/index.ts` |
| ✏️ Mutation | `ADD_FABRIC_COSTING` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/cost/containers/FabricCostingNew.tsx` |
| ✏️ Mutation | `UPDATE_FABRIC_COSTING` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/cost/containers/FabricCostingEdit.tsx` |
| 🔍 Query | `FABRIC_COSTINGS_SEARCH_QUERY` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/cost/containers/CostList.tsx` |
| 🔍 Query | `FABRIC_COSTING_BY_ID` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/cost/containers/FabricCostingEdit.tsx` |
| 🔍 Query | `GET_ALL_COSTING` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/cost/components/FabricCostingRecordDetails.tsx` |

---

## Insights

**113 definitions** — 7 queries, 6 mutations, 100 fragments

### `src/libs/spark-insights/src/util/InsightsQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `ACCREDITED_BP_PERFORMANCE` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedBPPerformance.tsx` |
| 🧩 Fragment | `ACCREDITED_DEPTH_OF_BP_USERS_FRAGMENT` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedBPDepthInfoCard.tsx` |
| 🧩 Fragment | `ACCREDITED_EVALUATION_TRENDS` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedEvaluationTrends.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `ACCREDITED_PARTNERS_COUNT` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedInformationCard.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `ACCREDITED_PARTNERS_EVALUATIONS` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedInformationCard.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `ACCREDITED_SCOPE_OF_BP_USERS` | `src/libs/spark-insights/src/components/accreditedPartners/AccreditedTotalBPCard.tsx` |
| 🧩 Fragment | `ACTIVE_CLAIMS_FRAGMENT` | `src/libs/spark-insights/src/containers/claims/ClaimsBody.tsx` |
| 🧩 Fragment | `APPROVAL_BY_ROUND_FRAGMENT` | `src/libs/spark-insights/src/containers/threeD/index.tsx`, `src/libs/spark-insights/src/containers/workload/WorkloadTemplate.tsx` |
| 🧩 Fragment | `AVERAGE_CLAIMS_FRAGMENT` | `src/libs/spark-insights/src/containers/claims/ClaimsBody.tsx` |
| 🧩 Fragment | `BP_CATEGORY_VIEW_3D` | `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/CategoryView.tsx`, `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/index.tsx` |
| 🧩 Fragment | `BP_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `BP_PRODUCTS_3D` | `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/BPView.tsx`, `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/CategoryView.tsx` |
| 🧩 Fragment | `BP_VIEW_3D` | `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/BPView.tsx`, `src/libs/spark-insights/src/components/threeD/businessPartnerCard3D/index.tsx` |
| 🧩 Fragment | `BRAND_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `CLAIMS_HEIRARCHY` | `src/libs/spark-insights/src/components/claims/ClaimsHierarchyCard.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `CLASS_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `COMMUNICATING_CHANNEL_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `CONNECTED_BOM_ALL_CYCLES_BP_TABLE` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMBPCard.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_BP_PERFORMANCE` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMBPPerformance.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_BP_PRODUCT` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMBPCard.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_BP_TABLE` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMBPCard.tsx`, `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMCard.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_BY_GROUP_N` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMCard.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_DEPTH_MATERIAL_TYPE_FRAGMENT` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMDepthByMaterialTypeBP.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_FRAGMENT` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMCard.tsx` |
| 🧩 Fragment | `CONNECTED_BOM_PRODUCTS` | _not referenced_ |
| 🧩 Fragment | `CONNECTED_COMPLETED_BOM` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMCard.tsx` |
| 🧩 Fragment | `CONNECTED_PRODUCTS_NO_ACTIVE_BOM` | `src/libs/spark-insights/src/components/connectedBOM/ConnectedBOMBPCard.tsx` |
| 🧩 Fragment | `DEPARTMENT_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `DESIGN_CYCLE_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `DIGITAL_TWIN_SAMPLE_METRICS` | `src/libs/spark-insights/src/components/threeD/DigitalTwinSampleMetrics.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `DIVISION_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `DUE_DATES_FABRIC_FRAGMENT` | `src/libs/spark-insights/src/components/samples/material/Fabric/SamplesUpcomingDueDatesFabric.tsx` |
| 🧩 Fragment | `DUE_DATES_FRAGMENT` | `src/libs/spark-insights/src/components/samples/material/Combo/SamplesUpcomingDueDatesCombo.tsx`, `src/libs/spark-insights/src/components/samples/material/Wash/SamplesUpcomingDueDatesWash.tsx`, `src/libs/spark-insights/src/components/samples/product/UpcomingDueDates.tsx` |
| 🧩 Fragment | `EVALUATION_FRAGMENT` | `src/libs/spark-insights/src/components/samples/product/Evaluations.tsx`, `src/libs/spark-insights/src/components/threeD/Evaluations3D.tsx` |
| 🧩 Fragment | `FABRIC_ADOPTION_RATE_FRAGMENT` | `src/libs/spark-insights/src/containers/fabricDevelopment/FabricDevelopmentTemplate.tsx` |
| 🧩 Fragment | `FABRIC_DEVELOPMENT_BY_ENGINEER` | `src/libs/spark-insights/src/components/fabricDevelopment/fabric/FabricDevByEngineer.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `FABRIC_DEVELOPMENT_BY_ENGINEER_BRAND` | `src/libs/spark-insights/src/components/fabricDevelopment/fabric/FabricDevByEngineerAndBrand.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `FABRIC_DEVELOPMENT_BY_ENGINEER_BRAND_AND_REASON` | `src/libs/spark-insights/src/components/fabricDevelopment/fabric/FabricDevByBrandAndReason.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `FABRIC_DEVELOPMENT_BY_ROLE` | `src/libs/spark-insights/src/components/fabricDevelopment/fabric/FabricDevByRole.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `FABRIC_DEV_RATIO_FRAGMENT` | `src/libs/spark-insights/src/containers/fabricDevelopment/FabricDevelopmentTemplate.tsx` |
| 🧩 Fragment | `FREQUENTLY_USED_CLAIMS` | `src/libs/spark-insights/src/components/claims/FrequentlyUsed.tsx` |
| 🧩 Fragment | `FREQUENTLY_USED_CLAIMS_BY_PID` | `src/libs/spark-insights/src/components/claims/FrequentlyUsed.tsx` |
| 🧩 Fragment | `HEALTH_CHECK_FRAGMENT` | `src/libs/spark-insights/src/components/healthCheck/ComponentAdoptionBarChart.tsx` |
| 🧩 Fragment | `MATERIAL_BRAND_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `MATERIAL_DEPARTMENT_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `MATERIAL_DESIGN_CYCLE_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `MATERIAL_DIVISION_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `MATERIAL_EVALUATION_FRAGMENT` | `src/libs/spark-insights/src/components/samples/material/Combo/SamplesEvaluationsCombo.tsx`, `src/libs/spark-insights/src/components/samples/material/Fabric/SamplesEvaluationsFabric.tsx`, `src/libs/spark-insights/src/components/samples/material/Wash/SamplesEvaluationsWash.tsx` |
| 🧩 Fragment | `PACKAGING_BOM_PRODUCTS` | `src/libs/spark-insights/src/components/connectedBOM/PackagingBOM/PackagingBOMBPCard.tsx` |
| 🧩 Fragment | `PACKAGING_COPY_DUE_DATES` | `src/libs/spark-insights/src/components/packaging/copy/PackagingWithCopyHeader.tsx` |
| 🧩 Fragment | `PACKAGING_COPY_SPECS` | `src/libs/spark-insights/src/components/packaging/copy/PackagingWithCopyHeader.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PACKAGING_COPY_WORKSPACE` | `src/libs/spark-insights/src/components/packaging/copy/PackagingWithCopyTable.tsx` |
| 🧩 Fragment | `PACKAGING_DIELINE_DUE_DATES` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineProducts.tsx` |
| 🧩 Fragment | `PACKAGING_DIELINE_EVALUATIONS` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineEvaluations.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PACKAGING_DIELINE_EVALUATORS` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineRequests.tsx` |
| 🧩 Fragment | `PACKAGING_DIELINE_PRODUCTS` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineProducts.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PACKAGING_DIELINE_REQUESTS` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineRequestSections.tsx`, `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineRequests.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PACKAGING_DIGITAL_BOM` | `src/libs/spark-insights/src/components/connectedBOM/PackagingBOM/PackagingBOMBPCard.tsx`, `src/libs/spark-insights/src/components/connectedBOM/PackagingBOM/PackagingBOMCard.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PACKAGING_DIGITAL_BOM_BP` | `src/libs/spark-insights/src/components/connectedBOM/PackagingBOM/PackagingBOMBPCard.tsx` |
| 🧩 Fragment | `PACKAGING_PRODUCTS_NO_ACTIVE_BOM` | _not referenced_ |
| 🧩 Fragment | `PACKAGING_PRODUCT_INFO` | `src/libs/spark-insights/src/components/packaging/dielines/PackagingDielineRequestSections.tsx` |
| 🧩 Fragment | `PARTNER_PERFORMANCE_CLAIMS` | `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PAST_DUE_DATES_FABRIC` | `src/libs/spark-insights/src/components/samples/material/Fabric/SamplesPastDueDatesFabric.tsx` |
| 🧩 Fragment | `PAST_DUE_DATES_WITH_BP` | `src/libs/spark-insights/src/components/samples/material/Combo/SamplesPastDueDatesCombo.tsx`, `src/libs/spark-insights/src/components/samples/material/Wash/SamplesPastDueDatesWash.tsx`, `src/libs/spark-insights/src/components/samples/product/PastDueDates.tsx` |
| 🧩 Fragment | `PERCENTAGE_CLAIMS_FRAGMENT` | `src/libs/spark-insights/src/containers/claims/ClaimsBody.tsx` |
| 🧩 Fragment | `PHOTO_VIDEO_APPROVAL_BY_ROUND_FRAGMENT` | `src/libs/spark-insights/src/containers/workload/WorkloadTemplate.tsx` |
| 🧩 Fragment | `PHYSICAL_APPROVAL_BY_ROUND_FRAGMENT` | `src/libs/spark-insights/src/containers/workload/WorkloadTemplate.tsx` |
| 🧩 Fragment | `PROCESS_ADHERENCE_3D` | `src/libs/spark-insights/src/components/threeD/ProcessAdherence.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `PRODUCT_SAMPLE_FORMAT_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `PRODUCT_SAMPLE_TYPE_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `PYRAMID_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `SAMPLE_APPROVAL_BY_ROUND` | `src/libs/spark-insights/src/components/workload/WorkloadSampleRounds.tsx` |
| 🧩 Fragment | `SAMPLE_APPROVAL_ROUND` | `src/libs/spark-insights/src/components/samples/material/SamplesApprovalByRound.tsx` |
| 🧩 Fragment | `SAMPLE_EVALUATED_BY_USER` | `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `SAMPLE_RATIO_3D` | `src/libs/spark-insights/src/components/threeD/SampleRatioCard.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `SAMPLE_SAVINGS_3D` | `src/libs/spark-insights/src/components/threeD/SampleSavingsCard.tsx` |
| 🧩 Fragment | `SAMPLE_TRACKING_FRAGMENT` | 4 files |
| 🧩 Fragment | `SAMPLE_TYPE_EVALUATED_BY_USER` | _not referenced_ |
| 🧩 Fragment | `SAMPLE_TYPE_FRAGMENT` | `src/libs/spark-insights/src/components/samples/product/SampleTypes.tsx` |
| 🧩 Fragment | `SUBSTANTIATED_CLAIMS_FRAGMENT` | `src/libs/spark-insights/src/containers/claims/ClaimsBody.tsx` |
| 🧩 Fragment | `SUPPLIER_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| 🧩 Fragment | `TOTAL_CLAIMS` | `src/libs/spark-insights/src/components/claims/TotalClaimsPerDesignCycle.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `TREND_FRAGMENT` | `src/libs/spark-insights/src/components/samples/product/Trends.tsx` |
| 🧩 Fragment | `UTILIZATION_3D` | `src/libs/spark-insights/src/components/threeD/Utilization.tsx`, `src/libs/spark-insights/src/containers/threeD/index.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `UTILIZATION_3D_TREND` | `src/libs/spark-insights/src/components/threeD/UtilizationTrend.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WASH_TREND_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `WORKLOAD_PRODUCT_COUNT_AND_DEV_RATIO` | `src/libs/spark-insights/src/components/workload/workloadProductCount/header.tsx`, `src/libs/spark-insights/src/components/workload/workloadProductCount/index.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_PRODUCT_COUNT_AND_DEV_RATIO_BP_AVERAGE` | `src/libs/spark-insights/src/components/workload/workloadProductCount/index.tsx` |
| 🧩 Fragment | `WORKLOAD_PRODUCT_SAMPLE_TO_RATIO` | `src/libs/spark-insights/src/components/workload/WorkloadSampleProductRatio.tsx` |
| 🧩 Fragment | `WORKLOAD_PRODUCT_STATUS` | `src/libs/spark-insights/src/components/workload/WorkloadStatus.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_ASSIGNED_BY_PURPOSE` | `src/libs/spark-insights/src/containers/workload/WorkloadTemplate.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_ASSIGNED_BY_USER` | `src/libs/spark-insights/src/components/workload/WorkloadSampleAssignedByUser.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_ASSIGNED_BY_USER_AND_FORMAT` | `src/libs/spark-insights/src/components/workload/WorkloadSampleAssignedByUserAndFormat.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_REQUEST_BY_ROLE_FORMAT` | `src/libs/spark-insights/src/components/workload/WorkloadSampleRequestedByRoleAndFormat.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_REQUEST_BY_TYPE_PURPOSE` | `src/libs/spark-insights/src/containers/workload/WorkloadTemplate.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_REQUEST_BY_USER` | `src/libs/spark-insights/src/components/workload/WorkloadRequestedByUser.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_TYPES_BY_PURPOSE` | `src/libs/spark-insights/src/components/workload/WorkloadPurpose.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_TYPES_BY_ROLE` | `src/libs/spark-insights/src/components/workload/WorkloadByRole.tsx`, `src/libs/spark-insights/src/util/Constants.tsx` |
| 🧩 Fragment | `WORKLOAD_SAMPLE_TYPES_BY_USERS` | `src/libs/spark-insights/src/components/workload/WorkloadByUser.tsx` |
| 🧩 Fragment | `WORKSPACE_FILTER_FRAGMENT` | `src/libs/spark-insights/src/util/FiltersUtil.tsx` |
| ✏️ Mutation | `ADD_BYO_TEMPLATES` | `src/libs/spark-insights/src/containers/byo/BYOSetupData.tsx` |
| ✏️ Mutation | `CREATE_EXPORT_REQUEST` | 6 files |
| ✏️ Mutation | `DELETE_BYO_TEMPLATES` | `src/libs/spark-insights/src/containers/byo/BYOLandingTemplate.tsx` |
| ✏️ Mutation | `SET_USER_SETTINGS` | 11 files |
| ✏️ Mutation | `SHARE_BYO_TEMPLATES` | `src/libs/spark-insights/src/containers/byo/BYOLandingTemplate.tsx` |
| ✏️ Mutation | `UPDATE_BYO_TEMPLATES` | `src/libs/spark-insights/src/containers/byo/BYOEditTemplate.tsx`, `src/libs/spark-insights/src/containers/byo/BYOInsightsGrid.tsx` |
| 🔍 Query | `DEV_RATIO_ADOPTION_CARD` | _not referenced_ |
| 🔍 Query | `GET_BUSINESS_PARTNERS_BY_IDS` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/specifications/components/FabricSpecificationForm.tsx`, `src/libs/spark-wash-graphql/index.ts` |
| 🔍 Query | `GET_BYO_FRAGMENT` | `src/libs/spark-insights/src/containers/byo/BYOTemplate.tsx` |
| 🔍 Query | `GET_BYO_TEMPLATES` | `src/libs/spark-insights/src/components/byo/BYOLandingForm.tsx` |
| 🔍 Query | `GET_BYO_TEMPLATE_BY_ID` | `src/libs/spark-insights/src/containers/byo/BYOEditTemplate.tsx`, `src/libs/spark-insights/src/containers/byo/BYOReportTemplate.tsx` |
| 🔍 Query | `GET_REQUESTED_SAMPLE_BY_USER` | `src/libs/spark-insights/src/util/Constants.tsx` |
| 🔍 Query | `GET_USER_SETTINGS` | 15 files |

---

## Legacy (Spark)

**176 definitions** — 120 queries, 40 mutations, 16 fragments

### `src/libs/spark-legacy/Spark-Components/graphql/ComponentHistoryQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_COMPONENT_HISTORY` | 8 files |

### `src/libs/spark-legacy/Spark-Components/graphql/SearchFilesModalQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `SEARCH_ATTACHMENTS` | 17 files |

### `src/libs/spark-legacy/Spark-Components/graphql/sparkComponentsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_PRODUCT_SEARCH` | `src/libs/spark-legacy/Spark-Components/ProductSearchAutocomplete.tsx` |

### `src/libs/spark-legacy/actions/graphql/actionsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_USER` | `src/libs/spark-mock-data-builders/src/builders/bom.ts` |
| 🔍 Query | `GET_USERS` | 9 files |

### `src/libs/spark-legacy/components/attachments/graphql/ComponentAttachmentsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `PUBLISH_ATTACHMENT_TO_GALLERY` | `src/libs/product-common/src/components/files/use3DFileUtils.ts`, `src/libs/spark-legacy/components/ShareToGalleryButton.tsx`, `src/libs/spark-legacy/components/graphql/ComponentsMutations.ts` |
| ✏️ Mutation | `UNPUBLISH_ATTACHMENT_TO_GALLERY` | `src/libs/product-common/src/components/files/use3DFileUtils.ts`, `src/libs/spark-legacy/components/ShareToGalleryButton.tsx`, `src/libs/spark-legacy/components/graphql/ComponentsMutations.ts` |
| ✏️ Mutation | `UPDATE_ATTACHMENT_MARK_3D_FINAL` | `src/libs/core-file-management/src/OrganizationAndFindability/OrganizationAndFindability.tsx`, `src/libs/core-file-management/src/OrganizationAndFindability/graphql/coreFileManagementQueries.ts`, `src/libs/product-common/src/components/files/use3DFileUtils.ts` |

### `src/libs/spark-legacy/components/breadcrumbs/graphql/BreadcrumbQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_ARTWORK_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbArtwork.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbArtwork.tsx` |
| 🔍 Query | `GET_CLAIM_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbClaim.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbClaim.tsx` |
| 🔍 Query | `GET_COLOR_ARCHROMA_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbArchroma.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbArchroma.tsx` |
| 🔍 Query | `GET_COLOR_COLORO_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbColoro.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbColoro.tsx` |
| 🔍 Query | `GET_COLOR_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbColor.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbColor.tsx` |
| 🔍 Query | `GET_COLOR_PANTONE_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbPantone.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbPantone.tsx` |
| 🔍 Query | `GET_PALETTE_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbPalette.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbPalette.tsx` |
| 🔍 Query | `GET_PRODUCT_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbProduct.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbProduct.tsx` |
| 🔍 Query | `GET_SAMPLE` | `src/libs/samples/index.ts`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbSample.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbSample.tsx` |
| 🔍 Query | `GET_TAG_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbTag.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbTag.tsx` |
| 🔍 Query | `GET_TEAM_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbTeam.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbTeam.tsx` |
| 🔍 Query | `GET_USER_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbUser.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbUser.tsx` |
| 🔍 Query | `GET_WASH_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbWash.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbWash.tsx` |
| 🔍 Query | `GET_WORKSPACE_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbWorkspace.test.tsx`, `src/libs/spark-legacy/components/breadcrumbs/molecules/BreadcrumbWorkspace.tsx` |

### `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_FAVORITE` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/graphql/FavoriteQueries.ts`, `src/libs/core-favorites/src/mocks/index.ts`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| ✏️ Mutation | `DELETE_FAVORITE` | `src/libs/core-favorites/src/atoms/FavoriteButton.tsx`, `src/libs/core-favorites/src/graphql/FavoriteQueries.ts`, `src/libs/core-favorites/src/mocks/index.ts`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| ✏️ Mutation | `TOGGLE_VIEW_SWITCH` | `src/libs/spark-legacy/components/connectedComponents/ToggleViewFilter.tsx` |
| ✏️ Mutation | `UPDATE_USER_ACCREDITATION` | _not referenced_ |

### `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `DEPARTMENT_FRAGMENT` | _not referenced_ |
| 🔍 Query | `GET_BRANDS` | `src/libs/spark-legacy/components/connectedComponents/BrandsAutocomplete.tsx`, `src/libs/spark-materials/src/components/core-filter-extensions/CoreBrandsFilter.tsx` |
| 🔍 Query | `GET_BUSINESS_PARTNERS_BY_TYPE` | `src/libs/bill-of-materials/src/components/materialsAdvancedSearch/__tests__/BomMaterialAdvancedSearchModal-RTL.test.tsx`, `src/libs/spark-materials/src/components/core-filter-extensions/CoreMaterialSupplierFilter.tsx` |
| 🔍 Query | `GET_CAPACITY_TYPES` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts`, `src/libs/spark-legacy/customHooks/useCapacityTypes.ts` |
| 🔍 Query | `GET_CLAZZES_BY_MULTIPLE_DEPARTMENTS` | `src/libs/spark-legacy/components/connectedComponents/ClassesAutocomplete.tsx` |
| 🔍 Query | `GET_DEPARTMENTS` | `src/libs/spark-legacy/components/connectedComponents/DepartmentsAutocomplete.tsx` |
| 🔍 Query | `GET_DEPARTMENTS_BY_DIVISION` | `src/libs/spark-legacy/components/connectedComponents/DepartmentsAutocomplete.tsx` |
| 🔍 Query | `GET_DIVISIONS` | `src/libs/spark-artwork/src/components/ArtworkForm.tsx`, `src/libs/spark-legacy/components/connectedComponents/DivisionsAutocomplete.tsx`, `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials-graphql/src/graphql/materialsQueries.ts` |
| 🔍 Query | `GET_FABRIC_SUPPLIERS` | 4 files |
| 🔍 Query | `GET_MERCH_TYPES_BY_DEPARTMENT_ID` | _not referenced_ |
| 🔍 Query | `GET_MERCH_VENDORS` | `src/libs/spark-wash-graphql/index.ts` |
| 🔍 Query | `GET_PRODUCT_STATUS` | _not referenced_ |
| 🔍 Query | `GET_RECENTLY_VIEWED_PRODUCTS` | `src/libs/spark-legacy/components/connectedComponents/ProductsOverviewCard.tsx` |
| 🔍 Query | `GET_TAGS_BY_TYPE_W_LABEL` | _not referenced_ |
| 🔍 Query | `GET_TRIM_SUPPLIERS` | `src/libs/spark-trim-graphql/index.ts`, `src/libs/spark-trim/src/routes/suppliers/TrimSuppliers.tsx`, `src/libs/spark-trim/src/utils/TrimHelperFunctions.tsx` |
| 🔍 Query | `GET_USER_ACCREDITATION` | 5 files |

### `src/libs/spark-legacy/components/graphql/ComponentsFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `ARTWORK_TEAM_FIELDS` | _not referenced_ |
| 🧩 Fragment | `BUSINESS_PARTNER_FIELDS` | _not referenced_ |
| 🧩 Fragment | `COMBINATION_TEAM_FIELDS` | `src/libs/spark-combination-graphql/src/CombinationsFragments.ts`, `src/libs/spark-combination-graphql/src/CombinationsQueries.ts` |
| 🧩 Fragment | `FILE_FIELDS` | `src/libs/spark-combination-graphql/src/CombinationsFragments.ts`, `src/libs/spark-materials-hub-graphql/src/BaseMaterialQueries.ts`, `src/libs/spark-materials-hub-graphql/src/PaperQueries.ts`, `src/libs/spark-materials-hub-graphql/src/WoodQueries.ts` |
| 🧩 Fragment | `PALETTE_TEAM_FIELDS` | `src/libs/spark-palette-graphql/src/PaletteQueries.ts` |
| 🧩 Fragment | `TRIM_TEAM_FIELDS` | _not referenced_ |
| 🧩 Fragment | `WASH_TEAM_FIELDS` | _not referenced_ |

### `src/libs/spark-legacy/components/graphql/ComponentsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_TODO` | `src/libs/spark-legacy/components/AddToDoModal.tsx` |
| ✏️ Mutation | `ADD_USER_SETTINGS` | `src/libs/spark-legacy/components/connectedComponents/UserSettingsSection.tsx` |
| ✏️ Mutation | `ARCHIVE_ATTACHMENT` | 11 files |
| ✏️ Mutation | `CREATE_USER_VIEW` | `src/libs/product-specs-common/src/components/grid/ViewsToolPanel.tsx` |
| ✏️ Mutation | `MANAGE_USER_VIEWS` | `src/libs/product-specs-common/src/components/grid/SelectViewsPanel.tsx` |
| ✏️ Mutation | `PUBLISH_ATTACHMENT_TO_GALLERY` | `src/libs/product-common/src/components/files/use3DFileUtils.ts`, `src/libs/spark-legacy/components/ShareToGalleryButton.tsx`, `src/libs/spark-legacy/components/attachments/graphql/ComponentAttachmentsMutations.ts` |
| ✏️ Mutation | `UNPUBLISH_ATTACHMENT_TO_GALLERY` | `src/libs/product-common/src/components/files/use3DFileUtils.ts`, `src/libs/spark-legacy/components/ShareToGalleryButton.tsx`, `src/libs/spark-legacy/components/attachments/graphql/ComponentAttachmentsMutations.ts` |
| ✏️ Mutation | `UPDATE_DEFAULT_PARTNER_ATTRIBUTES` | _not referenced_ |
| ✏️ Mutation | `UPDATE_USER_ATTRIBUTES` | `src/libs/spark-legacy/components/UserProfileNotificationSettings.tsx`, `src/libs/spark-legacy/components/connectedComponents/UserProfileHeader.tsx`, `src/libs/spark-legacy/components/connectedComponents/ViewUserProfileOptedAttributes.tsx` |
| ✏️ Mutation | `UPDATE_USER_VIEW` | `src/libs/product-specs-common/src/components/grid/ViewsToolPanel.tsx` |
| 🔍 Query | `GET_USERS` | 9 files |

### `src/libs/spark-legacy/components/graphql/ComponentsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `COMPONENT_ATTACHMENT_DETAILS_FRAGMENT` | _not referenced_ |
| 🔍 Query | `GET_ACCREDITATION_TYPES` | 5 files |
| 🔍 Query | `GET_FILE` | `src/libs/spark-legacy/components/ImageComponent.tsx`, `src/libs/spark-mock-data-builders/src/builders/base.ts` |
| 🔍 Query | `GET_IMPRESSION_INTENTS` | `src/libs/spark-combination-graphql/index.ts`, `src/libs/spark-combination-graphql/src/CombinationsQueries.ts`, `src/libs/spark-combination/src/components/AddImpressionIntentModal.tsx`, `src/libs/spark-legacy/components/ImpressionIntentFormSection.tsx` |
| 🔍 Query | `GET_ROLES` | 6 files |
| 🔍 Query | `GET_ROLES_W_LABEL` | _not referenced_ |
| 🔍 Query | `GET_USERS` | 9 files |
| 🔍 Query | `GET_USERS_LIST` | `src/libs/product-packaging/src/helpers/fetchInternalUsers.ts`, `src/libs/spark-legacy/admin/Impersonation.tsx`, `src/libs/spark-legacy/routes/users/containers/UsersList.tsx`, `src/libs/spark-legacy/routes/users/graphql/usersQueries.ts` |
| 🔍 Query | `GET_USER_VIEWS` | `src/libs/product-specs-common/src/components/grid/SelectViewsPanel.tsx`, `src/libs/product-specs-common/src/components/grid/ViewsToolPanel.tsx` |
| 🔍 Query | `GET_VMM_PARTNER` | `src/libs/spark-legacy/components/PartnerTypes.tsx` |
| 🔍 Query | `SEARCH_ATTACHMENTS_TAGS` | _not referenced_ |
| 🔍 Query | `SEARCH_MATERIALS_V2` | `src/libs/spark-legacy/components/materials/MaterialsAutocomplete.tsx` |
| 🔍 Query | `USER_PROFILE` | `src/libs/spark-legacy/components/UserProfileNotificationSettings.tsx`, `src/libs/spark-legacy/components/connectedComponents/UserProfileHeader.tsx` |

### `src/libs/spark-legacy/containers/access/withAccessCheckWrapperQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `RESOURCE_ACCESS_CHECK` | `src/libs/spark-legacy/containers/access/withAccessCheckWrapper.tsx` |

### `src/libs/spark-legacy/containers/graphql/ContainersQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `POWER_SEARCH` | `src/libs/spark-legacy/containers/Layout/PowerTools/PowerSearch.tsx` |

### `src/libs/spark-legacy/containers/graphql/SidebarQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `UPDATE_FAVORITES_ORDER` | _not referenced_ |
| 🔍 Query | `GET_FAVORITES_ARTWORKS` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_COLORS` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_COLORS_ARCHROMA` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_COLORS_COLORO` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_COLORS_PANTONE` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_COMBINATIONS` | 5 files |
| 🔍 Query | `GET_FAVORITES_FABRICS` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_FABRIC_SPECIFICATIONS` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_MATERIAL` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/graphql/favoriteQueries.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_PALETTE` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/graphql/favoriteQueries.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_PRODUCTS` | 5 files |
| 🔍 Query | `GET_FAVORITES_TEAMS` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/graphql/favoriteQueries.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_TRIMS` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_WASH` | `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |
| 🔍 Query | `GET_FAVORITES_WORKSPACES` | `src/libs/spark-common-components/index.ts`, `src/libs/spark-common-components/src/favorites/graphql/favoriteQueries.ts`, `src/libs/spark-common-components/src/favorites/sparkFavoriteConfig.tsx`, `src/libs/spark-legacy/components/connectedComponents/Favorite.tsx` |

### `src/libs/spark-legacy/customHooks/graphql/customHooksMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_ACCESS_CONTROL_PERMISSION` | `src/libs/spark-legacy/customHooks/useUpdateResourceACLGroups.tsx` |
| ✏️ Mutation | `DELETE_ACCESS_CONTROL_PERMISSION` | `src/libs/spark-legacy/customHooks/useUpdateResourceACLGroups.tsx` |

### `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_BOM_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.test.tsx`, `src/libs/product-common/src/customHooks/useComponentStatus.ts`, `src/libs/spark-mock-data-builders/src/builders/bom.ts` |
| 🔍 Query | `GET_CAPACITY_TYPES` | `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsQueries.ts`, `src/libs/spark-legacy/customHooks/useCapacityTypes.ts` |
| 🔍 Query | `GET_CLAIM_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.ts` |
| 🔍 Query | `GET_MEASUREMENT_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.test.tsx`, `src/libs/product-common/src/customHooks/useComponentStatus.ts` |
| 🔍 Query | `GET_PACKAGING_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.test.tsx`, `src/libs/product-common/src/customHooks/useComponentStatus.ts` |
| 🔍 Query | `GET_PERMISSIONS` | `src/libs/spark-legacy/customHooks/useUpdateResourceACLGroups.tsx`, `src/libs/spark-legacy/routes/teams/components/TeamManagePermissionsModal.tsx`, `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` |
| 🔍 Query | `GET_PROUCT_DETAIL_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.ts` |
| 🔍 Query | `GET_VERSIONED_COMPONENT_STATUS` | `src/libs/product-common/src/customHooks/useComponentStatus.test.tsx`, `src/libs/product-common/src/customHooks/useComponentStatus.ts`, `src/libs/spark-mock-data-builders/src/builders/bom.ts` |

### `src/libs/spark-legacy/routes/admin/routes/accessGroup/graphql/AccessGroupQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `UPDATE_ACCESS_CONTROL_GROUPS` | `src/libs/spark-legacy/routes/admin/routes/accessGroup/components/AccessGroupListBody.tsx` |
| 🔍 Query | `GET_USER_ACESS_GROUPS` | `src/libs/spark-legacy/routes/admin/routes/accessGroup/components/AccessGroupListBody.tsx`, `src/libs/spark-legacy/routes/admin/routes/accessGroup/containers/AccessGroupList.tsx` |

### `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PRODUCT_RULES_FIELDS_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `ADD_PRODUCT_RULE` | _not referenced_ |
| ✏️ Mutation | `DELETE_PRODUCT_RULE` | _not referenced_ |
| ✏️ Mutation | `UPDATE_PRODUCT_RULE` | _not referenced_ |
| 🔍 Query | `GET_ALL_AVAILABLE_RULES` | _not referenced_ |
| 🔍 Query | `GET_BUSINESS_PARTNERS` | `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/specifications/components/FabricSpecificationForm.tsx`, `src/libs/spark-legacy/routes/admin/routes/rules/helpers/BusinessPartnerAutocomplete.tsx` |
| 🔍 Query | `GET_PRODUCT_BUSINESS_PARTNER_RULES` | _not referenced_ |
| 🔍 Query | `GET_PRODUCT_DEPARTMENT_RULES` | _not referenced_ |
| 🔍 Query | `GET_RULE` | _not referenced_ |
| 🔍 Query | `GET_RULES` | _not referenced_ |
| 🔍 Query | `GET_SEARCH_PRODUCT_DEPARTMENT_RULES` | `src/libs/spark-legacy/customHooks/useSearchProductRules.tsx` |

### `src/libs/spark-legacy/routes/admin/routes/tags/graphql/AdminTagsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `CREATE_TAG` | _not referenced_ |
| ✏️ Mutation | `UPDATE_TAG` | _not referenced_ |

### `src/libs/spark-legacy/routes/admin/routes/tags/graphql/AdminTagsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_TAG` | _not referenced_ |
| 🔍 Query | `GET_TAG_TYPES` | _not referenced_ |

### `src/libs/spark-legacy/routes/admin/routes/vendorMerge/graphql/VendorMergeQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `VENDOR_MERGE_TEAMS_INFO` | _not referenced_ |
| ✏️ Mutation | `VENDOR_MERGE` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/containers/VendorMergeNew.tsx` |
| 🔍 Query | `GET_VENDOR_MERGE_STATUS_DATA` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/components/VendorMergeInfo.tsx` |
| 🔍 Query | `GET_VENDOR_MERGE_STATUS_LIST` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/components/VendorMergeListView.tsx` |
| 🔍 Query | `PID_AND_WRK_ID_SEARCH` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/components/PIDOrWRKIDSelectAutoComplete.tsx` |
| 🔍 Query | `SEARCH_BUSINESS_PARTNERS` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/components/BPSelectAutoComplete.tsx`, `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` |
| 🔍 Query | `SEARCH_TEAMS` | 11 files |

### `src/libs/spark-legacy/routes/dashboard/graphql/dashboardFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `UNION_FRAGMENT` | `src/libs/spark-legacy/routes/dashboard/graphql/dashboardQueries.ts` |

### `src/libs/spark-legacy/routes/dashboard/graphql/dashboardMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `DELETE_TODO` | _not referenced_ |
| ✏️ Mutation | `UPDATE_NOTIFICATION` | _not referenced_ |
| ✏️ Mutation | `UPDATE_NOTIFICATION_GROUPS` | `src/libs/spark-legacy/routes/inbox/containers/template/InboxTemplate.tsx` |

### `src/libs/spark-legacy/routes/dashboard/graphql/dashboardQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_INBOX_NOTIFICATIONS_COUNT` | _not referenced_ |
| 🔍 Query | `GET_NOTIFICATIONS` | _not referenced_ |
| 🔍 Query | `GET_NOTIFICATION_GROUPS` | `src/libs/spark-legacy/routes/inbox/containers/template/InboxTemplate.tsx` |
| 🔍 Query | `GET_NOTIFICATION_GROUP_STATS` | `src/libs/spark-legacy/routes/inbox/components/wip/InboxFilter.tsx` |
| 🔍 Query | `GET_TODOS` | `src/libs/spark-legacy/components/AddToDoModal.tsx` |

### `src/libs/spark-legacy/routes/resourceRedirect/config/samples.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `RESOURCE_REDIRECT_SLIM_GET_FABRIC_SPECIFICATION_BY_ID` | _not referenced_ |
| 🔍 Query | `RESOURCE_REDIRECT_SLIM_GET_FABRIC_SPEC_COMBO_BY_ID` | _not referenced_ |
| 🔍 Query | `RESOURCE_REDIRECT_SLIM_GET_SAMPLE_BY_ID` | _not referenced_ |

### `src/libs/spark-legacy/routes/resourceRedirect/graphql/resourceRedirectQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `RESOURCE_REDIRECT_SLIM_GET_DISCUSSION_BY_ID` | `src/libs/spark-legacy/routes/resourceRedirect/config/discussion.tsx` |

### `src/libs/spark-legacy/routes/rfid/graphql/rdifQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `SEARCH_RFID_LOCATIONS` | `src/libs/samples/src/organisms/SampleTrackingReadOnly.tsx`, `src/libs/spark-legacy/routes/rfid/components/RfidPage.tsx`, `src/libs/spark-legacy/routes/rfid/testUtils/testUtil.ts` |
| 🔍 Query | `SEARCH_RFID_SUGGESTIONS` | `src/libs/spark-legacy/routes/rfid/components/RfidLocationSearchWrapper.tsx` |

### `src/libs/spark-legacy/routes/teams/graphql/TeamsQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `BULK_UPDATE_TEAMS` | `src/libs/spark-palette/src/routes/materials/components/PaletteBulkEditTeamsModal.tsx` |
| ✏️ Mutation | `CREATE_TEAM` | `src/libs/spark-legacy/routes/teams/containers/TeamNew.tsx` |
| ✏️ Mutation | `MANAGE_TEAMS_WORKSPACES` | `src/libs/spark-legacy/routes/teams/containers/ManageTeamWorkspacesModal.tsx` |
| ✏️ Mutation | `UPDATE_TEAM` | _not referenced_ |
| 🔍 Query | `GET_CURRENT_TEAM` | `src/libs/spark-legacy/routes/teams/containers/TeamView.tsx` |
| 🔍 Query | `GET_ROLES` | 6 files |
| 🔍 Query | `GET_TEAM_COMMON_BPS` | `src/libs/spark-legacy/routes/teams/containers/TeamsList.tsx` |
| 🔍 Query | `GET_USERS` | 9 files |
| 🔍 Query | `SEARCH_TEAMS` | 11 files |
| 🔍 Query | `SEARCH_TEAMS_SUGGESTIONS` | `src/libs/spark-legacy/routes/teams/containers/TeamsList.tsx` |

### `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PRODUCT_TEMPLATE_DETAILS` | _not referenced_ |
| ✏️ Mutation | `UPDATE_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateEdit.tsx` |
| 🔍 Query | `GET_ALL_PRODUCTS_TEMPLATES` | `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateQueries.testHelper.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/TemplateLibraryContainer.tsx` |
| 🔍 Query | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `src/libs/bill-of-materials/src/components/productTemplate/ProductTemplateBomExpandedView.tsx` |
| 🔍 Query | `GET_CLAIM_TEMPLATE_BY_ID` | `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateClaimClone.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateClaimEdit.tsx` |
| 🔍 Query | `GET_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/components/ProductTemplatePDTLExpandedView.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateEdit.tsx`, `src/libs/spark-legacy/routes/templateLibrary/containers/ProductTemplateOverviewContainer.tsx` |
| 🔍 Query | `GET_PRODUCT_TEMPLATE_CATEGORY` | `src/libs/spark-legacy/routes/templateLibrary/components/ProductTemplateSideFilterForm.tsx` |
| 🔍 Query | `GET_PRODUCT_TEMPLATE_CLAIMS` | `src/libs/spark-legacy/routes/templateLibrary/components/ProductTemplateClaimExpandedView.tsx` |
| 🔍 Query | `GET_PRODUCT_TEMPLATE_MEASUREMENTS` | _not referenced_ |
| 🔍 Query | `SEARCH_TEMPLATE_SUGGESTIONS` | `src/libs/spark-legacy/routes/templateLibrary/containers/TemplateLibraryContainer.tsx` |

### `src/libs/spark-legacy/routes/users/graphql/usersQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_USERS_LIST` | `src/libs/product-packaging/src/helpers/fetchInternalUsers.ts`, `src/libs/spark-legacy/admin/Impersonation.tsx`, `src/libs/spark-legacy/components/graphql/ComponentsQueries.ts`, `src/libs/spark-legacy/routes/users/containers/UsersList.tsx` |
| 🔍 Query | `SEARCH_USERS_SUGGESTIONS` | `src/libs/spark-legacy/routes/users/containers/UsersList.tsx` |

### `src/libs/spark-legacy/services/graphql/AttachmentQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ARCHIVE_ATTACHMENT` | 11 files |
| 🔍 Query | `SEARCH_ATTACHMENTS` | 17 files |

### `src/libs/spark-legacy/services/graphql/valueAssessment.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `FRAGMENT_VALUE_ASSESSMENT` | _not referenced_ |
| 🧩 Fragment | `FRAGMENT_VALUE_ASSESSMENT_ERRORS` | _not referenced_ |
| 🧩 Fragment | `FRAGMENT_VALUE_ASSESSMENT_RECORD` | _not referenced_ |
| ✏️ Mutation | `CREATE_SCENARIO` | `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |
| ✏️ Mutation | `CREATE_VALUE_ASSESSMENT_MOCK_FABRIC` | `src/libs/samples/src/molecules/ValueAssessmentSection.test.tsx`, `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |
| ✏️ Mutation | `INCLUDE_OR_EXCLUDE_PATTERN` | `src/libs/spark-legacy/components/ValueAssessmentGrid.tsx` |
| ✏️ Mutation | `UPDATE_SCENARIO_REPLACE_FABRIC` | `src/libs/samples/src/molecules/ValueAssessmentSection.test.tsx`, `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |
| 🔍 Query | `GET_ASSESSMENT_DETAILS` | `src/libs/samples/src/molecules/ValueAssessmentSection.test.tsx`, `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |
| 🔍 Query | `GET_SAMPLE_VALUE_ASSESSMENT` | `src/libs/samples/src/molecules/ValueAssessmentSection.test.tsx`, `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |
| 🔍 Query | `GET_VALUE_ASSESSMENT_CATEGORIES` | `src/libs/samples/src/helpers/useGqlValueAssessmentCategories.test.ts`, `src/libs/samples/src/helpers/useGqlValueAssessmentCategories.ts` |
| 🔍 Query | `SEARCH_VALUE_ASSESSMENT_FABRICS` | _not referenced_ |
| 🔍 Query | `SEARCH_VALUE_ASSESSMENT_MATERIALS` | `src/libs/samples/src/molecules/ValueAssessmentSection.test.tsx`, `src/libs/samples/src/molecules/ValueAssessmentSection.tsx` |

---

## Materials

**1 definitions** — 1 queries

### `src/libs/spark-materials/src/customHooks/useMVRelatedSuppliers.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_BUSINESS_PARTNER_BY_ID` | `src/libs/product-common/src/queries/WorkspacePlanQueries.ts`, `src/libs/spark-fabric-graphql/index.ts`, `src/libs/spark-fabric/src/routes/specifications/components/FabricSpecificationForm.tsx`, `src/libs/workspaces/src/routes/plan/components/HistoryDrawer.tsx` |

---

## Materials — Shared GQL

**35 definitions** — 24 queries, 3 mutations, 8 fragments

### `src/libs/spark-materials-graphql/src/graphql/ResourceLinkQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `RESORUCE_LINK_MATERIAL_FRAGMENT` | _not referenced_ |
| 🔍 Query | `SEARCH_RESOURCE_LINKS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/resourceLinks/ResourceLinksWidget.tsx`, `src/libs/spark-materials/src/customHooks/useGetAllResourceLinks.tsx` |
| 🔍 Query | `SEARCH_RESOURCE_LINKS_BY_SOURCE_ID` | `src/libs/spark-fabric/src/inspiration/components/DevelopedCard.tsx`, `src/libs/spark-materials-graphql/index.ts` |

### `src/libs/spark-materials-graphql/src/graphql/getMaterialFromService.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_MATERIAL_FROM_SERVICE` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/hooks/useMaterialFromService.ts` |

### `src/libs/spark-materials-graphql/src/graphql/getTrimTypes.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_TRIM_TYPES` | 6 files |

### `src/libs/spark-materials-graphql/src/graphql/materialCommonFragment.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `COMMON_MATERIAL_FRAGMENT` | `src/libs/spark-artwork-graphql/src/queries/ArtworkFragments.ts`, `src/libs/spark-materials-graphql/index.ts` |

### `src/libs/spark-materials-graphql/src/graphql/materialDetailsFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `MATERIAL_DETAILS` | `src/libs/product-queries/src/queries/BomQueries.ts`, `src/libs/spark-combination-graphql/src/CombinationsFragments.ts`, `src/libs/spark-combination-graphql/src/CombinationsMutations.ts`, `src/libs/spark-combination-graphql/src/CombinationsQueries.ts`, `src/libs/spark-materials-graphql/index.ts` |
| 🧩 Fragment | `MATERIAL_DETAILS_SLIM_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts`, `src/libs/spark-materials-graphql/index.ts` |

### `src/libs/spark-materials-graphql/src/graphql/materialsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `MATERIALS_SEARCH_CONTENT_FRAGMENT` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-palette-graphql/src/PaletteQueries.ts` |
| 🧩 Fragment | `MATERIALS_SEARCH_COUNTS_FRAGMENT` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-palette-graphql/src/PaletteQueries.ts` |
| 🧩 Fragment | `MATERIALS_SEARCH_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `MATERIALS_SEARCH_PAGING_FRAGMENT` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-palette-graphql/src/PaletteQueries.ts` |
| 🔍 Query | `EXPORT_MATERIALS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/MaterialExcelDownload.tsx` |
| 🔍 Query | `GET_COMBO_FROM_SAMPLE` | `src/libs/samples/src/helpers/fsc/FscSampleRedirector.tsx`, `src/libs/spark-materials-graphql/index.ts` |
| 🔍 Query | `GET_DIVISIONS` | `src/libs/spark-artwork/src/components/ArtworkForm.tsx`, `src/libs/spark-legacy/components/connectedComponents/DivisionsAutocomplete.tsx`, `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsQueries.ts`, `src/libs/spark-materials-graphql/index.ts` |
| 🔍 Query | `GET_FABRIC_CONNECTION_ENUMS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/connections/ConnectionsArtworkFilters.tsx`, `src/libs/spark-materials/src/components/connections/ConnectionsMaterialSampleFilters.tsx` |
| 🔍 Query | `GET_FACILITIES` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/components/AddFacilityModal.tsx`, `src/libs/spark-trim-graphql/index.ts`, `src/libs/spark-trim/src/routes/suppliers/components/AddFacilityModal.tsx` |
| 🔍 Query | `GET_HIERARCHY_AND_FAVORITE_MATERIALS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/MaterialCreateAssetModal.tsx` |
| 🔍 Query | `GET_HUB_MATERIAL_STATUS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/MaterialTabsWrapper.tsx` |
| 🔍 Query | `GET_MATERIALS_WITH_PERMISSIONS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/MaterialsList.tsx` |
| 🔍 Query | `GET_MATERIAL_BY_IDS_FROM_SERVICE` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/connections/linkedMaterials/ConnectionsMaterialWrapper.tsx` |
| 🔍 Query | `GET_MATERIAL_FILTER_INFORMATION` | `src/libs/bill-of-materials/src/components/materialsAdvancedSearch/__tests__/BomMaterialAdvancedSearchModal-RTL.test.tsx`, `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/customHooks/useMaterialFilterInformation.ts` |
| 🔍 Query | `GET_MATERIAL_HUB_TYPES_FOR_PARENT` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/MaterialCreateAssetModal.tsx` |
| 🔍 Query | `GET_MATERIAL_RELATED_PALETTES` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/connections/ConnectionsPaletteWrapper.tsx` |
| 🔍 Query | `GET_MATERIAL_SAMPLE_CONNECTIONS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/connections/MaterialSampleConnections.tsx` |
| 🔍 Query | `GET_MATERIAL_TEAMS_WITHOUT_BP` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/MaterialsTeams.tsx`, `src/libs/spark-trim/src/routes/suppliers/TrimSuppliers.tsx`, `src/libs/spark-wash/src/pages/WashTeamPage.tsx` |
| 🔍 Query | `GET_MATERIAL_TEAMS_WITH_BP` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/MaterialsTeams.tsx`, `src/libs/spark-trim/src/routes/suppliers/TrimSuppliers.tsx`, `src/libs/spark-wash/src/pages/WashTeamPage.tsx` |
| 🔍 Query | `GET_RELATED_BOMS` | `src/libs/spark-fabric/src/routes/connections/components/FabricSpecProductConnectionsWrapper.tsx`, `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/containers/connections/MaterialProductConnections.tsx` |
| 🔍 Query | `GET_TRIM_LABEL_TYPE_ENUMS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/filters/trim/FilterTrimLabelCard.tsx` |
| 🔍 Query | `MULTIPLE_REQUEST_MATERIAL_SEARCH` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-palette/src/utils/AseImportUtils.ts` |
| 🔍 Query | `SEARCH_MATERIALS_PAGINATED` | `src/libs/spark-color/src/components/ColorAutocomplete.tsx`, `src/libs/spark-materials-graphql/index.ts` |

### `src/libs/spark-materials-graphql/src/graphql/resourceLinkMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_RESOURCE_LINK` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/container/DevelopUserDefinedMaterial.tsx`, `src/libs/spark-materials/src/components/resourceLinks/ManageResourceLinkModal.tsx` |
| ✏️ Mutation | `BULK_ADD_DELETE_RESOURCE_LINKS` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/resourceLinks/utils/LinkedResourceUtils.ts` |
| ✏️ Mutation | `REMOVE_RESOURCE_LINK` | `src/libs/spark-materials-graphql/index.ts`, `src/libs/spark-materials/src/components/resourceLinks/ManageResourceLinkModal.tsx` |

### `src/libs/spark-materials-graphql/src/graphql/searchMaterials.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `SEARCH_MATERIALS` | 6 files |

---

## Materials Hub

**52 definitions** — 21 queries, 17 mutations, 14 fragments

### `src/libs/spark-materials-hub-graphql/src/BaseMaterialQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `BASE_MATERIAL_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub-graphql/src/PaperQueries.ts`, `src/libs/spark-materials-hub-graphql/src/WoodQueries.ts` |
| 🧩 Fragment | `DEVELOPED_BASE_MATERIALS_FRAGMENT` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🧩 Fragment | `SEARCH_MATERIAL_RESOURCE_LINKS_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🧩 Fragment | `SHOW_CONNECTEDBOMS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| ✏️ Mutation | `ASSOCIATE_HUB_MATERIAL_ATTACHMENT_TEAMS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/utils/userDefinedMaterialUtils.ts` |
| ✏️ Mutation | `REMOVE_RESOURCES_V3` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/container/DevelopUserDefinedMaterial.tsx`, `src/libs/spark-materials-hub/src/userDefined/utils/userDefinedMaterialUtils.ts` |
| ✏️ Mutation | `UPDATE_HUB_MATERIAL_TEAMS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/utils/userDefinedMaterialUtils.ts` |
| ✏️ Mutation | `VALIDATE_MATERIAL_UNIQUENESS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/components/UserDefinedMaterialForm.tsx` |
| 🔍 Query | `GET_ACL_RESOURCE_TOKEN` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/utils/userDefinedMaterialUtils.ts` |
| 🔍 Query | `GET_BASE_MATERIAL_ENUMS` | 8 files |
| 🔍 Query | `GET_HUB_MATERIALS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/DuplicateUserDefinedMaterialModal.tsx` |
| 🔍 Query | `GET_HUB_MATERIAL_AND_TEMPLATE_PERMISSIONS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/UserDefinedMaterialView.tsx`, `src/libs/spark-materials-hub/src/userDefined/container/InspirationUserDefinedMaterialOverview.tsx` |
| 🔍 Query | `GET_HUB_MATERIAL_BY_ID` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/UserDefinedMaterialModify.tsx`, `src/libs/spark-materials-hub/src/userDefined/container/MaterialView.tsx`, `src/libs/spark-materials-hub/src/userDefined/container/ModifyInspirationUserDefinedMaterial.tsx` |
| 🔍 Query | `GET_UNITS_OF_MEASURE` | `src/libs/product-common/index.ts`, `src/libs/product-common/src/queries/MeasurementQueries.tsx`, `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub-graphql/src/useUnitsOfMeasure.ts`, `src/libs/spark-materials-hub/src/userDefined/utils/BulkCreateMaterials.testHelper.ts` |
| 🔍 Query | `SEARCH_MATERIALS_BY_CRITERIA` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/container/BaseMaterialNameField.tsx` |
| 🔍 Query | `SLIM_GET_HUB_MATERIAL_BY_ID` | `src/libs/spark-legacy/routes/resourceRedirect/config/material.tsx`, `src/libs/spark-legacy/routes/resourceRedirect/config/samples.tsx`, `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/ConfigSupplierTab.tsx` |

### `src/libs/spark-materials-hub-graphql/src/MaterialTypeQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_MATERIAL_TEMPLATE` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/materialTemplates/containers/MaterialTypeNew.tsx` |
| ✏️ Mutation | `UPDATE_MATERIAL_TEMPLATE` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/materialTemplates/containers/MaterialTypeEdit.tsx` |
| 🔍 Query | `GET_MATERIAL_HUB_TYPES` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/components/MaterialTypesAutocomplete.tsx`, `src/libs/spark-materials-hub/src/materialTemplates/containers/MaterialTypeEdit.tsx`, `src/libs/spark-materials-hub/src/materialTemplates/containers/MaterialTypeNew.tsx` |
| 🔍 Query | `GET_MATERIAL_TEMPLATE_TYPES` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🔍 Query | `GET_NUMERIC_DIMENSION_ATTRIBUTE_UNITS_OF_MEASURE` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/materialTemplates/AttributeTypes/NumericDimensionAttributeType.tsx` |
| 🔍 Query | `GET_TEMPLATE_BY_ID` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/form/customTableCells/MaterialCellEditor.tsx` |
| 🔍 Query | `GET_TEMPLATE_DETAILS_FOR_FORM` | 6 files |
| 🔍 Query | `GET_TEMPLATE_HIERARCHY` | 12 files |
| 🔍 Query | `GET_TEMPLATE_PERMISSIONS_AND_GALLERY_TAXONOMY` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/UserDefinedMaterialFiles.tsx` |
| 🔍 Query | `GET_TEMPLATE_STATUSES` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/materialTemplates/config/MaterialTemplateMocks.ts`, `src/libs/spark-materials-hub/src/materialTemplates/containers/TemplateStatusField.tsx` |

### `src/libs/spark-materials-hub-graphql/src/PaperQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PAPER_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| ✏️ Mutation | `ADD_PAPER` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/paper/PaperClone.tsx`, `src/libs/spark-materials-hub/src/paper/PaperNew.tsx` |
| ✏️ Mutation | `UPDATE_PAPER` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/paper/PaperEdit.tsx` |
| 🔍 Query | `GET_PAPER_BY_ID` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/paper/Paper.tsx`, `src/libs/spark-materials-hub/src/paper/PaperClone.tsx`, `src/libs/spark-materials-hub/src/paper/PaperEdit.tsx`, `src/libs/spark-materials-hub/src/paper/PaperTestMocks.ts` |
| 🔍 Query | `GET_PAPER_ENUMS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/config/MaterialsComponentRegister.tsx`, `src/libs/spark-materials-hub/src/paper/PaperFilters.tsx`, `src/libs/spark-materials-hub/src/paper/PaperForm.tsx`, `src/libs/spark-materials-hub/src/paper/PaperTestMocks.ts` |

### `src/libs/spark-materials-hub-graphql/src/WoodQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `WOOD_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| ✏️ Mutation | `ADD_WOOD` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/wood/WoodClone.tsx`, `src/libs/spark-materials-hub/src/wood/WoodNew.tsx` |
| ✏️ Mutation | `UPDATE_WOOD` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/wood/WoodEdit.tsx` |
| 🔍 Query | `GET_WOOD_BY_ID` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/wood/Wood.tsx`, `src/libs/spark-materials-hub/src/wood/WoodClone.tsx`, `src/libs/spark-materials-hub/src/wood/WoodEdit.tsx`, `src/libs/spark-materials-hub/src/wood/WoodTestMocks.ts` |
| 🔍 Query | `GET_WOOD_ENUMS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/config/MaterialsComponentRegister.tsx`, `src/libs/spark-materials-hub/src/wood/WoodFilters.tsx`, `src/libs/spark-materials-hub/src/wood/WoodForm.tsx`, `src/libs/spark-materials-hub/src/wood/WoodTestMocks.ts` |

### `src/libs/spark-materials-hub-graphql/src/materialsFragments.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `MATERIAL_TEMPLATE_ATTRIBUTE_DETAILS` | _not referenced_ |
| 🧩 Fragment | `MATERIAL_TEMPLATE_CERTIFICATION_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🧩 Fragment | `MATERIAL_TEMPLATE_COMPOSITION_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🧩 Fragment | `MATERIAL_TEMPLATE_DEFINED_BASE_ATTRIBUTE_CONFIGURATIONS` | _not referenced_ |
| 🧩 Fragment | `MATERIAL_TEMPLATE_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub-graphql/src/BaseMaterialQueries.ts`, `src/libs/spark-materials-hub-graphql/src/MaterialTypeQueries.ts` |
| 🧩 Fragment | `MATERIAL_TEMPLATE_ORIGIN_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts` |
| 🧩 Fragment | `MATERIAL_TEMPLATE_PERMISSIONS_DETAILS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub-graphql/src/MaterialTypeQueries.ts` |
| 🧩 Fragment | `MATERIAL_TEMPLATE_SUPPLIER_DETAILS` | _not referenced_ |

### `src/libs/spark-materials-hub-graphql/src/materialsMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_FAVORITE_MATERIAL_TYPES` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials/src/components/FavoriteMaterialsCard.tsx` |
| ✏️ Mutation | `ADD_RELATIONSHIP` | `src/libs/spark-materials-hub-graphql/index.ts` |
| ✏️ Mutation | `BULK_MATERIAL_VALIDATE_UNIQUENESS` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/utils/userDefinedMaterialUtils.ts` |
| ✏️ Mutation | `CHANGE_MATERIAL_VIEW_SETTING` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials/src/containers/MaterialsList.tsx` |
| ✏️ Mutation | `COPY_ATTACHMENT_V3` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/container/DevelopUserDefinedMaterial.tsx` |
| ✏️ Mutation | `PARTIAL_UPDATE_HUB_MATERIAL` | `src/libs/spark-materials-hub-graphql/index.ts`, `src/libs/spark-materials-hub/src/userDefined/ConfigSupplierItem.tsx`, `src/libs/spark-materials-hub/src/userDefined/EditConfigSupplierModal.tsx`, `src/libs/spark-materials-hub/src/userDefined/UserDefinedMaterialFiles.tsx` |
| ✏️ Mutation | `UPDATE_TEAMS` | 6 files |

### `src/libs/spark-materials-hub-graphql/src/useMaterialTypes.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_MATERIAL_TYPES` | `src/libs/spark-materials-hub-graphql/index.ts` |

---

## Packaging — Base

**9 definitions** — 6 queries, 1 mutations, 2 fragments

### `src/libs/spark-packaging-base/src/graphql/PackagingBrandComplianceMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `BULK_ADD_COMPLIANCE_PRODUCTS` | `src/libs/spark-packaging-base/index.ts`, `src/libs/workspaces/src/routes/products/components/ImportBrandComplianceModal.tsx` |

### `src/libs/spark-packaging-base/src/graphql/PackagingBrandComplianceQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_BRAND_COMPLIANCE_PRODUCTS_RECORD_BY_ID` | `src/libs/spark-packaging-base/index.ts` |
| 🔍 Query | `GET_BRAND_COMPLIANCE_PRODUCTS_VALIDATIONS_BY_IDS` | `src/libs/spark-packaging-base/index.ts`, `src/libs/workspaces/src/routes/products/components/ImportBrandComplianceModal.tsx` |

### `src/libs/spark-packaging-base/src/graphql/PackagingCountryQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_PACKAGING_COUNTRIES` | `src/libs/spark-packaging-base/src/customHooks/usePackagingCountries.ts` |

### `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts`, `src/libs/spark-packaging-base/index.ts`, `src/libs/spark-packaging-base/src/customHooks/usePackagingDetailsByParent.tsx` |
| 🔍 Query | `GET_PACKAGING_FIELD_VALUES_BY_TYPE` | `src/libs/product-packaging/src/helpers/PackagingDetailsQueries.testhelper.ts`, `src/libs/spark-packaging-base/index.ts`, `src/libs/spark-packaging-base/src/customHooks/usePackagingDetailsEnums.ts`, `src/libs/spark-packaging-library/src/builders/index.ts` |

### `src/libs/spark-packaging-base/src/graphql/PackagingLibraryQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `SPG_ATTACHMENT_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `SPG_FRAGMENT` | `src/libs/spark-packaging-base/index.ts`, `src/libs/spark-packaging-library/src/graphql/PackagingLibraryQueries.ts` |
| 🔍 Query | `GET_FILE_LIBRARIES_SEARCH` | 5 files |

---

## Packaging — Library

**7 definitions** — 4 queries, 3 mutations

### `src/libs/spark-packaging-library/src/graphql/PackagingLibraryQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_FILE_LIBRARY_ITEM` | `src/libs/spark-packaging-library/src/builders/index.ts`, `src/libs/spark-packaging-library/src/templates/PackagingLibraryCreateTemplate.tsx` |
| ✏️ Mutation | `GENERATE_SPG_PACKET` | `src/libs/spark-packaging-library/src/components/view/PackagingLibraryOverview.tsx` |
| ✏️ Mutation | `UPDATE_FILE_LIBRARY_ITEM` | `src/libs/spark-packaging-library/src/builders/index.ts`, `src/libs/spark-packaging-library/src/templates/PackagingLibraryEditTemplate.tsx` |
| 🔍 Query | `GET_FILES_V3` | 5 files |
| 🔍 Query | `GET_FILE_LIBRARIES` | `src/libs/spark-packaging-library/src/graphql/PackagingLibraryQueries.testHelper.ts` |
| 🔍 Query | `GET_PACKAGE_LIBRARY` | 4 files |
| 🔍 Query | `GET_RELATED_PACKAGING_COMPONENTS` | 4 files |

---

## Palette

**22 definitions** — 12 queries, 7 mutations, 3 fragments

### `src/libs/spark-palette-graphql/src/PaletteQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `MATERIALS_PALETTE_SEARCH_FRAGMENT` | `src/libs/spark-palette-graphql/index.ts` |
| 🧩 Fragment | `PALETTE_DETAILS` | `src/libs/spark-palette-graphql/index.ts` |
| 🧩 Fragment | `SPARK_Material_DETAILS` | `src/libs/spark-palette-graphql/index.ts` |
| ✏️ Mutation | `ADD_MATERIALS_TO_PALETTE` | `src/libs/spark-legacy/routes/materials/AddMaterialToPalettesRouter.tsx`, `src/libs/spark-legacy/routes/materials/MaterialsBulkAddToPaletteRouter.tsx`, `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette-graphql/src/addMaterialsToPalette.ts` |
| ✏️ Mutation | `ADD_PALETTE` | `src/libs/spark-palette-graphql/index.ts` |
| ✏️ Mutation | `ADD_PARTNERS` | 6 files |
| ✏️ Mutation | `DELETE_PALETTE` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/PaletteOverview.tsx` |
| ✏️ Mutation | `REMOVE_MATERIALS_FROM_PALETTE` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/routes/bulkRemoveFromPalette/BulkRemoveFromPaletteRouter.tsx` |
| ✏️ Mutation | `UPDATE_PALETTE` | 6 files |
| ✏️ Mutation | `UPDATE_TEAMS` | 6 files |
| 🔍 Query | `GET_PALETTE_BY_ID` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/PaletteEdit.tsx`, `src/libs/spark-palette/src/containers/PaletteOverview.tsx`, `src/libs/spark-palette/src/routes/files/PaletteFiles.tsx` |
| 🔍 Query | `GET_PALETTE_DROPDOWN_OPTIONS` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/components/PaletteOverviewSection.tsx`, `src/libs/spark-palette/src/containers/PaletteList.tsx` |
| 🔍 Query | `GET_PALETTE_MATERIALS_WITH_PERMISSIONS` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/CustomPaletteViewPrint.tsx`, `src/libs/spark-palette/src/routes/materials/PaletteMaterialsList.tsx` |
| 🔍 Query | `GET_PALETTE_RELATED_MATERIALS` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/routes/materials/PaletteMaterialsList.tsx`, `src/libs/spark-palette/src/routes/materials/components/PaletteAddMaterialsModal.tsx`, `src/libs/spark-palette/src/utils/AseImportUtils.ts` |
| 🔍 Query | `GET_PALETTE_STATUS` | `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/Palette.tsx` |
| 🔍 Query | `GET_TEAMS` | 6 files |
| 🔍 Query | `REFRESH_PARTNERS` | 6 files |
| 🔍 Query | `REFRESH_TEAMS` | 6 files |
| 🔍 Query | `SEARCH_MATERIALS` | 6 files |
| 🔍 Query | `SEARCH_PALETTES` | `src/libs/spark-materials/src/components/searchToCollect/MaterialsSearchFormField.tsx`, `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/PaletteList.tsx` |
| 🔍 Query | `SEARCH_PALETTE_MATERIALS` | `src/libs/spark-materials/src/components/searchToCollect/MaterialsSearchFormField.tsx`, `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/routes/materials/components/PaletteBulkEditTeamsModal.tsx` |
| 🔍 Query | `SEARCH_Palette_SUGGESTIONS` | `src/libs/spark-materials/src/components/searchToCollect/MaterialsSearchFormField.tsx`, `src/libs/spark-palette-graphql/index.ts`, `src/libs/spark-palette/src/containers/PaletteList.tsx` |

---

## Resources

**9 definitions** — 7 queries, 2 mutations

### `src/libs/spark-resources/src/graphql/TrainingQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `SEND_NOTIFICATION` | `src/libs/spark-resources/src/containers/Resources.tsx` |
| ✏️ Mutation | `SET_TRAINING_TOPICS` | `src/libs/spark-resources/src/components/TrainingMaterialsList.tsx`, `src/libs/spark-resources/src/components/atoms/ResourcesTopicsFilter.tsx`, `src/libs/spark-resources/src/containers/Resources.tsx` |
| 🔍 Query | `GET_ALL_RESOURCE_TRAINING_DOCUMENTS` | `src/libs/spark-resources/src/builders/gqlMocks/index.ts`, `src/libs/spark-resources/src/containers/Resources.tsx` |
| 🔍 Query | `GET_IMAGE` | `src/libs/spark-resources/src/components/atoms/ImageViewer.tsx` |
| 🔍 Query | `GET_RESOURCE_TRAINING_DOCUMENT` | `src/libs/spark-resources/src/containers/ResourcesView.tsx` |
| 🔍 Query | `GET_RESOURCE_TRAINING_LABELS` | _not referenced_ |
| 🔍 Query | `GET_TRAINING_TOPICS` | `src/libs/spark-resources/src/builders/gqlMocks/index.ts`, `src/libs/spark-resources/src/components/TrainingMaterialsList.tsx`, `src/libs/spark-resources/src/components/atoms/ResourcesTopicsFilter.tsx`, `src/libs/spark-resources/src/containers/Resources.tsx` |
| 🔍 Query | `GET_VIDEO` | _not referenced_ |
| 🔍 Query | `SEARCH_RESOURCE_TRAINING_DOCUMENTS` | _not referenced_ |

---

## Rules

**7 definitions** — 4 queries, 2 mutations, 1 fragments

### `src/libs/spark-rules/src/graphql/RulesQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `RULE_LIBRARY_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `ADD_RULE_LIBRARIES` | `src/libs/spark-rules/src/components/molecules/RuleLibraryListElement.tsx` |
| ✏️ Mutation | `UPDATE_RULE_LIBRARIES` | `src/libs/spark-rules/src/components/molecules/RuleLibraryListElement.tsx` |
| 🔍 Query | `GET_ALL_RULE_LIBRARIES` | `src/libs/spark-rules/src/components/molecules/RuleLibraryListElement.tsx`, `src/libs/spark-rules/src/customHooks/useGetAllRuleLibraryOptions.ts` |
| 🔍 Query | `GET_ALL_RULE_OPTIONS` | `src/libs/spark-rules/src/customHooks/useGetAllRuleLibraryOptions.ts` |
| 🔍 Query | `SEARCH_RULE_LIBRARIES` | `src/libs/spark-mock-data-builders/src/builders/product.ts`, `src/libs/spark-rules/index.ts`, `src/libs/spark-rules/src/customHooks/useSearchRuleLibrary.ts` |
| 🔍 Query | `SEARCH_RULE_LIBRARIES_GROUPED_BY_PIDS` | `src/libs/spark-rules/src/customHooks/useSearchRuleLibrary.ts` |

---

## Static / Temp

**1 definitions** — 1 queries

### `src/libs/spark-static/src/temp/graphql/BackgroundActivityQuery.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_BACKGROUND_ACTIVITY_NOTIFICATIONS_TEMP` | `src/libs/spark-legacy/containers/Notifications/withUserContext.tsx`, `src/libs/spark-static/index.ts` |

---

## Trim — UI

**1 definitions** — 1 queries

### `src/libs/spark-trim/src/forms/fields/TrimConditionalEnumField.tsx`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `query` | 441 files |

---

## Trim — GQL

**23 definitions** — 19 queries, 4 fragments

### `src/libs/spark-trim-graphql/src/TrimSampleQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `TRIM_COLOR_DETAILS_M_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `TRIM_DETAILS_M` | _not referenced_ |
| 🧩 Fragment | `TRIM_FINISH_DETAILS_M` | _not referenced_ |
| 🧩 Fragment | `TRIM_SIZE_DETAILS_M` | _not referenced_ |
| 🔍 Query | `GET_SELECT_OPTIONS_FOR_TRIM_SAMPLE` | `src/libs/samples/src/containers/trim/TrimSampleNew.tsx`, `src/libs/samples/src/containers/wash/WashSampleNew.tsx`, `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_AND_OPTIONS` | `src/libs/samples/src/containers/trim/TrimSampleBulkCreate.tsx`, `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_BY_ID_MIN` | `src/libs/samples/src/components/trim/TrimSampleComponentWrapper.tsx`, `src/libs/samples/src/containers/trim/TrimSampleNew.tsx`, `src/libs/samples/src/pages/Sample.tsx`, `src/libs/spark-trim-graphql/index.ts`, `src/libs/spark-trim/src/pages/TrimSamplesListPage.tsx` |

### `src/libs/spark-trim-graphql/src/getTrimEnumQuery.ts`

| Type | Name | Used In |
|------|------|---------|
| 🔍 Query | `GET_TRIM_BUCKLE_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_BUTTON_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_CLOSURE_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_CONSTRUCTION_COMPONENTS_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_CORD_PARTS_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_ELASTIC_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_EMBELLISHMENT_PARTS_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_HARDWARE_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_INTERLINING_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_LABEL_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_LACE_NARROW_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_PATCH_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_TAPE_RIBBON_CORDING_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_THREAD_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_ZIPPER_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |
| 🔍 Query | `GET_TRIM_ZIPPER_PULLER_ENUMS` | `src/libs/spark-trim-graphql/index.ts` |

---

## UI Admin

**51 definitions** — 37 queries, 13 mutations, 1 fragments

### `src/libs/spark-ui-admin/src/graphql/uiAdminMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `EXPIRE_KEY` | _not referenced_ |
| ✏️ Mutation | `REFRESH_PRODUCT` | _not referenced_ |
| ✏️ Mutation | `REFRESH_PRODUCTS` | _not referenced_ |
| ✏️ Mutation | `REFRESH_SAMPLE` | _not referenced_ |
| ✏️ Mutation | `REFRESH_SAMPLES` | _not referenced_ |
| ✏️ Mutation | `REFRESH_WORKSPACE` | _not referenced_ |
| ✏️ Mutation | `REFRESH_WORKSPACES` | _not referenced_ |
| ✏️ Mutation | `REQUEST_REPORT` | _not referenced_ |
| ✏️ Mutation | `RESEND_DISCUSSION` | _not referenced_ |
| ✏️ Mutation | `RETRY_PACKET` | _not referenced_ |

### `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `DIFF_QUERY_FRAGMENT` | _not referenced_ |
| 🔍 Query | `GET_ACL_PROXY_TOKEN` | _not referenced_ |
| 🔍 Query | `GET_ACL_TOKEN` | _not referenced_ |
| 🔍 Query | `GET_ATTACHMENTS` | _not referenced_ |
| 🔍 Query | `GET_BOM_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_BP_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_COMBO_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_DISCUSSIONS_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_FABRIC_BY_ID` | 9 files |
| 🔍 Query | `GET_FSC_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_KEY` | _not referenced_ |
| 🔍 Query | `GET_MEASUREMENT_SET_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_PERMISSIONS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts`, `src/libs/spark-legacy/customHooks/useUpdateResourceACLGroups.tsx`, `src/libs/spark-legacy/routes/teams/components/TeamManagePermissionsModal.tsx` |
| 🔍 Query | `GET_PRODUCT_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_PRODUCT_PACKET_REPORTS` | _not referenced_ |
| 🔍 Query | `GET_PRODUCT_VERSIONS` | _not referenced_ |
| 🔍 Query | `GET_RELATIONSHIPS_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_SAMPLE_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_SAMPLE_LOCATIONS` | _not referenced_ |
| 🔍 Query | `GET_SYSTEM_TEAMS` | _not referenced_ |
| 🔍 Query | `GET_TEAM_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_TRIM_BY_ID` | `src/libs/spark-trim-graphql/index.ts`, `src/libs/spark-trim/src/containers/TrimClone.tsx`, `src/libs/spark-trim/src/containers/TrimOverview.tsx`, `src/libs/spark-trim/src/pages/TrimFilesWrapperPage.tsx` |
| 🔍 Query | `GET_UNSENT_DISCUSSIONS` | _not referenced_ |
| 🔍 Query | `GET_USER_BY_ID` | _not referenced_ |
| 🔍 Query | `GET_WHERE_USED` | _not referenced_ |
| 🔍 Query | `GET_WORKSPACE_BY_ID` | _not referenced_ |
| 🔍 Query | `QUERY_PRODUCT_DIFF` | _not referenced_ |
| 🔍 Query | `QUERY_SAMPLE_DIFF` | _not referenced_ |
| 🔍 Query | `QUERY_TEAM_DIFF` | _not referenced_ |
| 🔍 Query | `QUERY_WORKSPACE_DIFF` | _not referenced_ |
| 🔍 Query | `SEARCH_BUSINESS_PARTNERS` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/components/BPSelectAutoComplete.tsx`, `src/libs/spark-legacy/routes/admin/routes/vendorMerge/graphql/VendorMergeQueries.ts` |
| 🔍 Query | `SEARCH_RELATIONSHIPS_BY_IDS` | _not referenced_ |
| 🔍 Query | `SEARCH_USERS` | _not referenced_ |
| 🔍 Query | `SEARCH_USERS_BY_BP` | _not referenced_ |

### `src/libs/spark-ui-admin/src/pages/systemEvents/graphql/systemEventQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `ADD_SPARK_BANNER` | `src/libs/spark-ui-admin/src/pages/systemEvents/SystemEventsPage.tsx` |
| ✏️ Mutation | `ARCHIVE_SPARK_BANNER` | `src/libs/spark-ui-admin/src/pages/systemEvents/EventDetails.tsx` |
| ✏️ Mutation | `UPDATE_SPARK_BANNER` | `src/libs/spark-ui-admin/src/pages/systemEvents/EventDetails.tsx` |
| 🔍 Query | `GET_ACTIVE_BANNERS` | `src/libs/spark-layout/src/organisms/SparkBanner.tsx`, `src/libs/spark-legacy/containers/Home/SplashPage.tsx`, `src/libs/spark-router/src/SparkRouter.tsx`, `src/libs/spark-ui-admin/index.ts` |
| 🔍 Query | `GET_BANNER_SCOPES` | `src/libs/spark-ui-admin/src/pages/systemEvents/SystemEventsPage.tsx` |
| 🔍 Query | `GET_BANNER_TYPES` | `src/libs/spark-ui-admin/src/pages/systemEvents/SystemEventsPage.tsx` |
| 🔍 Query | `SEARCH_BANNERS` | `src/libs/spark-ui-admin/src/pages/systemEvents/SystemEventsPage.tsx` |

---

## Wash

**3 definitions** — 2 queries, 1 fragments

### `src/libs/spark-wash-graphql/src/washFederatedQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `PLM_WASH_DETAILS_FRAGMENT` | `src/libs/spark-wash-graphql/index.ts` |
| 🔍 Query | `PLM_GET_BUSINESS_PARTNERS_BY_IDS` | `src/libs/spark-wash-graphql/index.ts`, `src/libs/spark-wash/src/components/WashForm.tsx` |
| 🔍 Query | `PLM_GET_WASH_DROPDOWN_VALUES` | `src/libs/spark-wash-graphql/index.ts`, `src/libs/spark-wash/src/components/WashForm.tsx` |

---

## Watchlist

**11 definitions** — 6 queries, 3 mutations, 2 fragments

### `src/libs/watchlist/src/graphql/WatchlistQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| 🧩 Fragment | `WATCHLIST_FRAGMENT` | _not referenced_ |
| 🧩 Fragment | `WATCHLIST_PARTICIPANT_FRAGMENT` | _not referenced_ |
| ✏️ Mutation | `CLONE_WATCHLIST_ATTACHMENTS` | `src/libs/watchlist/src/containers/WatchlistCloneTemplate.tsx`, `src/libs/watchlist/src/routes/WatchlistCloneRoute.test.tsx` |
| ✏️ Mutation | `CREATE_WATCHLIST_ENTRIES` | 5 files |
| ✏️ Mutation | `UPDATE_WATCHLIST_ENTRIES` | `src/libs/watchlist/src/containers/WatchlistBulkUpdate.tsx`, `src/libs/watchlist/src/containers/WatchlistEditTemplate.tsx`, `src/libs/watchlist/src/routes/WatchlistEditRoute.test.tsx` |
| 🔍 Query | `GET_WATCHLIST_BY_IDS` | `src/libs/watchlist/src/containers/WatchlistCloneTemplate.tsx`, `src/libs/watchlist/src/containers/WatchlistEditTemplate.tsx`, `src/libs/watchlist/src/containers/WatchlistViewTemplate.tsx` |
| 🔍 Query | `GET_WATCHLIST_FORM_CONSTANTS` | `src/libs/watchlist/src/containers/WatchlistNewTemplate.tsx` |
| 🔍 Query | `GET_WATCHLIST_FOR_BULK_CREATE` | `src/libs/watchlist/src/containers/WatchlistBulkCreate.tsx` |
| 🔍 Query | `GET_WATCHLIST_FOR_BULK_UPDATE` | `src/libs/watchlist/src/containers/WatchlistBulkUpdate.tsx` |
| 🔍 Query | `GET_WATCHLIST_VERSION` | `src/libs/watchlist/src/containers/WatchlistViewTemplate.tsx` |
| 🔍 Query | `SEARCH_WATCHLIST` | `src/libs/product/src/components/specs/WatchlistContent.tsx`, `src/libs/watchlist/index.ts` |

---

## Workspaces

**5 definitions** — 1 queries, 4 mutations

### `src/libs/workspaces/src/graphql/BulkDiscussionQueries.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `BULK_CREATE_DISCUSSIONS` | `src/libs/workspaces/src/routes/discussions/containers/DiscussionBulkCreate.tsx` |
| ✏️ Mutation | `CLONE_BULK_DISCUSSIONS_ATTACHMENTS` | `src/libs/workspaces/src/routes/discussions/components/cloneBulkDiscussionFilesUtil.ts` |
| 🔍 Query | `GET_BULK_DISCUSSION_DATA` | `src/libs/workspaces/src/routes/discussions/containers/DiscussionBulkCreate.tsx` |

### `src/libs/workspaces/src/graphql/workspaceMutations.ts`

| Type | Name | Used In |
|------|------|---------|
| ✏️ Mutation | `CREATE_WORKSPACE` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |
| ✏️ Mutation | `UPDATE_WORKSPACE` | `src/libs/workspaces/src/containers/WorkspaceFormContainer.tsx` |

---
