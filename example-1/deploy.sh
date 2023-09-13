resourceGroupName=myresourcegroup18400398
appName=appservicedf1ddfd0
zipFile=source.zip

# az webapp deployment source config-zip --resource-group $resourceGroupName --name $appName --src $zipFile

az webapp config set --resource-group $resourceGroupName --name $appName --startup-file start.sh
az webapp deploy \
    --name $appName \
    --resource-group $resourceGroupName \
    --src-path $zipFile