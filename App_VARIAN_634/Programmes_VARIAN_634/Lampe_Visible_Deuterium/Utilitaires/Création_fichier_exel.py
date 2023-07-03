import openpyxl
import csv

def sauvegarder_donnees(nom_fichier, longueurs_d_onde, tensions, titre_1, titre_2):
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(longueurs_d_onde)):
            writer.writerow([longueurs_d_onde[i], tensions[i]])

my_list = [3, 8, 2, 7, 1, 9]
max_index = my_list.index(max(my_list))
print(max_index)  # Output: 5

p=[1,2,3]
p.reverse()
sauvegarder_donnees('Analyse_de_courbes\mon_classeur.xlsx',  p, [2,3,5], 'longueurs_d_onde', 'Tension')
def stocke_liste_exel(L,lettre, titre): # L: Liste a stocké dans le exel / lettre: lettre de la colonne du exel / titre: titre de la colonne
    workbook = openpyxl.Workbook()

    # Sélectionner la feuille de calcul active
    worksheet = workbook.active

    # Donner un nom à la colonne
    worksheet[lettre + '1'] = titre

    # Les valeurs de la liste

    # Ajouter chaque élément de la liste dans une cellule de la colonne A
    for i, valeur in enumerate(L):
        cellule = lettre + str(i+2)
        worksheet[cellule] = valeur

    # Enregistrer le classeur Excel
    workbook.save('expérience_1.xlsx')


