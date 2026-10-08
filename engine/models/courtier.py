from engine.models.character import Character


class Courtier(Character): #create class coutisan
    
    def __init__(self, character_id, name, age, ambition, loyalty, is_player=False, influence=0):
        super().__init__(character_id, name, age, ambition, loyalty, is_player)
        self.influence = influence

    def __repr__(self):
        return f"{self.character_id}, {self.name}, age : {self.age}, ambition : {self.ambition}, loyalty : {self.loyalty}, is it a player : {self.is_player}, influence : {self.influence}"


"""
from models.courtier import Courtier

ardouin = Courtier(character_id=1, name="Ardouin", age=35, ambition=80, loyalty=60, influence=75)
"""