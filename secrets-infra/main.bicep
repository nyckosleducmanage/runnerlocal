param keyVaultName string
param location string
param devopsGroupObjectId string
param keyvaultServicePrincipalObjectId string
param privateEndpointSubnetId string
param tagG2SOwner string
param tagG2SVersion string
param tagG2SEnvironment string

var commonResourceBaseTags = {
  g2s_service: 'G2S'
  'g2s_service-id': '4bb74e51-e33b-40b3-9148-b4f6a2ee2e15'
  g2s_owner: tagG2SOwner
  'G2S_first-line-support': 'g2s-devops'
  g2s_environment: tagG2SEnvironment
  managed_by: 'Nicolas Leduc'
  g2s_component: 'foundation'
  g2s_version: tagG2SVersion
  g2s_instance: 'mgmt'
  'g2s_operational-owner': 'g2s-devops'
}

resource vault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  tags: union(commonResourceBaseTags, { data_classification: 'other' })
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    enablePurgeProtection: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
  }
}

resource privateEndpointKv 'Microsoft.Network/privateEndpoints@2022-09-01' = {
  name: 'pe-${vault.name}'
  location: location
  tags: union(commonResourceBaseTags, { data_classification: 'other' })
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'link-pe-${vault.name}'
        properties: {
          privateLinkServiceId: vault.id
          groupIds: [
            'vault'
          ]
        }
      }
    ]
  }
}

var keyVaultAdminRoleId = '00482a5a-887f-4fb3-b363-3b7fe8e74483'
resource devopsIsKeyVaultAdmin 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(vault.id, devopsGroupObjectId, keyVaultAdminRoleId)
  scope: vault
  properties: {
    principalId: devopsGroupObjectId
    roleDefinitionId: tenantResourceId('Microsoft.Authorization/roleDefinitions', keyVaultAdminRoleId)
    principalType: 'Group'
  }
}

var keyVaultSecretsOfficerRoleId = 'b86a8fe4-44ce-4948-aee5-eccb2c155cd7'
resource servicePrincipalIsKeyVaultSecretsOfficer 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(vault.id, keyvaultServicePrincipalObjectId, keyVaultSecretsOfficerRoleId)
  scope: vault
  properties: {
    principalId: keyvaultServicePrincipalObjectId
    roleDefinitionId: tenantResourceId('Microsoft.Authorization/roleDefinitions', keyVaultSecretsOfficerRoleId)
    principalType: 'ServicePrincipal'
  }
}

var keyVaultCryptoOfficerRoleId = '14b46e9e-c2b7-41b4-b07b-48a6ebf60603'
resource servicePrincipalIsKeyVaultCryptoOfficer 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(vault.id, keyvaultServicePrincipalObjectId, keyVaultCryptoOfficerRoleId)
  scope: vault
  properties: {
    principalId: keyvaultServicePrincipalObjectId
    roleDefinitionId: tenantResourceId('Microsoft.Authorization/roleDefinitions', keyVaultCryptoOfficerRoleId)
    principalType: 'ServicePrincipal'
  }
}
