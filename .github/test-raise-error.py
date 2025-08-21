import subprocess
import os

def main():
    try:
        # Assurez-vous d'être dans un dépôt Git
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Le script est conçu pour être exécuté depuis la racine du dépôt Git.
        # Les chemins ci-dessous sont relatifs à cette racine.
        
        issue_title = "Test titre erreur 1"
        issue_body = "Test corps de l'erreur 1 !!"

        # Crée le répertoire .github/workflows si nécessaire
        os.makedirs('.github', exist_ok=True)
        
        # Crée le fichier déclencheur avec le contenu personnalisé
        trigger_file_path = os.path.join('.github', 'error_trigger')
        with open(trigger_file_path, 'w') as f:
            f.write(f"title: {issue_title}\n\n{issue_body}")

        # Ajoute le fichier déclencheur au staging area
        subprocess.run(['git', 'add', trigger_file_path], check=True, capture_output=True, text=True)
        
        # Commite le fichier
        subprocess.run(['git', 'commit', '-m', f"Signalement d'une erreur: '{issue_title}'"], check=True, capture_output=True, text=True)
        
        # Pousse le commit vers le dépôt distant
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)

        print("L'erreur a été signalée avec succès. Une nouvelle erreur a été créée sur le dépôt GitHub.")
    
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        print(e)
        
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")

if __name__ == "__main__":
    main()