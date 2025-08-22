#  »»» Errors.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import tkinter as tk
import customtkinter as ctk
import time
import os
import subprocess
import webbrowser
import pyperclip

# Création de la fenêtre CustomTkinter d'affichage de l'erreur
app = ctk.CTk()
app.geometry("600x400")
app.title("Errors")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def raise_error(previous_app, error, tool, mail = False, specific_error = None, additional_infos = "Aucune info supplémentaire fournie") :
    global app
    # Arrêt de la fenêtre ayant envoyé l'erreur
    previous_app.destroy()
    # Création et affichage des éléments de la fenêtre
    label_error = ctk.CTkLabel(master=app, text=error, width=165, text_color="red")
    label_error.pack(pady=5)
    label_advice1 = ctk.CTkLabel(master=app, text="Vous pouvez lire la documentation et réessayer", width=165, text_color="red")
    label_advice1.pack(pady=0)
    label_advice2 = ctk.CTkLabel(master=app, text="Pour toute aide supplémentaire, contactez oscar.mazeure@orange.fr", width=165, text_color="red")
    label_advice2.pack(pady=0)
    if mail == True :
        label_advice3 = ctk.CTkLabel(master=app, text="Une erreur est en train d'être créée sur GitHub...", width=165, text_color="red")
        label_advice3.pack(pady=0)

    if mail != False and specific_error != None : # Si l'envoi de l'erreur et activé, appel de la fonction pour remonter cette erreur
        send_email_error(error, specific_error, tool, additional_infos)
    
    app.mainloop()

    return app

def send_email_error(general_error, specific_error, tool, additional_infos) :
    issue_title = "Nouvelle erreur"
    issue_body = f"""
**Nouvelle erreur :** {general_error}
                    
**Erreur detaillee :** {specific_error}
**Outil utilise :** {tool}
                 """
    if additional_infos :
        issue_body += ("\n **Informations supplementaires :**")
    for clé, valeur in additional_infos.items() :
        issue_body += (f"""
    {clé} : {valeur}""")

    try :
        trigger_file_path = f"C:/Users/{os.getlogin()}/Documents/GitHub/Radio-6/.github/error_trigger"
        with open(trigger_file_path, 'w') as f:
                f.write(f"title: {issue_title}\n\n{issue_body}")
        
        subprocess.run(['git', 'add', trigger_file_path], check=True, capture_output=True, text=True)
        subprocess.run(['git', 'commit', '-m', f"Signalement d'une erreur: '{issue_title}'"], check=True, capture_output=True, text=True)
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        issue_body += f"""
**Autre erreur dans Errors.py :** {e}
{e.stderr}
"""
        crash_handling(issue_body)
        
    except Exception as e:
        issue_body += f"""
**Autre erreur dans Errors.py :** {e}
"""
        crash_handling(issue_body)

def web_browsing_github():
    url = "https://github.com/ArcisseDeCaumont/Radio-6/issues/new"
    webbrowser.open(url)

def copy_error(issue):
    pyperclip.copy(issue)

def crash_handling(issue):
    global app
    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkBaseClass):
            widget.destroy()

    label_advice1 = ctk.CTkLabel(master=app, text="Le rapport d'erreur a échoué. Merci de signaler l'erreur sur GitHub ou à oscar.mazeure@orange.fr", width=250, text_color="red")
    label_advice1.pack(pady=10)
    bouton_copy = ctk.CTkButton(master=app, text="Copier le message d'erreur", command=lambda : copy_error(issue))
    bouton_copy.pack(pady=5)
    bouton_github = ctk.CTkButton(master=app, text="Aller sur GitHub", command=web_browsing_github)
    bouton_github.pack(pady=5)