from random import randint

tirage = randint(1, 100)


dico_role = {"peasant": 1, "courtier": 2, "advisor": 3, "king": 4}

class Complot:
    def __init__(self, initiator, target):
        self.initiator = initiator
        self.target = target
        self.success = None
        self.chance = self._success_chance()

    def __repr__(self):
        """return an str object with the name of the initiator and the name of the target"""
        return f"initiator : {self.initiator.name}, target : {self.target.name}"

    def _success_chance(self):
        """calculate the success chances for a plot to win"""
        grade_initiator = dico_role[self.initiator.role]
        grade_target = dico_role[self.target.role]
        gap = grade_target - grade_initiator
        a, b = self._success_random()
        return max(0, min(100, 60 - 15 * gap)) + a - b

    def _success_random(self):
        return randint(0, 20), randint(0, 10)

    def _success(self):
        if self.chance >= 55 :
            self.success = True
        else :
            self.success = False

    


    



"""
if __name__ == "__main__":
    a = Courtier(1, "Ardouin", "courtier", 80, 60)
    b = Courtier(2, "Lapeyre", "advisor", 80, 60)
    c = Complot(a, b)
    print(c)
"""
