import os
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

def sauvegarder_bdd_avec_mysqldump():
    # 1. Récupération des configurations
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_MDP')
    database = os.getenv('DB_NAME')

    if not all([host, user, password, database]):
        print("[ERREUR] : Variables d'environnement manquantes dans le fichier .env")
        return False

    # 2. Préparation du dossier et du nom de fichier
    dossier = "backups_sql"
    os.makedirs(dossier, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"backup_{database}_{timestamp}.sql"
    chemin_complet = os.path.join(dossier, nom_fichier)

    # 3. Construction de la commande mysqldump
    # Note : On utilise --result-file pour éviter les problèmes d'encodage de redirection de flux
    commande = [
        'mysqldump',
        f'--host={host}',
        f'--user={user}',
        f'--password={password}',
        '--single-transaction',  # Important : évite de bloquer la BDD pendant l'export
        '--quick',               # Optimise la mémoire pour les grosses tables
        f'--result-file={chemin_complet}',
        database
    ]

    try:
        print(f"--- Début de la sauvegarde (mysqldump) de '{database}' ---")
        
        # Exécution de la commande
        # capture_output=True permet de récupérer les erreurs si mysqldump échoue
        resultat = subprocess.run(commande, capture_output=True, text=True, check=True)
        
        print(f"Sauvegarde réussie : {chemin_complet}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] mysqldump a échoué :")
        print(e.stderr) # Affiche l'erreur réelle de MySQL (ex: mauvais mot de passe)
        return False
    except FileNotFoundError:
        print("[ERREUR] : L'utilitaire 'mysqldump' n'est pas installé ou n'est pas dans le PATH.")
        return False
    except Exception as e:
        print(f"[ERREUR] Inattendue : {e}")
        return False

if __name__ == "__main__":
    sauvegarder_bdd_avec_mysqldump()
