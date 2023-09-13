import pulumi


import os
from pulumi_azure_native import resources, web, storage

PREFIX = "efhack"

# Create an Azure Resource Group
resource_group = resources.ResourceGroup(PREFIX + 'rg')

# Create an Azure storage account
storage_account = storage.StorageAccount(PREFIX + 'sa',
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2)

# Create a Blob container
blob_container = storage.BlobContainer(PREFIX +'bc',
    account_name = storage_account.name,
    public_access = storage.PublicAccess.NONE,
    resource_group_name = resource_group.name)

# Create a blob with the App code
blob = storage.Blob(PREFIX +'app_code',
    resource_group_name = resource_group.name,
    account_name = storage_account.name,
    container_name = blob_container.name,
    type = storage.BlobType.BLOCK,
    source = pulumi.FileArchive(os.path.join(os.path.dirname(__file__), "../source.zip")) 
    )


def list_keys(args):
  print(args)
  return storage.list_storage_account_keys(args[1], None, args[0])


# Get the storage account (primary) access key
account_keys = pulumi.Output.all(
  resource_group.name, 
  storage_account.name
).apply(
  lambda args: list_keys(args)
).apply(lambda ak: ak.keys[0].value)


# Create connection string for the storage account
connection_string = account_keys.apply(
    lambda accountKeys: f"DefaultEndpointsProtocol=https;AccountName={storage_account.name};AccountKey={accountKeys};EndpointSuffix=core.windows.net")

# Create an App Service Plan
plan = web.AppServicePlan('asp',
    resource_group_name=resource_group.name,
    kind='App',
    sku=web.SkuDescriptionArgs(
        tier='BASIC',
        name='B1',
    ))

# Create an App Service
app = web.WebApp('app',
    resource_group_name=resource_group.name,
    server_farm_id=plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(name='WEBSITE_RUN_FROM_PACKAGE', 
            value=pulumi.Output.all(storage_account.name, blob_container.name, blob.name).apply(
            lambda args: f"https://{args[0]}.blob.core.windows.net/{args[1]}/{args[2]}")),
            web.NameValuePairArgs(name = 'AzureWebJobsStorage', value = connection_string),
        ],
    ))

# Export the Web App hostname
pulumi.export('hostname', app.default_host_name)