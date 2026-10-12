class Character:
    def __init__(self, character_id, name, role, ambition, loyalty, is_player=False):
        self.character_id = character_id
        self.name = name
        self.role = role

        self.ambition = ambition
        self.loyalty = loyalty

        self.is_player = is_player

        self.relationships = {}
        self.memories = []


        