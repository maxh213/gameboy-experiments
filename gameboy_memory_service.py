class Gameboy_Memory_Service:

    def __init__(self, pyboy):
        self.pyboy = pyboy
        self.species_map = {
            158: "Totadile"
        }

    # Helper function to check if the Pokemon is shiny based on its DVs
    def check_shiny(self, dvs):
        attack_dv = (dvs & 0xF000) >> 12
        defense_dv = (dvs & 0x0F00) >> 8
        speed_dv = (dvs & 0x00F0) >> 4
        special_dv = dvs & 0x000F
        return (
            (attack_dv in {2, 3, 6, 7, 10, 11, 14, 15}) and
            defense_dv == 10 and
            speed_dv == 10 and
            special_dv == 10
        )

    def is_first_party_pokemon_shiny(self):
        # Memory address for the DVs of the first Pokemon in the party
        DVs_ADDRESS = 0xDCF4

        # Load the DVs from memory
        dvs = self.pyboy.get_memory_value(DVs_ADDRESS)

        # Check if the Pokemon is shiny
        is_shiny = self.check_shiny(dvs)

        return is_shiny

    def get_first_party_pokemon_info(self):

        # Memory addresses
        SPECIES_ID_ADDRESS = 0xDCDF
        LEVEL_ADDRESS = 0xDCFE
        DVs_ADDRESS = 0xDCF4

        # Load values from memory
        species_id = self.pyboy.get_memory_value(SPECIES_ID_ADDRESS)
        level = self.pyboy.get_memory_value(LEVEL_ADDRESS)
        dvs = self.pyboy.get_memory_value(DVs_ADDRESS)

        # Deduce gender from the Attack DV
        attack_dv = (dvs & 0xF000) >> 12
        gender = 'Male' if attack_dv % 2 == 0 else 'Female'

        # Get Pokémon species name
        if (species_id == 158):
            pokemon_species_name = 'Totodile'
        else: 
            pokemon_species_name = species_id

        return pokemon_species_name, level, gender