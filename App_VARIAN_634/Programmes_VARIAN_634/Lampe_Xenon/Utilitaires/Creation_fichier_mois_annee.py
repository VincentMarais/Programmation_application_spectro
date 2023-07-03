import os
import datetime
REPERTOIRE_PAR_DEFAUT="C:\\Users\\admin\Documents\\Projet_GP\\Programmation_Spectro\\Programmation_application_spectro\\App_VARIAN_634\\Programmes_VARIAN_634\\Lampe_Xenon\\Manip"

def detection_exitance_repertoire(chemin): # Path chemin d'accès
    chemin=os.path.join(chemin)
    if not os.path.exists(chemin):
        return False

def Repertoire_annee_mois_jour():
    current_date = datetime.datetime.now()
    current_year, current_month, current_day = current_date.strftime("%Y") , current_date.strftime("%m_%Y"), current_date.strftime("%d_%m_%Y") 
        
    chemin=os.path.join(REPERTOIRE_PAR_DEFAUT,"Manip_"+current_year, "Manip_"+ current_month , "Manip_"+current_day)
    if  detection_exitance_repertoire(chemin)==False:
        os.makedirs(chemin)
        print("Le répertoire à été créé : ", chemin)
    else:
            print("Le répertoire existe déjà :", chemin)


def Repertoire_Date_Fente(chemin, Taille_de_fente):
    Taille_de_fente=input("Taille de fente : Fente_2nm, Fente_1nm , Fente_0_5nm, Fente_0_2nm : ")
    date_aujourdhui = datetime.date.today()
    Date = date_aujourdhui.strftime("%d_%m_%Y")
    chemin = os.path.join("C:\\Users\\vimarais\\Desktop\\Programmation_application_spectro-master\\Manip", Date, Taille_de_fente)

    # Vérifier si le répertoire existe déjà
    if not os.path.exists(chemin):
        # Créer le répertoire en utilisant le chemin d'accès
        os.makedirs(chemin)
        print("Répertoire créé avec succès :", chemin)
    else:
        print("Le répertoire existe déjà :", chemin)

    return Date, Taille_de_fente


