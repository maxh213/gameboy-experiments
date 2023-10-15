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
        dvs = self.get_value_dvs(DVs_ADDRESS, 2)

        # Check if the Pokemon is shiny
        is_shiny = self.check_shiny(dvs)

        return is_shiny

    def get_first_party_pokemon_info(self):
        # Memory addresses
        addresses = {
            'species_id': 0xDCDF,
            'held_item': 0xDCE0,
            'move_1': 0xDCE1,
            'move_2': 0xDCE2,
            'move_3': 0xDCE3,
            'move_4': 0xDCE4,
            'ot_id': 0xDCE5,
            'experience': 0xDCE7,
            'hp_exp': 0xDCEA,
            'atk_exp': 0xDCEC,
            'def_exp': 0xDCEE,
            'spd_exp': 0xDCF0,
            'spe_exp': 0xDCF2,
            'dvs': 0xDCF4,
            'move_1_pp': 0xDCF6,
            'move_2_pp': 0xDCF7,
            'move_3_pp': 0xDCF8,
            'move_4_pp': 0xDCF9,
            'happiness': 0xDCFA,
            'pokerus_status': 0xDCFB,
            'caught_data': 0xDCFC,
            'level': 0xDCFE,
            'status': 0xDCFF,
            'hp': 0xDD01,
            'max_hp_stat': 0xDD03,
            'attack_stat': 0xDD05,
            'defense_stat': 0xDD07,
            'speed_stat': 0xDD09,
            'special_attack_stat': 0xDD0B,
            'special_defense_stat': 0xDD0D
        }

        # Load values from memory
        pokemon_info = {key: self.get_value(addr, 2 if '_stat' in key else 1) for key, addr in addresses.items()}

        # Get Pokémon species name
        if (pokemon_info['species_id'] == 158):
            pokemon_species_name = 'Totodile'
        else:
            pokemon_species_name = pokemon_info['species_id']  # Perhaps lookup in a species dictionary for better results

        pokemon_info['species_name'] = pokemon_species_name

        # Extract DVs by using bitwise operations
        dv_value = self.get_value_dvs(addresses['dvs'], 2)
        attack_dv = (dv_value & 0xF000) >> 12
        defense_dv = (dv_value & 0x0F00) >> 8
        speed_dv = (dv_value & 0x00F0) >> 4
        special_dv = dv_value & 0x000F

        # Deduce gender from the Attack DV
        gender = 'Male' if attack_dv % 2 == 0 else 'Female'
        pokemon_info['gender'] = gender

        # Update pokemon_info dictionary
        pokemon_info.update({
            'attack_dv': attack_dv,
            'defense_dv': defense_dv,
            'speed_dv': speed_dv,
            'special_dv': special_dv,
        })

        pokemon_info['moves'] = str(pokemon_info['move_1']) + ', ' + str(pokemon_info['move_2']) + ', ' + str(pokemon_info['move_3']) + ', ' + str(pokemon_info['move_4'])
        return pokemon_info

    def print_first_party_pokemon_info(self, current_attempts):
        info = self.get_first_party_pokemon_info()
        is_shiny = self.is_first_party_pokemon_shiny()
        shiny_attack_pass = False
        shiny_other_stat_pass = False
        attack_dv = info['attack_dv']
        if (attack_dv == 2 or attack_dv == 3 or attack_dv == 6 or attack_dv == 7 or attack_dv == 10 or attack_dv == 11 or attack_dv == 14 or attack_dv == 15):
            shiny_attack_pass = True
        if (info['defense_dv'] == 10 and info['speed_dv'] == 10 and info['special_dv'] == 10):
            shiny_other_stat_pass = True

        print(f"""
Shiny: {is_shiny},
Number of resets: {str(current_attempts)},
Pokemon Species: {info['species_name']}, 
Level: {info['level']}, 
Gender: {info['gender']}, 
Attack IV: {info['attack_dv']},
Defense IV: {info['defense_dv']},
Speed IV: {info['speed_dv']},
Special IV: {info['special_dv']},
Attack IV shiny pass: {shiny_attack_pass},
Other stat IV shiny pass: {shiny_other_stat_pass},
Pokérus Status: {info['pokerus_status']},
Max HP: {info['max_hp_stat']},
Attack: {info['attack_stat']},
Defense: {info['defense_stat']},
Speed: {info['speed_stat']},
Special Attack: {info['special_attack_stat']},
Special Defense: {info['special_defense_stat']}
""")

    def get_value(self, address, length=1):
        if length == 1:
            return self.pyboy.get_memory_value(address)
        else:
            low_byte = self.pyboy.get_memory_value(address)
            high_byte = self.pyboy.get_memory_value(address + 1)
            return high_byte

    def get_value_dvs(self, address, length=1):
        if length == 1:
            return self.pyboy.get_memory_value(address)
        else:
            low_byte = self.pyboy.get_memory_value(address)
            high_byte = self.pyboy.get_memory_value(address + 1)
            return (high_byte << 8) | low_byte 
