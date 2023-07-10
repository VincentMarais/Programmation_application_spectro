import os
chemin ="Detection"
def detection_exitance_repertoire(chemin): # Path chemin d'accès
    chemin=os.path.join(chemin)
    if not os.path.exists(chemin):
        return False
    else:
        return True
print(detection_exitance_repertoire(chemin))