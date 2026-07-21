# Frontend GraphQL Client Inventory — Phase-1 Domains

> Source: `pdex-ui-react` gql definitions (ClientCallingGqlQueries snapshot) · Generated: 2026-07-21
> Scope: frontend operations that call a phase-1 domain root field (product, bom, measurement, productDetails, packaging, watchlist, impression, claims), with variables, root fields, fragment usage and consuming files.

## Summary

| Stat | Count |
|---|---|
| Phase-1 operations | 145 |
| Queries | 91 |
| Mutations | 54 |
| Fragments on phase-1 types | 23 |
| Client libraries involved | 11 |
| Dynamic (runtime-composed) definitions | 3 |

### Out of scope

- 615 further client operations resolve to later-phase domains or to services outside spark-internal-graphql — excluded per program scope (phase 1 = the 8 domains above).
- 206 further fragments target non-phase-1 types.

## Dynamic / runtime-composed definitions

- These gql documents are assembled at runtime (interpolated operation names, conditional fragments) and cannot be statically inventoried.
- They are incompatible with GraphQL codegen and persisted queries — each needs an explicit refactoring story before federation cutover.

| Const | Client file | Failure mode |
|---|---|---|
| `BUILD_FILES_FRAGMENT` | `ClientCallingGqlQueries/product-queries__BomQueries.txt` | expected '{' got 'files' |
| `BOM_FABRIC_SPEC_COMBO_DETAILS` | `ClientCallingGqlQueries/product-queries__BomQueries.txt` | expected '{' got 'SPARK_FabricSpecCombo' |
| `query` | `ClientCallingGqlQueries/spark-trim__TrimConditionalEnumField.txt` | expected '{' got '$' |

## Product (`product`)

- Definitions: 64 operations (44 queries, 20 mutations) + 7 fragments
- Client libraries: `claims`, `core-discussions`, `product-common`, `product-packaging`, `product-queries`, `spark-legacy`, `spark-ui-admin`, `workspaces`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `addBusinessPartnersToProductWithType` | mutation | `ADD_PARTNERS_PRODUCT_WITH_TYPE` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | $productId: ID!, $partners: [SPARK_ProductPartnerInput] | `addBusinessPartnersToProductWithType` | — | — | — | — |
| `addProduct` | mutation | `ADD_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $workspaceId: ID, $sparkProduct: SPARK_ProductInput!, $copyProduct: SPARK_CopyProductInput | `addProduct` | — | `ProductNew.tsx`<br>`ProductTemplateNew.tsx` | — | — |
| `addProductRule` | mutation | `ADD_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $rule: SPARK_ProductRuleCreateInput | `addProductRule` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `addTeams` | mutation | `ADD_TEAMS_PRODUCT` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | $productId: String!, $teamIds: [String], $workspaceIds: [String], $newPartners: [SPARK_ProductPartnerInput] | `addTeamsToProduct` | — | `BPSelector.tsx` | — | — |
| `productBusinessPartnerActions` | mutation | `BUSINESS_PARTNER_ACTIONS_PRODUCT` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | $actionType: String!, $values: SPARK_ProductPartnerActionInput | `productBusinessPartnerActions` | — | `Teams.tsx` | — | — |
| `carryForwardProduct` | mutation | `CARRY_FORWARD_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productId: String, $carryForwardProductInput: CarryForwardProductInput | `carryForwardProduct` | — | `ProductCarryForwardModal.tsx`<br>`WorkspacePlanGrid.tsx` | — | — |
| `deleteProductRule` | mutation | `DELETE_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $ruleId: ID! | `deleteProductRule` | — | — | — | — |
| `linkProduct` | mutation | `LINK_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $parentProductId: String!, $childProductId: String! | `linkProduct` | `LINK_PRODUCT_FRAGMENT`, `linkProductFragment` | `ProductActionsDropDown.tsx` | — | — |
| `updateProductTeamsWorkspaceContext` | mutation | `MANAGE_TEAMS_WORKSPACES` | `src/libs/spark-legacy/routes/teams/graphql/TeamsQueries.tsx` | $productId: ID!, $teamWorkspacesToAdd: [WorkspaceTeamPair], $teamWorkspacesToRemove: [WorkspaceTeamPair] | `updateProductTeamsWorkspaceContext` | — | `ManageTeamWorkspacesModal.tsx` | — | — |
| `addProducts` | mutation | `PRODUCT_BULK` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $workspaceId: ID!, $products: [SPARK_ProductInput] | `addProducts` | — | `ProductBulkCreate.tsx` | — | — |
| `bulkUpdateProducts` | mutation | `PRODUCT_BULK_UPDATE` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $products: [SPARK_ProductUpdateInput]! | `bulkUpdateProducts` | — | `ProductBulkUpdate.tsx` | — | — |
| `updateViewToggle` | mutation | `TOGGLE_VIEW_SWITCH` | `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsMutations.ts` | $toggleInput: SPARK_ToggleInput! | `updateViewToggle` | — | `ToggleViewFilter.tsx` | — | — |
| `unlinkProduct` | mutation | `UNLINK_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $parentProductId: String!, $childProductId: String! | `unlinkProduct` | `LINK_PRODUCT_FRAGMENT`, `linkProductFragment` | `Links.tsx`<br>`ProductLinkRailListItem.tsx` | — | — |
| `updateComponentStatus` | mutation | `UPDATE_COMPONENT_STATUS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productComponents: [ProductComponentStatusUpdateInput] | `updateComponentStatus` | — | `ComponentStatusDropdown.tsx` | — | `bom.ts` |
| `updateComponentStatuses` | mutation | `UPDATE_COMPONENT_STATUSES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productId: String!, $ids: SPARK_ComponentIdsInput!, $status: SPARK_ComponentStatusInput | `updateComponentStatuses` | — | `ProductComponentSetStatusesDropdown.tsx` | — | — |
| `updateProduct` | mutation | `UPDATE_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $input: SPARK_ProductUpdateInput!, $copyProduct: SPARK_CopyProductInput | `updateProduct` | — | — | — | — |
| `updateProduct` | mutation | `UPDATE_PRODUCT` | `(local) ClientCallingGqlQueries/spark-legacy__carouselMutations.txt` | $input: SPARK_ProductUpdateInput! | `updateProduct` | — | — | — | — |
| `updateProductRule` | mutation | `UPDATE_PRODUCT_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $rule: SPARK_ProductRuleUpdateInput | `updateProductRule` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `updateBusinessPartnerStatuses` | mutation | `UPDATE_PRODUCT_STATUSES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productId: String!, $statusInput: [SPARK_ProductPartnerStatusInput]! | `updateBusinessPartnerStatuses` | — | `BPSelector.tsx`<br>`ProductsGridItem.tsx`<br>`ProductsListItemHeader.tsx` | — | `withProductPartnerStatuses.tsx` |
| `updateProduct` | mutation | `UPDATE_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $sparkProduct: SPARK_ProductUpdateInput!, $copyProduct: SPARK_CopyProductInput | `updateProduct` | — | `ProductTemplateEdit.tsx` | — | — |
| `getTechPackBulkCount` | query | `BULK_TECHPACK_COUNTS` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $bulkTechPackCountResource: [SPARK_ProductTechPackCountInput] | `getProductTechPackBulkCountV1` | — | `BulkGenerateProductPacketModal.tsx`<br>`BulkGenerateReleasePacketModal.tsx` | — | `product.ts` |
| `getAllAvailableRules` | query | `GET_ALL_AVAILABLE_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | — | `getAllAvailableRules` | — | — | — | — |
| `getProducts` | query | `GET_ALL_PRODUCTS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $page: Int, $size: Int, $q: String, $filter: [String] | `getProducts` | — | — | — | — |
| `getProductTemplates` | query | `GET_ALL_PRODUCTS_TEMPLATES` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $page: Int, $size: Int, $q: String, $filter: [String], $types: [Int], $includeProductComponentsCount: Boolean | `getProductTemplates` | — | `ProductTemplateQueries.testHelper.tsx`<br>`TemplateLibraryContainer.tsx` | — | — |
| `getBulkDiscussionData` | query | `GET_BULK_DISCUSSION_DATA` | `src/libs/workspaces/src/graphql/BulkDiscussionQueries.ts` | $productIds: [ID]!, $workspaceId: String | `getRoles`, `getProductsByIds` | — | `DiscussionBulkCreate.tsx` | — | — |
| `getCarryForwardFormData` | query | `GET_CARRY_FORWARD_FORM_DATA` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $workspaceId: ID, $strWorkspaceId: String | `searchImpressionsByProductId`, `getProduct` | `PRODUCT_COMPONENT_FRAGMENT`, `PRODUCT_FULL_TEAM_FRAGMENT`, `ProductFullTeamFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct`, `productComponentFragment` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | — | — |
| `getTechPackCountV1` | query | `GET_COUNT_V1` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productId: ID!, $partnerId: ID, $workspaceContext: String, $parentProductId: ID | `getProductTechPackCountV1` | — | `GenerateTechPackModal.tsx`<br>`ReleaseTechPackModal.tsx` | — | — |
| `getFilesWithMetaData` | query | `GET_FILES_WITH_METADATA` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $productIds: [ID]! | `getProductsByIds` | `ATTACHMENTS_WITH_META_DATA_FRAGMENT`, `AttachmentsWithMetaData` | — | — | `handleUpdateSubmit.tsx` |
| `getProduct` | query | `GET_PRODUCT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID! | `getProduct` | `PRODUCT_COMPONENT_FRAGMENT`, `productComponentFragment` | `ImportProductDetailsModal.tsx`<br>`ProductEdit.tsx` | — | `index.ts`<br>`product.ts` |
| `getFormData` | query | `GET_PRODUCTS_BY_ID_LIST` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $productIds: [ID]!, $workspaceId: ID!, $strWorkspaceId: String | `getWorkspaceV2`, `getTags`, `getTags`, `getProductStatus`, `getProductsByIds` | `PRODUCT_COMPONENT_FRAGMENT`, `productComponentFragment` | `ProductBulkUpdate.tsx` | — | — |
| `getProductTemplates` | query | `GET_PRODUCTS_WITH_IDS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $page: Int, $size: Int, $q: String, $filter: [String], $resourceType: String, $resourceId: String, $includeBoms: Boolean, $includeClaims: Boolean, $includeMeasurementSets: Boolean, $includeProductDetails: Boolean, $workspaceIdFilter: String, $includeProductComponentsCount: Boolean | `getProductTemplates` | — | `ClaimBulkUpdate.tsx` | — | `index.ts` |
| `getProducts` | query | `GET_PRODUCTS_WITH_SAMPLE_DETAILS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $page: Int, $size: Int, $q: String, $filter: [String] | `getProducts` | — | `SampleCompare.tsx` | — | — |
| `getProductWorkspaces` | query | `GET_PRODUCT_AND_WORKSPACES` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $q: String | `getProduct`, `getWorkspacesPagedV3` | `PRODUCT_FULL_TEAM_FRAGMENT`, `ProductFullTeamFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ReleaseProductPacket.tsx`<br>`WatchlistForm.tsx`<br>`WatchlistViewTemplate.tsx` | — | — |
| `getProductWorkspaces` | query | `GET_PRODUCT_AND_WORKSPACES_WITH_STATUS` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $q: String, $workspaceIdFilter: String | `getProduct`, `getWorkspacesPagedV3` | `PRODUCT_VENDOR_ATTRIBUTES`, `ProductVendorAttributesFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ReleaseTechPackModal.tsx` | — | — |
| `getProductBPRules` | query | `GET_PRODUCT_BUSINESS_PARTNER_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $businessPartnerIds: [Int], $activeOnly: Boolean | `getProductBPRules` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `getProductById` | query | `GET_PRODUCT_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | $id: ID! | `getProduct` | — | — | — | — |
| `getProductComponentStatusCounts` | query | `GET_PRODUCT_COMPONENT_STATUS_COUNTS` | `src/libs/product-queries/src/queries/ProductFilesQueries.tsx` | $id: ID!, $partnerId: ID, $type: String, $tags: [String], $archived: Boolean, $workspaceId: String, $types: [Int] | `getProduct` | — | `BomViewTemplate.tsx`<br>`ProductFilesQueries.testHelper.tsx`<br>`SpecsContainer.tsx` | — | — |
| `breadcrumbProduct` | query | `GET_PRODUCT_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/graphql/BreadcrumbQueries.ts` | $id: ID! | `getProduct` | — | `BreadcrumbProduct.tsx` | — | `BreadcrumbProduct.test.tsx` |
| `getProductDeptRules` | query | `GET_PRODUCT_DEPARTMENT_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $productIds: [String], $departmentIds: [Int], $activeOnly: Boolean | `getProductDeptRules` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `getProductStatusUpdateInfo` | query | `GET_PRODUCT_FOR_STATUS_UPDATE` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $workspaceIdFilter: String | `getProductStatus`, `getProduct` | `PRODUCT_VENDOR_ATTRIBUTES`, `ProductVendorAttributesFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ProductQueries.testHelper.tsx` | — | `withProductPartnerStatuses.tsx` |
| `getProduct` | query | `GET_PRODUCT_MINIMAL` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID! | `getProduct` | `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | — | — | — |
| `getStatus` | query | `GET_PRODUCT_STATUS` | `src/libs/spark-legacy/components/connectedComponents/graphql/ConnectedComponentsQueries.ts` | — | `getProductStatus`, `getProductSampleEvaluationTypesV2`, `getSampleTrackingTypesV2` | — | — | — | — |
| `getTeams` | query | `GET_PRODUCT_TEAMS` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | $id: ID! | `getProduct`, `getRoles` | `DISCUSSION_TEAMS_FRAGMENT`, `DiscussionTeamsFragment` | — | — | — |
| `getTeams` | query | `GET_PRODUCT_TEAMS` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | $id: ID! | `getProduct`, `getRoles` | `LEGACY_DISCUSSION_TEAMS_FRAGMENT`, `LegacyDiscussionTeamsFragment` | — | — | — |
| `getProductTemplates` | query | `GET_PRODUCT_TEMPLATE` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $page: Int, $size: Int, $q: String, $filter: [String], $types: [Int], $resourceId: String, $resourceType: String, $includeProductDetailTemplates: Boolean, $includeProductComponentsCount: Boolean, $includeClaimTemplates: Boolean, $includeMeasurementSetTemplates: Boolean, $includeBomTemplates: Boolean, $includeAttachmentsTemplates: Boolean | `getProductTemplates` | `ATTACHMENT_V3_FRAGMENT`, `AttachmentV3Fragment`, `FULL_CLAIM_DETAILS(true)`, `FullClaimDetailsFragment`, `MEASUREMENT_TEMPLATE_FRAGMENT`, `PRODUCT_TEMPLATE_DETAILS`, `SIZE_TEMPLATE_FRAGMENT_WITH_ROWS`, `TIGHT_FIT_FRAGMENT`, `measurementTemplateFragment`, `productTemplateDetails`, `sizeTemplateFragmentWithRows`, `tightFitFragment` | `ProductTemplatePDTLExpandedView.tsx`<br>`ProductTemplateEdit.tsx`<br>`ProductTemplateOverviewContainer.tsx` | — | — |
| `getCategories` | query | `GET_PRODUCT_TEMPLATE_CATEGORY` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $resourceId: String, $resourceType: String, $type: String!, $productType: Int | `getCategories` | — | `ProductTemplateSideFilterForm.tsx` | — | — |
| `getProductVersions` | query | `GET_PRODUCT_VERSIONS` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | $id: ID! | `getProductVersions` | — | — | — | — |
| `getProductWithAttachmentsAndComponents` | query | `GET_PRODUCT_WITH_ATTACHMENTS_AND_COMPONENTS` | `src/libs/product-queries/src/queries/ProductFilesQueries.tsx` | $id: ID!, $partnerId: ID, $type: String, $tags: [String], $archived: Boolean, $workspaceId: String, $includeUnfilteredData: Boolean, $onlyProductPacketFiles: Boolean, $types: [Int] | `getProduct` | `ATTACHMENT_V3_FRAGMENT`, `AttachmentV3Fragment`, `PRODUCT_BASE_INFO_FRAGMENT`, `PRODUCT_COMPONENT_FRAGMENT`, `ProductBaseInfoFragment`, `productComponentFragment` | — | — | — |
| `getProduct` | query | `GET_PRODUCT_WITH_META_DATA` | `src/libs/product-queries/src/queries/WorkspaceFilesQueries.ts` | $id: ID!, $resourceString: ID | `getUserAccessUnencoded`, `getProduct` | `ATTACHMENTS_WITH_META_DATA_FRAGMENT`, `AttachmentsWithMetaData` | — | — | — |
| `getProductWithTeams` | query | `GET_PRODUCT_WITH_TEAMS` | `src/libs/product-queries/src/queries/TeamTabQueries.ts` | $id: ID!, $partnerId: String, $workspaceId: String, $isDesignPartner: Boolean | `getProduct` | `PRODUCT_FULL_TEAM_FRAGMENT`, `ProductFullTeamFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `BPSelector.tsx`<br>`Teams.tsx` | — | — |
| `getProductWorkspaceMetricsReportCount` | query | `GET_PRODUCT_WORKSPACES_METRICS_REPORT_COUNT` | `src/libs/product-queries/src/queries/workspaceQueries.tsx` | $workspaceId: String | `getSampleProductTypesV2`, `getProductStatus`, `getProductWorkspaceMetricsReportCount` | — | `WorkspaceOverview.tsx` | — | — |
| `getProductRule` | query | `GET_RULE` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $id: ID! | `getProductRulesById` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `getProductRules` | query | `GET_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | — | `getProductRules` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | — | — |
| `searchProductRules` | query | `GET_SEARCH_PRODUCT_DEPARTMENT_RULES` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | $productIds: [String], $departmentIds: [Int], $businessPartnerIds: [Int] | `searchProductRules` | `PRODUCT_RULES_FIELDS_FRAGMENT`, `ProductRules` | — | `useSearchProductRules.tsx` | — |
| `getProduct` | query | `GET_SPARK_PRODUCT_BP` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | $id: ID! | `getProduct` | `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ImportProductDetailsSection.tsx` | — | `discussionsUtils.ts`<br>`LegacyDiscussionQueries.ts` |
| `getProduct` | query | `GET_SPARK_PRODUCT_BP` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | $id: ID! | `getProduct` | `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ImportProductDetailsSection.tsx` | — | `DiscussionQueries.ts`<br>`discussionsUtils.ts` |
| `getProductScaffolding` | query | `GET_SPARK_PRODUCT_SCAFFOLDING` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $workspaceIdFilter: String, $partnerIdFilter: String, $isDesignPartner: Boolean | `getProduct` | `PRODUCT_BASE_INFO_FRAGMENT`, `PRODUCT_VENDOR_ATTRIBUTES`, `ProductBaseInfoFragment`, `ProductVendorAttributesFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | — | — | — |
| `getProduct` | query | `GET_SPARK_PRODUCT_V2` | `src/libs/core-discussions/src/graphql/DiscussionQueries.ts` | $id: ID!, $partnerId: ID | `getProduct` | `DISCUSSION_LIST_FRAGMENT_V2`, `DiscussionListFragmentV2`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ProductsListItem.tsx` | — | `discussionsUtils.ts`<br>`functionsNewDiscussion.tsx`<br>`LegacyDiscussionQueries.ts` |
| `getProduct` | query | `GET_SPARK_PRODUCT_V2` | `src/libs/product-queries/src/queries/LegacyDiscussionQueries.ts` | $id: ID!, $partnerId: ID | `getProduct` | `LEGACY_DISCUSSION_LIST_FRAGMENT_V2`, `LegacyDiscussionListFragmentV2`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct` | `ProductsListItem.tsx` | — | `DiscussionQueries.ts`<br>`discussionsUtils.ts`<br>`functionsNewDiscussion.tsx` |
| `getTeamsProductAndWorkspace` | query | `GET_TEAMS_PRODUCT_AND_WORKSPACE` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $productId: ID!, $workspaceId: String! | `getProductsByIds`, `getWorkspacesPagedV3` | — | `ProductQueries.testHelper.tsx`<br>`ReplaceWorkspaceFieldset.tsx` | — | — |
| `getCategories` | query | `GET_WORKSPACE_CATEGORY` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $resourceId: String, $resourceType: String, $type: String! | `getCategories` | — | `ProductListSideFilterForm.tsx`<br>`UserListSideFilterForm.tsx` | — | — |
| `getCategories` | query | `GET_WORKSPACE_CATEGORY_CLAZZ` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $resourceId: String, $resourceType: String, $type: String! | `getCategories` | — | `ProductListSideFilterForm.tsx` | — | — |
| `getProducts` | query | `PID_AND_WRK_ID_SEARCH` | `src/libs/spark-legacy/routes/admin/routes/vendorMerge/graphql/VendorMergeQueries.ts` | $q: String | `getProducts`, `getWorkspacesPagedV3` | — | `PIDOrWRKIDSelectAutoComplete.tsx` | — | — |
| `getDpciInfo` | query | `USE_DPCI_INFO` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $productId: ID! | `getProduct` | — | — | `useDpciInformation.tsx` | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `ClaimWorkspaceProductFragment` | `SPARK_Product` | `CLAIM_WORKSPACE_PRODUCT_FRAGMENT` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 58 | `index.ts` |
| `ProductBaseInfoFragment` | `SPARK_Product` | `PRODUCT_BASE_INFO_FRAGMENT` | `src/libs/product-queries/src/queries/ProductFragments.tsx` | 69 | `BomQueries.ts`<br>`ProductFilesQueries.tsx`<br>`ProductQueries.tsx`<br>`WatchlistQueries.ts` |
| `ProductRules` | `SPARK_ProductRules` | `PRODUCT_RULES_FIELDS_FRAGMENT` | `src/libs/spark-legacy/routes/admin/routes/rules/graphql/AdminRulesQueries.ts` | 20 | — |
| `ProductVendorAttributesFragment` | `ProductVendorAttributes` | `PRODUCT_VENDOR_ATTRIBUTES` | `src/libs/product-queries/src/queries/ProductFragments.tsx` | 8 | `ProductQueries.tsx` |
| `WorkspaceProductFragment` | `SPARK_Product` | `WORKSPACE_PRODUCT_FRAGMENT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | 136 | — |
| `linkProductFragment` | `SPARK_Product` | `LINK_PRODUCT_FRAGMENT` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | 6 | — |
| `productTemplateDetails` | `SPARK_Product` | `PRODUCT_TEMPLATE_DETAILS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | 23 | — |

## BOM (`bom`)

- Definitions: 19 operations (14 queries, 5 mutations) + 8 fragments
- Client libraries: `product-queries`, `spark-legacy`, `spark-ui-admin`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `addBom` | mutation | `ADD_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $sparkBom: SPARK_BomInput | `addBom` | — | `BomCloneTemplate.tsx`<br>`BomCreateTemplate.tsx` | — | — |
| `lockBom` | mutation | `LOCK_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $bomId: String! | `lockBom` | `BOM_ACCESS_FRAGMENT`, `BomAccessFragment` | `BomViewHeader.tsx` | — | — |
| `unlockBom` | mutation | `UNLOCK_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $bomId: String! | `unlockBom` | `BOM_ACCESS_FRAGMENT`, `BomAccessFragment` | `BomViewHeader.tsx` | — | — |
| `updateBom` | mutation | `UPDATE_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $sparkBom: SPARK_UpdateBomInput | `updateBom` | — | `BomViewTemplate.tsx` | — | — |
| `updateBomComponentStatus` | mutation | `UPDATE_BOM_COMPONENT_STATUS` | `src/libs/product-queries/src/queries/BomQueries.ts` | $productId: String!, $ids: [String]!, $status: SPARK_ComponentStatusInput | `updateBomComponentStatus` | — | `BomViewTemplate.tsx` | — | — |
| `searchMaterialsBom` | query | `BOM_SEARCH_MATERIALS` | `src/libs/product-queries/src/queries/BomQueries.ts` | $searchString: String, $materialType: String, $partnerIds: [ID], $internalOnly: Boolean, $excludedTypes: [String], $size: Int, $sortDirection: SPARK_SortDirection, $nestedSearchFilters: [SPARK_MaterialNestedSearchFilter] | `searchMaterialsBom` | `BUILD_FILES_FRAGMENT('SPARK_BaseMaterial')`, `BUILD_FILES_FRAGMENT('SPARK_FabricSpecification')`, `MATERIAL_DETAILS`, `MAX_BOM_SEARCH_SIZE`, `MaterialDetails`, `SPARK_BaseMaterial_Files`, `SPARK_FabricSpecification_Files` | — | — | — |
| `getBomByIds` | query | `GET_BOMS_BY_IDS` | `src/libs/product-queries/src/queries/BomQueries.ts` | $ids: [String!], $includeLiveMaterialData: Boolean | `getBomByIds` | `BOM_DETAILS_FRAGMENT`, `BomDetails` | `BomCloneTemplate.tsx` | `useBomsByIds.ts` | `BomViewTemplate.test.tsx` |
| `getBomByIds` | query | `GET_BOMS_BY_IDS_WITH_PRODUCT_INFO` | `src/libs/product-queries/src/queries/BomQueries.ts` | $ids: [String!], $includeLiveMaterialData: Boolean | `getBomByIds` | `BOM_DETAILS_FRAGMENT`, `BomDetails`, `PRODUCT_BASE_INFO_FRAGMENT`, `ProductBaseInfoFragment` | `BomViewTemplate.tsx` | — | `BomViewRoute.test.tsx`<br>`BomViewRouteEdit.test.tsx` |
| `getBomByParentId` | query | `GET_BOMS_BY_PARENT_ID` | `src/libs/product-queries/src/queries/BomQueries.ts` | $parentId: String!, $includeLiveMaterialData: Boolean | `getBomByParentId` | `BOM_FABRIC_SPEC_COMBO_DETAILS()`, `BomFabricSpecComboDetails` | — | `useBomsByParentId.ts` | — |
| `getBomElastic` | query | `GET_BOMS_FROM_ES_BY_PARENT_IDS` | `src/libs/product-queries/src/queries/BomQueries.ts` | $q: String! | `getBomElastic` | — | — | `useBomsByParentIdsFromES.ts` | — |
| `getBomByIds` | query | `GET_BOM_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | $ids: [String!] | `getBomByIds` | — | — | — | — |
| `getBomComponentStatus` | query | `GET_BOM_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | $ids: [String!] | `getBomByIds` | — | — | `useComponentStatus.ts` | `bom.ts`<br>`useComponentStatus.test.tsx` |
| `getBomMaterialTypes` | query | `GET_BOM_MATERIAL_TYPES` | `src/libs/product-queries/src/queries/BomQueries.ts` | $ids: [String] | `getBomMaterialTypes` | — | — | `useBomMaterialTypes.ts` | `useBomMaterialTypes.test.tsx` |
| `getBomPackagingMasterData` | query | `GET_BOM_PACKAGING_MASTER_DATA` | `src/libs/product-queries/src/queries/BomQueries.ts` | — | `getBomPackagingMaterialTypes`, `getBomPackagingUnitOfMeasure` | — | — | `useBomMaterialTypes.ts` | `useBomMaterialTypes.test.tsx` |
| `getBomPackagingSubstrates` | query | `GET_BOM_PACKAGING_SUBSTRATES` | `src/libs/product-queries/src/queries/BomQueries.ts` | — | `getBomPackagingSubstrates` | — | — | — | `fetchPackagingSubstrateOptions.ts`<br>`PackagingLibraryQueries.testHelper.ts` |
| `getBomStatus` | query | `GET_BOM_STATUS` | `src/libs/product-queries/src/queries/BomQueries.ts` | — | `getBomStatus` | — | — | — | `withBomStatuses.tsx` |
| `getBomDataAndImpressions` | query | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $ids: [String!], $productTemplateId: ID!, $includeLiveMaterialData: Boolean | `getBomByIds`, `searchImpressionsByProductId` | `BOM_DETAILS_FRAGMENT`, `BomDetails`, `IMPRESSION_FRAGMENT()`, `ImpressionFragment` | `ProductTemplateBomExpandedView.tsx` | — | — |
| `getComboSupplierForBom` | query | `GET_COMBINATION_SUPPLIER_FOR_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $comboId: String, $partnerIds: [ID] | `getComboSupplierForBom` | `BOM_COMBO_SUPPLIER_FRAGMENT`, `BomComboSupplier` | — | — | `mapCombinationDataToMaterial.ts` |
| `getValidSuppliersForBom` | query | `GET_VALID_SUPPLIERS_FOR_BOM` | `src/libs/product-queries/src/queries/BomQueries.ts` | $merchVendorIds: [ID]! | `getValidRawMaterialSuppliersForBom`, `getValidTrimSuppliersForBom` | — | `BomForm.tsx`<br>`PackagingBomForm.tsx` | — | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `BaseImpressionDetails` | `SPARK_BomBaseImpressionDetails` | `BASE_IMPRESSION_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 4 | — |
| `BomAccessFragment` | `SPARK_Bom` | `BOM_ACCESS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 10 | — |
| `BomComboSupplier` | `SPARK_BomComboSupplier` | `BOM_COMBO_SUPPLIER_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 22 | — |
| `BomDetails` | `SPARK_Bom` | `BOM_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 225 | `ProductTemplateQueries.tsx` |
| `FabricLibraryImpressionDetails` | `SPARK_BomFabricLibraryImpressionDetails` | `FABRIC_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 4 | — |
| `TrimLibraryImpressionDetails` | `SPARK_BomTrimLibraryImpressionDetails` | `TRIM_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 14 | — |
| `TrimZipperLibraryImpressionDetails` | `SPARK_BomTrimZipperLibraryImpressionDetails` | `TRIM_ZIPPER_LIBRARY_IMPRESSION_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 18 | — |
| `WashLibraryImpressionDetails` | `SPARK_BomWashLibraryImpressionDetails` | `WASH_IMPRESSION_DETAILS_FRAGMENT` | `src/libs/product-queries/src/queries/BomQueries.ts` | 4 | — |

## Measurement (`measurement`)

- Definitions: 15 operations (9 queries, 6 mutations) + 3 fragments
- Client libraries: `product-common`, `spark-legacy`, `spark-ui-admin`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `addTightFit` | mutation | `ADD_TIGHT_FIT` | `src/libs/product-common/src/queries/TightFitQueries.tsx` | $tightFit: SPARK_TightFitInput | `addTightFit` | — | `TightFitTemplateNewLayout.tsx` | — | `index.ts` |
| `deleteSampleMeasurementSet` | mutation | `DELETE_SAMPLE_MEASUREMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $sampleId: String! | `deleteSampleMeasurementSet` | — | `SampleCompare.tsx`<br>`Sample.tsx` | — | `index.ts` |
| `lockMeasurementSet` | mutation | `LOCK_MEASUREMENT_SET` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $measurementSetId: ID! | `lockMeasurementSet` | `MEASUREMENT_FIELDS_FRAGMENT`, `measurementFieldsFragment` | `MeasurementSetTemplate.tsx` | — | `index.ts` |
| `putSampleMeasurementSet` | mutation | `PUT_SAMPLE_MEASUREMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $sampleMeasurementSet: SPARK_SampleMeasurementSetInput! | `putSampleMeasurementSet` | `SAMPLE_MEASUREMENT_FRAGMENT`, `SampleMeasurementFragment` | `SampleCompare.tsx`<br>`SampleNew.tsx`<br>`Sample.tsx`<br>`SampleMeasurementEditTemplate.tsx` | — | `index.ts` |
| `unlockMeasurementSet` | mutation | `UNLOCK_MEASUREMENT_SET` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $measurementSetId: ID! | `unlockMeasurementSet` | `MEASUREMENT_FIELDS_FRAGMENT`, `measurementFieldsFragment` | `MeasurementSetTemplate.tsx` | — | `index.ts` |
| `updateTightFit` | mutation | `UPDATE_TIGHT_FIT` | `src/libs/product-common/src/queries/TightFitQueries.tsx` | $tightFit: SPARK_TightFitInput | `updateTightFit` | `TIGHT_FIT_FRAGMENT`, `tightFitFragment` | `TightFitTemplateEditLayout.tsx` | — | `index.ts` |
| `getMeasurements` | query | `GET_MEASUREMENTS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $resourceId: String, $calculated: Boolean, $businessPartnerIds: [String], $mustHaveRows: Boolean | `getMeasurements` | `MEASUREMENT_FIELDS_FRAGMENT`, `measurementFieldsFragment` | `ImportMeasurementSet.tsx` | — | `index.ts` |
| `getMeasurementsMetaData` | query | `GET_MEASUREMENTS_META_DATA` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | — | `getUnitsOfMeasure`, `getThicknessUnitsOfMeasure`, `getSections` | — | — | — | `MeasurementQueries.testHelper.ts`<br>`index.ts`<br>`withMeasurementsMetaData.tsx` |
| `getMeasurementByIds` | query | `GET_MEASUREMENT_BY_IDS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | $ids: [String!] | `getMeasurementByIds` | `MEASUREMENT_FIELDS_FRAGMENT`, `measurementFieldsFragment` | — | — | — |
| `getMeasurementComponentStatus` | query | `GET_MEASUREMENT_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | $ids: [String!] | `getMeasurementByIds` | — | — | `useComponentStatus.ts` | `useComponentStatus.test.tsx` |
| `getMeasurementByIds` | query | `GET_MEASUREMENT_SET_BY_ID` | `src/libs/spark-ui-admin/src/graphql/uiAdminQueries.ts` | $ids: [String!] | `getMeasurementByIds` | — | — | — | — |
| `getMeasurementSetStatus` | query | `GET_MEASUREMENT_SET_STATUS` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | — | `getMeasurementSetStatus` | — | `TightFitTemplateEditLayout.tsx` | — | `index.ts` |
| `getMeasurementsElastic` | query | `GET_PRODUCT_TEMPLATE_MEASUREMENTS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $resourceId: String | `getMeasurementsElastic` | `MEASUREMENT_TEMPLATE_FRAGMENT`, `SIZE_TEMPLATE_FRAGMENT_WITH_ROWS`, `TIGHT_FIT_FRAGMENT`, `measurementTemplateFragment`, `sizeTemplateFragmentWithRows`, `tightFitFragment` | — | — | — |
| `getTightFits` | query | `GET_TIGHT_FITS` | `src/libs/product-common/src/queries/TightFitQueries.tsx` | $ids: [String], $name: String, $statusIds: [Int], $brandIds: [Int], $divisionIds: [Int], $departmentIds: [Int] | `getTightFits` | `TIGHT_FIT_FRAGMENT`, `tightFitFragment` | — | — | — |
| `getUnitsOfMeasure` | query | `GET_UNITS_OF_MEASURE` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | — | `getUnitsOfMeasure` | — | — | — | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `SampleMeasurementFragment` | `SPARK_SampleMeasurementSet` | `SAMPLE_MEASUREMENT_FRAGMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 34 | `index.ts`<br>`CombinationSamplesBulkEvaluate.tsx` |
| `measurementFieldsFragment` | `SPARK_Measurements` | `MEASUREMENT_FIELDS_FRAGMENT` | `src/libs/product-common/src/queries/MeasurementQueries.tsx` | 112 | `index.ts` |
| `tightFitFragment` | `SPARK_TightFit` | `TIGHT_FIT_FRAGMENT` | `src/libs/product-common/src/queries/TightFitQueries.tsx` | 71 | — |

## Product Details (`productDetails`)

- Definitions: 7 operations (2 queries, 5 mutations) + 1 fragments
- Client libraries: `product-details`, `spark-legacy`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `cloneFilesForProductDetails` | mutation | `CLONE_PDTL_ATTACHMENTS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $attachmentIds: [String!], $cloneReference: [PDTLAttachmentCloneRef] | `cloneFilesForProductDetails` | — | `ProductDetailClone.tsx` | — | — |
| `createProductDetailsSet` | mutation | `CREATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $productDetails: productDetailSetInput | `createProductDetailsSet` | — | `ProductDetailsSetNew.tsx`<br>`ProductDetailClone.tsx` | — | — |
| `productDetailLockUnlock` | mutation | `PRODUCT_DETAILS_LOCK_UNLOCK` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $constructionSetId: ID!, $isLock: Boolean | `productDetailLockUnlock` | — | `ProductDetailsViewTemplate.tsx` | — | — |
| `updateProductDetailsSet` | mutation | `UPDATE_PRODUCT_DETAILS_SET` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $productDetailsId: ID!, $productDetails: productDetailSetUpdateInput | `updateProductDetailsSet` | — | `ProductDetailsViewTemplate.tsx`<br>`ProductTemplateProductDetailsEdit.tsx` | — | `index.ts` |
| `updateProductDetailComponentStatus` | mutation | `UPDATE_PRODUCT_DETAIL_COMPONENT_STATUS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $productId: String!, $ids: [String]!, $status: SPARK_ComponentStatusInput | `updateProductDetailComponentStatus` | — | `ProductDetailsViewTemplate.tsx` | — | — |
| `getProductDetailsById` | query | `GET_PRODUCT_DETAILS_SET_BY_IDS` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | $ids: [String] | `getProductDetailsById` | `PRODUCT_DETAILS_DATA_FRAGMENT`, `ProductDetailsDataFragment` | — | — | — |
| `getProductDetailComponentStatus` | query | `GET_PROUCT_DETAIL_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | $ids: [String!] | `getProductDetailsById` | — | — | `useComponentStatus.ts` | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `ProductDetailsDataFragment` | `SPARK_ProductDetails` | `PRODUCT_DETAILS_DATA_FRAGMENT` | `src/libs/product-details/src/graphql/SpecificationQueries.ts` | 107 | — |

## Packaging (`packaging`)

- Definitions: 21 operations (12 queries, 9 mutations) + 1 fragments
- Client libraries: `product-common`, `product-packaging`, `spark-legacy`, `spark-packaging-base`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `addPackaging` | mutation | `ADD_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $sparkPackaging: SPARK_PackagingInput! | `addPackaging` | — | `PackagingDetailsCloneTemplate.tsx`<br>`PackagingDetailsNewTemplate.tsx` | — | — |
| `bulkAddPackagings` | mutation | `BULK_ADD_PACKAGING_DETAILS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $bulkPackagingInput: SPARK_PackagingBulkInput! | `bulkAddPackagings` | — | `PackagingBulkCreate.tsx` | — | — |
| `bulkUpdatePackagings` | mutation | `BULK_UPDATE_PACKAGING_DETAILS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $bulkPackagingInput: SPARK_PackagingBulkInput! | `bulkUpdatePackagings` | — | `PackagingBulkUpdate.tsx` | — | — |
| `evaluateDieline` | mutation | `EVALUATE_DIELINE` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $dielineId: String!, $dielineEvaluation: SPARK_DielineEvaluationInput | `evaluateDieline` | — | `PackagingEvaluationButton.tsx` | — | — |
| `lockPackaging` | mutation | `LOCK_PACKAGING` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String! | `lockPackaging` | — | `PackagingDetailsTemplate.tsx` | — | — |
| `exportPackaging` | mutation | `PACKAGING_EXCEL_EXPORT` | `src/libs/product-common/src/queries/WorkspaceProductsQueries.ts` | $workspaceId: String!, $workspaceDescription: String!, $ids: [String] | `exportPackaging` | — | `WorkspaceDownloadDropdown.tsx` | — | — |
| `unlockPackaging` | mutation | `UNLOCK_PACKAGING` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String! | `unlockPackaging` | — | `PackagingDetailsTemplate.tsx` | — | — |
| `updatePackagingComponentStatus` | mutation | `UPDATE_PACKAGING_COMPONENT_STATUS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $productId: String!, $ids: [String]!, $status: SPARK_ComponentStatusInput | `updatePackagingComponentStatus` | — | `PackagingDetailsTemplate.tsx` | — | — |
| `updatePackaging` | mutation | `UPDATE_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String!, $sparkPackaging: SPARK_PackagingInput! | `updatePackaging` | — | `PackagingDetailsTemplate.tsx` | — | — |
| `getDielines` | query | `GET_DIELINES` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $printerIds: [String], $packagingIds: [String], $parentIds: [String], $statusIds: [Int] | `getDielines` | — | — | `useFetchDielines.ts` | — |
| `getDielineEvaluationStatuses` | query | `GET_DIELINE_STATUS_LIST` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | — | `getDielineEvaluationStatuses` | — | — | `useFetchDielineStatusList.tsx` | — |
| `getPackagingComponentStatus` | query | `GET_PACKAGING_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | $packagingId: String! | `getPackagingById` | — | — | `useComponentStatus.ts` | `useComponentStatus.test.tsx` |
| `getCountries` | query | `GET_PACKAGING_COUNTRIES` | `src/libs/spark-packaging-base/src/graphql/PackagingCountryQueries.ts` | $codes: [String] | `getCountries` | — | — | `usePackagingCountries.ts` | — |
| `getPackagingById` | query | `GET_PACKAGING_DETAIL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String! | `getPackagingById` | `GET_PACKAGING_DETAIL_FRAGMENT(false)`, `PackagingDetailsFragment` | — | — | — |
| `getPackagings` | query | `GET_PACKAGING_DETAILS_BY_PARENTS` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $parentIds: [String]!, $workspaceIds: [String] | `getPackagings` | `GET_PACKAGING_DETAIL_FRAGMENT()`, `PackagingDetailsFragment` | — | — | — |
| `getPackagings` | query | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $parentIds: [String]!, $workspaceIds: [String] | `getPackagings` | `GET_PACKAGING_DETAIL_FRAGMENT(true)`, `PackagingDetailsFragment` | — | `usePackagingDetailsByParent.tsx` | `index.ts`<br>`PackagingDetailsQueries.ts` |
| `getPackagings` | query | `GET_PACKAGING_DETAILS_BY_PARENTS_INTERNAL` | `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts` | $parentIds: [String]!, $workspaceIds: [String] | `getPackagings` | `GET_PACKAGING_DETAIL_BASE_FRAGMENT(true)`, `PackagingDetailsBaseFragment` | — | `usePackagingDetailsByParent.tsx` | `PackagingDetailsQueries.ts`<br>`index.ts` |
| `getPackagingById` | query | `GET_PACKAGING_DETAIL_WITH_INTERNAL_DATA` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String! | `getPackagingById` | `GET_PACKAGING_DETAIL_FRAGMENT(true)`, `PackagingDetailsFragment` | — | `usePackagingDetail.tsx` | `index.ts`<br>`usePackagingDetail.test.tsx` |
| `getPackagingFieldValuesByType` | query | `GET_PACKAGING_FIELD_VALUES_BY_TYPE` | `src/libs/spark-packaging-base/src/graphql/PackagingDetailsQueries.ts` | $type: String! | `getPackagingFieldValuesByType` | — | — | `usePackagingDetailsEnums.ts` | `PackagingDetailsQueries.testhelper.ts`<br>`index.ts`<br>`index.ts` |
| `getPackagingPacketsInformation` | query | `GET_PACKAGING_PACKETS_INFORMATION` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingIds: [String], $workspaceIds: [String], $partnerIds: [String] | `getPackagings` | `PACKAGING_PACKET_INFORMATION_FRAGMENT`, `packagePacketInformation` | `BulkGeneratePackagingPacketModal.tsx` | — | `index.ts`<br>`product.ts` |
| `getPackagingPacketInformation` | query | `GET_PACKAGING_PACKET_INFORMATION` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | $packagingId: String! | `getPackagingById` | `PACKAGING_PACKET_INFORMATION_FRAGMENT`, `packagePacketInformation` | — | — | `PackagingPacketUtils.ts` |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `packagePacketInformation` | `SPARK_Packaging` | `PACKAGING_PACKET_INFORMATION_FRAGMENT` | `src/libs/product-packaging/src/graphql/PackagingDetailsQueries.ts` | 49 | — |

## Watchlist (`watchlist`)

- Definitions: 5 operations (2 queries, 3 mutations) + 1 fragments
- Client libraries: `watchlist`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `cloneFilesForWatchlist` | mutation | `CLONE_WATCHLIST_ATTACHMENTS` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | $attachmentIds: [String!], $cloneReference: [WatchlistAttachmentCloneRef] | `cloneFilesForWatchlist` | — | `WatchlistCloneTemplate.tsx` | — | `WatchlistCloneRoute.test.tsx` |
| `createWatchlistEntries` | mutation | `CREATE_WATCHLIST_ENTRIES` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | $watchlistEntries: [SPARK_WatchlistInput!]! | `createWatchlistEntries` | — | — | — | — |
| `updateWatchlistEntries` | mutation | `UPDATE_WATCHLIST_ENTRIES` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | $watchlistEntries: [SPARK_WatchlistInput!]! | `updateWatchlistEntries` | — | `WatchlistBulkUpdate.tsx`<br>`WatchlistEditTemplate.tsx` | — | `WatchlistEditRoute.test.tsx` |
| `getWatchlistByIds` | query | `GET_WATCHLIST_BY_IDS` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | $ids: [String!], $q: String, $skipPartners: Boolean! | `getWatchlistByIds` | `PRODUCT_BASE_INFO_FRAGMENT`, `WATCHLIST_FORM_CONSTANTS`, `WATCHLIST_FRAGMENT`, `WATCHLIST_PARTICIPANT_FRAGMENT`, `WatchlistFields` | `WatchlistCloneTemplate.tsx`<br>`WatchlistEditTemplate.tsx`<br>`WatchlistViewTemplate.tsx` | — | — |
| `getWatchlistForBulkUpdate` | query | `GET_WATCHLIST_FOR_BULK_UPDATE` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | $q: String, $query: String, $filter: [String], $workspaceId: ID!, $skipPartners: Boolean! | `getWatchlistByFilter`, `getWorkspaceV2` | `PRODUCT_BASE_INFO_FRAGMENT`, `WATCHLIST_FORM_CONSTANTS`, `WATCHLIST_FRAGMENT`, `WATCHLIST_PARTICIPANT_FRAGMENT`, `WatchlistFields` | `WatchlistBulkUpdate.tsx` | — | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `WatchlistFields` | `SPARK_Watchlist` | `WATCHLIST_FRAGMENT` | `src/libs/watchlist/src/graphql/WatchlistQueries.ts` | 45 | — |

## Impression (`impression`)

- Definitions: 2 operations (2 queries, 0 mutations) + 0 fragments
- Client libraries: `product-queries`, `spark-legacy`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `getBomDataAndImpressions` | query | `GET_BOM_TEMPLATES_AND_IMPRESSIONS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $ids: [String!], $productTemplateId: ID!, $includeLiveMaterialData: Boolean | `getBomByIds`, `searchImpressionsByProductId` | `BOM_DETAILS_FRAGMENT`, `BomDetails`, `IMPRESSION_FRAGMENT()`, `ImpressionFragment` | `ProductTemplateBomExpandedView.tsx` | — | — |
| `getCarryForwardFormData` | query | `GET_CARRY_FORWARD_FORM_DATA` | `src/libs/product-queries/src/queries/ProductQueries.tsx` | $id: ID!, $workspaceId: ID, $strWorkspaceId: String | `searchImpressionsByProductId`, `getProduct` | `PRODUCT_COMPONENT_FRAGMENT`, `PRODUCT_FULL_TEAM_FRAGMENT`, `ProductFullTeamFragment`, `VMM_BUSINESS_PARTNER_ON_PRODUCT`, `VmmBusinessPartnerOnProduct`, `productComponentFragment` | `ProductQueries.testHelper.tsx`<br>`ProductCarryForwardModal.tsx`<br>`WorkspaceCarryForwardSpecsForm.tsx` | — | — |

## Claims (`claims`)

- Definitions: 14 operations (8 queries, 6 mutations) + 2 fragments
- Client libraries: `claims`, `spark-legacy`, `spark-ui-admin`

| Operation | Kind | Const | Client file | Variables | Root fields | Fragments | Components | Hooks | Other consumers |
|---|---|---|---|---|---|---|---|---|---|
| `createClaim` | mutation | `ADD_CLAIMS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $sparkClaim: SPARK_ClaimsInput | `createClaim` | — | `ClaimNewTemplate.tsx`<br>`ProductTemplateClaimClone.tsx` | — | `index.ts`<br>`fabricClaimsUtils.ts` |
| `bulkUpdateClaim` | mutation | `BULK_UPDATE_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $sparkClaim: SPARK_BulkClaimsUpdateInput | `bulkUpdateClaim` | — | `ClaimBulkUpdate.tsx` | — | `index.ts` |
| `lockClaim` | mutation | `LOCK_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $claimId: String! | `lockClaim` | — | `ClaimViewTemplate.tsx` | — | `index.ts` |
| `requestClaimExport` | mutation | `REQUEST_REPORT` | `src/libs/spark-ui-admin/src/graphql/uiAdminMutations.ts` | — | `requestClaimExport` | — | — | — | — |
| `unlockClaim` | mutation | `UNLOCK_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $claimId: String! | `unlockClaim` | — | `ClaimViewTemplate.tsx` | — | `index.ts` |
| `updateClaim` | mutation | `UPDATE_CLAIM` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $sparkClaim: SPARK_ClaimsUpdateInput | `updateClaim` | — | `ClaimViewTemplate.tsx`<br>`ProductTemplateClaimEdit.tsx` | — | `index.ts`<br>`fabricClaimsUtils.ts` |
| `getClaims` | query | `GET_CLAIMS_AND_CHANNELS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $parentHumanId: String, $claimHumanIds: [String], $partnerIds: [String] | `getClaims`, `getCommunicationChannels`, `getAllClaimsAbout` | `CLAIM_DETAILS_FRAGMENT`, `ClaimDetailsFragment` | `ClaimNewTemplate.tsx`<br>`ImportProductDetailsSection.tsx` | — | `index.ts` |
| `getClaimByIds` | query | `GET_CLAIM_BY_ID` | `(local) ClientCallingGqlQueries/claims__ClaimQueries.txt` | $claimHumanIds: [String] | `getClaimByIds`, `getCommunicationChannels`, `getAllClaimsAbout` | `FULL_CLAIM_DETAILS(includeWorkspaces)`, `FullClaimDetailsFragment` | — | — | — |
| `getClaimComponentStatus` | query | `GET_CLAIM_COMPONENT_STATUS` | `src/libs/spark-legacy/customHooks/graphql/customHooksQueries.ts` | $ids: [String!] | `getClaimByIds` | — | — | `useComponentStatus.ts` | — |
| `breadcrumbClaims` | query | `GET_CLAIM_CRUMB` | `src/libs/spark-legacy/components/breadcrumbs/graphql/BreadcrumbQueries.ts` | $id: [String] | `getClaimByIds` | — | `BreadcrumbClaim.tsx` | — | `BreadcrumbClaim.test.tsx` |
| `getClaimByIds` | query | `GET_CLAIM_TEMPLATE_BY_ID` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $claimHumanIds: [String] | `getClaimByIds` | `FULL_CLAIM_DETAILS(true)`, `FullClaimDetailsFragment` | `ProductTemplateClaimClone.tsx`<br>`ProductTemplateClaimEdit.tsx` | — | — |
| `getComponentVersion` | query | `GET_CLAIM_VERSION` | `src/libs/claims/src/graphql/ClaimQueries.ts` | $id: String!, $version: Int! | `getComponentVersion`, `getCommunicationChannels` | `FULL_CLAIM_DETAILS(true)`, `FullClaimDetailsFragment` | — | `useClaimQuery.ts` | `index.ts`<br>`ClaimViewRoute.test.tsx` |
| `getCommunicationChannels` | query | `GET_COMMUNICATION_CHANNELLS` | `src/libs/claims/src/graphql/ClaimQueries.ts` | — | `getCommunicationChannels` | — | — | — | `index.ts` |
| `getClaims` | query | `GET_PRODUCT_TEMPLATE_CLAIMS` | `src/libs/spark-legacy/routes/templateLibrary/graphql/ProductTemplateQueries.tsx` | $parentHumanId: String | `getClaims` | `CLAIM_DETAILS_FRAGMENT`, `ClaimDetailsFragment` | `ProductTemplateClaimExpandedView.tsx` | — | — |

### Fragments

| Fragment | On type | Const | Client file | Fields | Used in |
|---|---|---|---|---|---|
| `ClaimDetailsFragment` | `SPARK_Claims` | `CLAIM_DETAILS_FRAGMENT` | `src/libs/claims/src/graphql/ClaimQueries.ts` | 18 | `index.ts`<br>`ProductTemplateQueries.tsx` |
| `FullClaimDetailsFragment` | `SPARK_Claims` | `FULL_CLAIM_DETAILS` | `(local) ClientCallingGqlQueries/claims__ClaimQueries.txt` | 78 | — |
