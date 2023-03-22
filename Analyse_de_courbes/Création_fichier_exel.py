import openpyxl

# Créer un nouveau classeur Excel
workbook = openpyxl.Workbook()

# Sélectionner la feuille de calcul active
worksheet = workbook.active

# Donner un nom à la colonne
worksheet['A1'] = 'Valeurs'

# Les valeurs de la liste
valeurs = [1, 2, 3, 4]

# Ajouter chaque élément de la liste dans une cellule de la colonne A
for i, valeur in enumerate(valeurs):
    cellule = 'A' + str(i+2)
    worksheet[cellule] = valeur

# Enregistrer le classeur Excel
workbook.save('mon_classeur.xlsx')



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


stocke_liste_exel([1, 2, 3, 4], 'A', 'Tension')
