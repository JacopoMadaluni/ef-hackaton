
import * as pulumi from "@pulumi/pulumi";
import * as azure from "@pulumi/azure";
import * as azuread from "@pulumi/azuread";
import * as random from "@pulumi/random";

// Create an Azure Resource Group
const resourceGroup = new azure.core.ResourceGroup("resourceGroup", {
    location: "UK South",
});

// Create an Azure Storage Account
const storageAccount = new azure.storage.Account("storageAccount", {
    resourceGroupName: resourceGroup.name,
    accountTier: "Standard",
    accountReplicationType: "LRS",
});

// Create an Azure Storage Container
const storageContainer = new azure.storage.Container("storageContainer", {
    name: "container",
    storageAccountName: storageAccount.name,
    containerAccessType: "blob",
});

// Create an Azure App Service Plan
const appServicePlan = new azure.appservice.Plan("appServicePlan", {
    resourceGroupName: resourceGroup.name,
    kind: "App",
    sku: {
        tier: "Basic",
        size: "B1",
    },
});

// Create an Azure App Service
const appService = new azure.appservice.AppService("appService", {
    resourceGroupName: resourceGroup.name,
    appServicePlanId: appServicePlan.id,
    appSettings: {
        "WEBSITE_RUN_FROM_PACKAGE": "https://github.com/user/repo/releases/download/v1.0.0/app.zip",
        "STORAGE_CONNECTION_STRING": storageAccount.primaryConnectionString,
        "CONTAINER": storageContainer.name,
    },
    siteConfig: {
        alwaysOn: true,
        http2Enabled: true,
        nodeVersion: "16.13.0",
    },
});

// Export the connection string for the storage account
export const connectionString = storageAccount.primaryConnectionString;
