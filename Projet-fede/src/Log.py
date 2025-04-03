import  pandas as pd
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import smtplib, ssl


class Log():
    def __init__(self, path: str):
        self.path = path

        self.checkPresences()
        self.sendEmail()
    
    def checkPresences(self):
        """Open csv with pandas and read colonnes Nom et extraction des uniques""" 
        df = pd.read_csv(self.path, sep=',')
        print(df.columns)
    
        uniques = df['Nom'].unique()
        self.uniques = uniques
        
        self.uniques = ', '.join(uniques)
        print(self.uniques)
    

    def sendEmail(self):
            smtp_server = 'smtp.gmail.com'
            port = 465
            destinateur = 'ipsa.presence@gmail.com' #adresse d'envoie crée
            password = 'uxsj qcxu xvfk scgc' #mot de passe adresse
            destinataire = "valentin.perrot.alt@gmail.com" #adresse destinateur
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Envoie Présence éléve'# objet mail
            message['From'] = destinateur
            message['To'] = destinataire
            message.attach(MIMEText(f"Bonjour,\n\nVoici votre compte-rendu des présences.\n\nSont présents: {self.uniques}", 'plain'))# message mail


            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(destinateur, password)
                server.sendmail(destinateur, destinataire, message.as_string())

            print("Email envoyé avec succès !")
            print("Fin de l'appelle... \n  Arret du programme...")
            exit(0)

