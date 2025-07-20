import requests
import tkinter as tk
import customtkinter as ctk
import time
import sentry_sdk

def raise_error(app, error, tool, mail = False, specific_error = None) :
    app.destroy()
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("ModifierSiteWeb")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    label_arror = ctk.CTkLabel(master=app, text=error, width=165, text_color="red")
    label_arror.pack(pady=5)
    label_advice1 = ctk.CTkLabel(master=app, text="Lisez la documentation et réessayez", width=165, text_color="red")
    label_advice1.pack(pady=0)
    label_advice2 = ctk.CTkLabel(master=app, text="Pour toute  aide supplémentaire, contactez oscar.mazeure@orange.fr", width=165, text_color="red")
    label_advice2.pack(pady=0)

    if mail != False and specific_error != None :
        send_email_error(error, specific_error, tool)
    
    return app

def send_email_error(general_error, specific_error, tool) :
    sentry_sdk.init(
        dsn="https://51140a20e915ca042dbe4bf523d7103f@o4509700906352640.ingest.de.sentry.io/4509700953079888",
        send_default_pii=True,
    )
    sentry_sdk.capture_exception(specific_error)

app = ctk.CTk()
app.geometry("775x400")
app.title("ModifierSiteWeb")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

bouton_erreur = ctk.CTkButton(master=app, text="Test de la fonction erreur", command=lambda : raise_error(app, "Erreur générale test !", "Outil test", mail=True, specific_error="Erreur détaillée\nDétails supplémentaires"))
bouton_erreur.pack(pady=5)

app.mainloop()