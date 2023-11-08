# azure-bus-python
Secret Needed

Either create it manually as shown below
```
az servicebus queue authorization-rule create --resource-group <name> --namespace-name <name> --queue-name <nme> --name <name> --rights Listen
```
```
az servicebus queue authorization-rule keys list --resource-group <resource-group-name> --namespace-name <namespace-name> --queue-name orders --name order-consumer
```
```
oc create secret generic namespace-secret --from-literal=connection="Endpoint=sb://<endpoint>;SharedAccessKeyName=<sa-name>;SharedAccessKey=<primary-key>"
```

or allow External Secret Operator pull it in.
If using an external secret operator you will need the initial service principal to access the Azure key vault.

```
az ad sp create-for-rbac --name myKeyVaultServicePrincipal --role reader --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group-name>
```

```
oc create secret docker-registry dockerconfigjson --docker-server=quay.io --docker-username=<username> --docker-password=<pass> --docker-email=test@acme.com -n hello-chris
```