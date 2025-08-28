#  »»» WebsiteManager.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import tkinter as tk
import customtkinter as ctk
import os
import sys
import time
import subprocess
import AjouterEmission
import SupprimerEmission
import ModifierAgenda
import GérerPodcasts
import Errors

# Fonction pour l'affichage de la fenêtre de fin de porgramme
def finish_window(app) :
    # ╚> Arrêt de la fenêtre précédente
    app.destroy()
    # ╚> Création de la nouvelle fenêtre
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("WebsiteManager")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # ╚> Création et affichage des éléments de la fenêtre
    label_finished1 = ctk.CTkLabel(master=app, text="C'est bon !", width=165,)
    label_finished1.pack(pady=5)
    label_finished2 = ctk.CTkLabel(master=app, text="Le programme a fini de s'exécuter, vous pouvez fermer cette fenêtre", width=200)
    label_finished2.pack(pady=0)

    # ╚> Délai de 60 secondes
    time.sleep(60)
    # ╚> Arrêt du programme
    sys.exit()


# Fonction de synchronisation avec GitHub
def commit_changes(app) :
    # ╚> Définition du chemin du dossier à synchroniser
    repo_path = f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/"
    # ╚> Changement du répoertoire de travail vers ce dossier
    os.chdir(repo_path)
    
    try:
    # ╚> Rassemblement des changements
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True, text=True)

    # ╚> Ajout des fichiers pour l'envoi
        commit_result = subprocess.run(['git', 'commit', '-m', "Upload automatique"], check=True, capture_output=True, text=True)
        print("Changes committed.")
        print("Commit Output:", commit_result.stdout)

    # ╚> Envoi des changements à GitHub
        push_result = subprocess.run(['git', 'push'], check=True, capture_output=True, text=True, timeout=700)
        print("All changes pushed successfully.")
        print("Push Output:", push_result.stdout)

    except subprocess.CalledProcessError as e:
        Errors.raise_error(app, "Erreur lors de la synchronisation GitHub.", "WebsiteManager.py", mail=True, specific_error=e, additional_infos={"Stderr" : e.stderr})
        return "error"
    except Exception as e :
        Errors.raise_error(app, "Erreur lors de la synchronisation GitHub", "WebsiteManager.py", mail=True, specific_error=e)
        return "error"
    
    finish_window(app)

# Création de la fenêtre CustomTkinter
app = ctk.CTk()
app.geometry("400x400")
app.title("WebsiteManager")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Accès aux fonctions des autres fichiers
def ajouter_émission():
    global app
    app.destroy()
    AjouterEmission.main()

def supprimer_émission():
    global app
    app.destroy()
    SupprimerEmission.main()

def modifier_agenda():
    global app
    app.destroy()
    ModifierAgenda.main()

def gérer_podcasts():
    global app
    app.destroy()
    GérerPodcasts.main()

# Création et ajout des éléments à la fenêtre
bouton_ajout = ctk.CTkButton(master=app, text="Ajouter une émission", command=ajouter_émission)
bouton_ajout.pack(pady=5)

bouton_suppression = ctk.CTkButton(master=app, text="Supprimer une émission", command=supprimer_émission)
bouton_suppression.pack(pady=5)

bouton_agenda = ctk.CTkButton(master=app, text="Renseigner la prochaine émission", command=modifier_agenda)
bouton_agenda.pack(pady=5)

bouton_agenda = ctk.CTkButton(master=app, text="Gérer les catégories de podcasts", command=ajouter_émission)
bouton_agenda.pack(pady=5)

bouton_commit = ctk.CTkButton(master=app, text="Synchroniser avec GitHub", command=lambda : commit_changes(app))
bouton_commit.pack(pady=5)

if __name__ == "__main__" :
    app.mainloop()