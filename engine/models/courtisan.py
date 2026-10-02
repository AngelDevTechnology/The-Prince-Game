class Courtisan:
    def __init__(self, idPNJ, nom, role, ambition, loyaute, est_joueur):
        self.idPNJ = idPNJ
        self.nom = nom
        self.role = role
        self.ambition = ambition
        self.loyaute = loyaute
        self.est_joueur = est_joueur

    def __repr__(self):
        return f"id = {self.idPNJ}, nom = {self.nom}, role = {self.role}, ambition = {self.ambition}, loyaute = {self.loyaute}, est_joueur = {self.est_joueur}"