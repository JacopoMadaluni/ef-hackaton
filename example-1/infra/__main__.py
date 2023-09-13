# import pulumi


# import os
# from pulumi_azure_native import resources, web, storage, authorization
# import pulumi_azure as azure

# PREFIX = "efhack"

# # Create an Azure Resource Group
# resource_group = resources.ResourceGroup(PREFIX + 'rg')

# # Create an Azure storage account
# storage_account = storage.StorageAccount(PREFIX + 'sa',
#     resource_group_name=resource_group.name,
#     sku=storage.SkuArgs(
#         name=storage.SkuName.STANDARD_LRS,
#     ),
#     kind=storage.Kind.STORAGE_V2)

# # Create a Blob container
# blob_container = storage.BlobContainer(PREFIX +'bc',
#     account_name = storage_account.name,
#     public_access = storage.PublicAccess.CONTAINER,
#     resource_group_name = resource_group.name)

# # Create a blob with the App code
# blob = storage.Blob('source.zip',
#     resource_group_name = resource_group.name,
#     account_name = storage_account.name,
#     container_name = blob_container.name,
#     type = storage.BlobType.BLOCK,
#     source = pulumi.FileArchive(os.path.join(os.path.dirname(__file__), "../source.zip")) 
#     )


# def list_keys(args):
#   print(args)
#   return storage.list_storage_account_keys(args[1], None, args[0])


# # Get the storage account (primary) access key
# account_keys = pulumi.Output.all(
#   resource_group.name, 
#   storage_account.name
# ).apply(
#   lambda args: list_keys(args)
# ).apply(lambda ak: ak.keys[0].value)


# # Create connection string for the storage account
# connection_string = account_keys.apply(
#     lambda accountKeys: f"DefaultEndpointsProtocol=https;AccountName={storage_account.name};AccountKey={accountKeys};EndpointSuffix=core.windows.net")

# # Create an App Service Plan
# plan = web.AppServicePlan('asp',
#     resource_group_name=resource_group.name,
#     kind='App',
#     sku=web.SkuDescriptionArgs(
#         tier='BASIC',
#         name='B1',
#     ))

# # Assign a system-assigned managed identity to the App Service
# identity = web.ManagedServiceIdentityArgs(
#     type = web.ManagedServiceIdentityType.SYSTEM_ASSIGNED
# )



# # Define App Service
# app = web.WebApp('web-app',
#     resource_group_name=resource_group.name,
#     location=resource_group.location,
#     server_farm_id=plan.id,
#     site_config=web.SiteConfigArgs(
#         app_settings=[
#             web.NameValuePairArgs(name='WEBSITES_ENABLE_APP_SERVICE_STORAGE', value='false'),
#             web.NameValuePairArgs(name='WEBSITE_RUN_FROM_PACKAGE', value='1')
#         ]
#     ))

# # # Create a custom role with full access
# # custom_role = authorization.RoleDefinition('full-access-role',
# #     role_name='Full Access Role',
# #     scope=storage_account.id,
# #     assignable_scopes=[storage_account.id],  # Add the assignable_scopes parameter
# #     permissions=[azure.authorization.RoleDefinitionPermissionArgs(
# #         actions=["*"],    # Full access
# #         not_actions=[],
# #         data_actions=[],  # access to data in the storage account
# #         not_data_actions=[])
# #     ])
        
# # # Assign the managed identity to the custom role for the storage account
# # role_assignment = authorization.RoleAssignment('role_assignment',
# #     role_definition_id=custom_role.id,
# #     principal_id=app.identity.apply(lambda identity: identity.principal_id),
# #     scope=storage_account.id)




# # Export the app service principal id and storage account id
# # pulumi.export('principal_id', app.identity.apply(lambda identity: identity.principal_id))
# pulumi.export('storage_account_id', storage_account.id)

# # Export the Web App hostname
# pulumi.export('hostname', app.default_host_name)












# GPT +================================
import pulumi
import pulumi_azure as azure
import pulumi_azure_native as azure_native

config = pulumi.Config()

# Create an Azure Resource Group
resource_group = azure_native.resources.ResourceGroup('myresourcegroup')

# Create an Azure Storage Account
storage_account = azure.storage.Account('mystorageaccount',
    resource_group_name=resource_group.name,
    account_tier='Standard',
    account_replication_type='LRS',
)

# Create an Azure App Service Plan
plan = azure_native.web.AppServicePlan('myserviceplan',
    location=resource_group.location,
    resource_group_name=resource_group.name,
    kind="Linux",
    reserved=True,
    sku=azure_native.web.SkuDescriptionArgs(
        tier="Basic",
        name="B1",
    ),
)


# Create an App Service
app = azure.appservice.AppService('appservice',
    resource_group_name=resource_group.name,
    app_service_plan_id=plan.id,
    app_settings={
        # 'WEBSITE_RUN_FROM_PACKAGE': "1",
        'FUNCTIONS_WORKER_RUNTIME': "python",
    }
)

# Export the name of the App Service
pulumi.export('app_service_name', app.name)
pulumi.export('resource_group.name', resource_group.name)