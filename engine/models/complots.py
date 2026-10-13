import random
from engine.models.courtier import Courtier

dico_role = {'peasant' : 1, 'courtier' : 2, 'advisor' : 3, 'king' : 4}

class Complot:
    def __init__(self, initiator, target):
        self.initiator = initiator
        self.target = target
        self.success = None

    def __repr__(self):
        return f"initiator : {self.initiator.name}, target : {self.target.name}"

    def success_chance(self):
        grade_initiator = dico_role[self.initiator.role]
        grade_target = dico_role[self.target.role]
        gap = grade_target - grade_initiator
        chance = 50 - 15 * gap











"""
if __name__ == "__main__":
    a = Courtier(1, "Ardouin", "courtier", 80, 60)
    b = Courtier(2, "Lapeyre", "advisor", 80, 60)
    c = Complot(a, b)
    print(c)
"""