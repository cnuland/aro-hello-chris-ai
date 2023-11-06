# azure-bus-python
Secret Needed

Either create it manually as shown below
```
oc create secret generic namespace-secret --from-literal=connection="Endpoint=sb://<endpoint>;SharedAccessKeyName=<sa-name>;SharedAccessKey=<primary-key>"
```

or allow External Secret Operator pull it in.
If using an external secret operator you will need the initial service principal to access the Azure key vault.

```
az ad sp create-for-rbac --name myKeyVaultServicePrincipal --role reader --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group-name>
```