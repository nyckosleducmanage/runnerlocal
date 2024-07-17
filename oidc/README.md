# Fonctionnement OIDC

## Benefits of using OIDC

Bonnes pratiques de sécurité suivantes :

### Pas de secrets dans le cloud :
Vous n'aurez pas besoin de dupliquer vos informations d'identification cloud en tant que secrets GitHub à long terme. Au lieu de cela, vous pouvez configurer la confiance OIDC sur votre fournisseur de cloud, puis mettre à jour vos flux de travail pour demander un jeton d'accès de courte durée à votre fournisseur de cloud via OIDC.

### Gestion de l'authentification et de l'autorisation
Vous avez un contrôle plus granulaire sur la manière dont les flux de travail peuvent utiliser les informations d'identification, en utilisant les outils d'authentification (authN) et d'autorisation (authZ) de votre fournisseur de cloud pour contrôler l'accès aux ressources cloud.

### Rotation des informations d'identification
Avec OIDC, votre fournisseur de cloud émet un jeton d'accès de courte durée qui n'est valable que pour une seule tâche, puis expire automatiquement.

## Diagram

![image](https://github.com/nyckosleducmanage/runnerlocal/blob/main/oidc/oidc.png)
