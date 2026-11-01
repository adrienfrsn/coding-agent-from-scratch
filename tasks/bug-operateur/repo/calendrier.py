def est_bissextile(annee):
    return annee % 4 == 0 and annee % 100 == 0 or annee % 400 == 0
