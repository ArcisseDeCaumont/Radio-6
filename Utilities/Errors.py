#  »»» Errors.py
#  »»» © Oscar Mazeure pour Radio 6 lycée Arcisse de Caumont

import tkinter as tk
import customtkinter as ctk
import time
import sentry_sdk

# Création d'un objet erreur (Exception) personnalisé
class Error(Exception) :
    def __init__(self, error):
        super().__init__(error)

def raise_error(app, error, tool, mail = False, specific_error = None, additional_infos = "Aucune info supplémentaire fournie") :
    # Arrêt de la fenêtre ayant envoyé l'erreur
    app.destroy()
    # Création de la fenêtre CustomTkinter d'affichage de l'erreur
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("ModifierSiteWeb")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    # Création et affichage des éléments de la fenêtre
    label_arror = ctk.CTkLabel(master=app, text=error, width=165, text_color="red")
    label_arror.pack(pady=5)
    label_advice1 = ctk.CTkLabel(master=app, text="Lisez la documentation et réessayez", width=165, text_color="red")
    label_advice1.pack(pady=0)
    label_advice2 = ctk.CTkLabel(master=app, text="Pour toute  aide supplémentaire, contactez oscar.mazeure@orange.fr", width=165, text_color="red")
    label_advice2.pack(pady=0)

    if mail != False and specific_error != None : # Si l'envoi de l'erreur et activé, appel de la fonction pour remonter cette erreur
        send_email_error(error, specific_error, tool, additional_infos)
    
    return app

def send_email_error(general_error, specific_error, tool, additional_infos) :
    # Initialisation du lien avec Sentry (logiciel de gestion des erreurs)
    sentry_sdk.init(
        dsn="https://51140a20e915ca042dbe4bf523d7103f@o4509700906352640.ingest.de.sentry.io/4509700953079888",
        send_default_pii=True,
    )
    # Ajout de détails à l'erreur renvoyée à Sentry
    sentry_sdk.set_context("Infos", {"Erreur générale" : general_error, "Détails de l'erreur" : specific_error, "Outil utilisé" : tool, "Infos supplémentaires" : additional_infos})
    # Envoi de l'erreur à Sentry
    try :
        raise Error(general_error)
    except Error as e :
        sentry_sdk.capture_exception(e)