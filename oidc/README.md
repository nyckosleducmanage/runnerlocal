# Fonctionnement OIDC

## Benefits of using OIDC

By updating your workflows to use OIDC tokens, you can adopt the following good security practices:

No cloud secrets: You won't need to duplicate your cloud credentials as long-lived GitHub secrets. Instead, you can configure the OIDC trust on your cloud provider, and then update your workflows to request a short-lived access token from the cloud provider through OIDC.
Authentication and authorization management: You have more granular control over how workflows can use credentials, using your cloud provider's authentication (authN) and authorization (authZ) tools to control access to cloud resources.
Rotating credentials: With OIDC, your cloud provider issues a short-lived access token that is only valid for a single job, and then automatically expires.

![image](https://github.com/nyckosleducmanage/runnerlocal/blob/main/oidc/oidc.png)
