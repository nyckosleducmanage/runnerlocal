# Github Runner R4P

This is a base Github runner image from Summerwind base image.

## Tools added
- Ansible
- Azure CLI
- Bicep
- Helm
- Kubectl
- Node Exporter
- OpenSSH Client
- PowerShell
- Python

By Nicolas Leduc


## Secrets Key Vault

[![Deploy Secrets Key Vault][img_secrets_keyvault]][wkf_secrets_keyvault]

This [`workflow`](.github/workflows/deploy-secrets-keyvault.yml) deploys IaC in [`secrets-infra`](secrets-infra) folder for the key vault that will contain secrets synchronized from Application CyberArk.  These secrets are used in workflows.

The workflow takes no parameters and runs on standard `ubuntu-latest`-labeled runner.

It deploys [bicep](secrets-infra/main.bicep) with parameters from Github variables from environment `g2s-dev-01`:

- `MANAGEMENT_DEVOPS_GROUP_OBJECT_ID`
- `MANAGEMENT_KV_SP_OBJECT_ID`
- `KEYVAULT_PRIVATE_ENDPOINT_SUBNET_ID`

Some other parameters are hardcoded, so keyvault is named `kv-g2s-secrets` and is deployed in resource group `g2s-dev-secrets`, region `westheurope`.

Target subscription and Azure identity for deployment are as usual taken from Github variables

- `CLIENT_ID`
- `SUBSCRIPTION_ID`
- `TENANT_ID`

[wkf_secrets_keyvault]: https://github.com/nyckosleducmanage/runnerlocal/actions/workflows/deploy-secrets-keyvault.yml
