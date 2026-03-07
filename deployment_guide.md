# Guide de Déploiement (Docker & GitHub) : jemassurance.online

## 1. Préparation GitHub
1. Créez un dépôt sur GitHub et poussez votre code.
2. Ajoutez les **Secrets** dans GitHub (Settings > Secrets > Actions) :
   - `HOST_IP` : L'IP de votre VPS Hostinger.
   - `HOST_USER` : `root` (en général).
   - `SSH_PRIVATE_KEY` : Votre clé privée SSH (autorisée sur le VPS).

## 2. Configuration du VPS (Une seule fois)
Connectez-vous à votre VPS et installez Docker :
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

## 3. Déploiement Continu
Désormais, à chaque **git push**, GitHub Actions va :
1. Se connecter à votre VPS.
2. Récupérer le dernier code.
3. Reconstruire et relancer les containers via `docker-compose.yml`.

Le frontend sera disponible sur le port 80 (HTTP) et l'API sur le port 8001.
