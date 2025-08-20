import subprocess
import os

def main():
    try:
        # Assurez-vous d'être dans un dépôt Git
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Demande à l'utilisateur de saisir le contenu de l'erreur
        issue_title = "Test titre erreur 1"
        issue_body = "Test corps de l'erreur 1 !!"

        # Crée le répertoire .github/workflows si nécessaire
        os.makedirs('.github', exist_ok=True)
        
        # Crée le fichier déclencheur avec le contenu personnalisé
        with open('.github/create_issue_trigger', 'w') as f:
            f.write(f"title: {issue_title}\n\n{issue_body}")

        # Ajoute et commite le fichier
        subprocess.run(['git', 'add', '.github/create_issue_trigger'], check=True)
        subprocess.run(['git', 'commit', '-m', f"Signalement d'une erreur: '{issue_title}'"], check=True)
        
        # Pousse le commit vers le dépôt distant
        subprocess.run(['git', 'push'], check=True)

        print("L'erreur a été signalée avec succès. Une nouvelle erreur a été créée sur le dépôt GitHub.")

    except subprocess.CalledProcessError:
        print("Erreur: Le script doit être exécuté depuis la racine d'un dépôt Git cloné.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")

if __name__ == "__main__":
    main()