import tkinter as tk
import customtkinter as ctk
import os
import subprocess
import AjouterEmission
import SupprimerEmission
import Errors

def commit_changes(app):
    repo_path = f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/"
    os.chdir(repo_path)
    
    try:        
        subprocess.run(['git', 'add', '-A'], check=True, capture_output=True, text=True)
        print("All changes added to staging.")

        commit_result = subprocess.run(['git', 'commit', '-m', "Upload automatique"], check=True, capture_output=True, text=True)
        print("Changes committed.")
        print("Commit Output:", commit_result.stdout)

        push_result = subprocess.run(['git', 'push'], check=True, capture_output=True, text=True, timeout=700)
        print("All changes pushed successfully.")
        print("Push Output:", push_result.stdout)

    except subprocess.CalledProcessError as e:
        print(e)
        print(e.stderr)
        Errors.raise_error(app, "Erreur lors de la synchronisation GitHub.", "ModifierSiteWeb.py", mail=True, specific_error=e)
        return "error"
    
    return

app = ctk.CTk()
app.geometry("400x400")
app.title("ModifierSiteWeb")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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
    AjouterEmission.main()

bouton_ajout = ctk.CTkButton(master=app, text="Ajouter une émission", command=ajouter_émission)
bouton_ajout.pack(pady=5)

bouton_suppression = ctk.CTkButton(master=app, text="Supprimer une émission", command=ajouter_émission)
bouton_suppression.pack(pady=5)

bouton_agenda = ctk.CTkButton(master=app, text="Renseigner la prochaine émission", command=ajouter_émission)
bouton_agenda.pack(pady=5)

app.mainloop()