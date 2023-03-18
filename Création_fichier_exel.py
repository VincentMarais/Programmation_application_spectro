import openpyxl

# Créer un nouveau classeur Excel
workbook = openpyxl.Workbook()

# Sélectionner la feuille de calcul active
worksheet = workbook.active

# Donner un nom à la colonne
worksheet['A1'] = 'Valeurs'

# Les valeurs de la liste
valeurs = [1, 2, 3, 4, 5, 8]

# Ajouter chaque élément de la liste dans une cellule de la colonne A
for i, valeur in enumerate(valeurs):
    cellule = 'A' + str(i+2)
    worksheet[cellule] = valeur

# Enregistrer le classeur Excel
workbook.save('mon_classeur.xlsx')