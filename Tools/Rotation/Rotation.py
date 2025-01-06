import os
import random
import pandas as pd

# Weight for mode
# [RAAS/AAS, Invasion, Skirmish, TC, Insurgency/Destruction]
WEIGHT_MODE = [5, 36, 4, 4, 51]

# Weight for alliance
# B-BlueForce I-Independent P-PAC R-RedForce
# [B-I, B-P, B-R, I-P, I-R, P-R, I-I]
WEIGHT_ALLIANCE = [25, 15, 10, 15, 10, 6, 20]

# Weight for daylight(%)
# [Daytime, not Daytime]
WEIGHT_LIGHT = [7, 3]

# Weight for large size map
# [Large, not Large]
WEIGHT_SIZE = [3,2]

# Weight for equal battle group type
# [Balance, not Balance]
WEIGHT_EQUAL = [1,1]

TOTAL_NUMBER = 5000

FILEPATH = "LayerRotation"

class Layer:
    def __init__(self, level="", ID=0, layer_name="", game_mode="", lighting="", tickets="", commander="", layer_size="", notes="", totals=""):
        self.level = level
        self.ID = ID
        self.layer_name = layer_name
        self.game_mode = game_mode
        self.lighting = lighting
        self.tickets = tickets
        self.commander = commander
        self.layer_size = layer_size
        self.notes = notes
        self.totals = totals

class Level:
    def __init__(self, name=""):
        self.name = name
        self.destruction = []
        self.r_aas = []
        self.insurgency = []
        self.invasion = []
        self.seed = []
        self.skirmish = []
        self.ta = []
        self.tc = []
        self.training = []
        self.valid_count = 0

class BGLayer:
    def __init__(self, layer_name=""):
        self.layer_name = layer_name
        self.team1 = []
        self.team2 = []
        self.blue_force = set()
        self.independent = set()
        self.red_force = set()
        self.PAC = set()

def get_milestone(weights):
    milestone = []
    temp = 0
    for index in range(len(weights)):
        temp += weights[index]
        milestone.append(temp)

    return milestone

def read_all_layers():
    # get local director
    current_directory = os.getcwd()

    # get file path
    files = os.listdir(current_directory)

    # get Layers.csv file
    for file in files:
        if file.endswith('Layers.csv'):
            layers = []

            file_path = os.path.join(current_directory, file)
            df = pd.read_csv(file_path)

            # ,Level,ID,Layer Name,Game Mode,Lighting,Tickets,Commander,Layer Size*,,Notes,,Totals,
            level = ""
            ID = 0
            layer_name = ""
            game_mode = ""
            lighting = ""
            tickets = ""
            commander = ""
            layer_size = ""
            notes = ""
            totals = ""

            for index, row in df.iloc[1:-2].iterrows():
                # row.iloc[1] -> Level
                if pd.notnull(row.iloc[1]):
                    level = row.iloc[1]

                # row.iloc[2] -> ID
                if pd.notnull(row.iloc[2]):
                    ID = int(row.iloc[2])

                # row.iloc[4] -> Game Mode
                if pd.notnull(row.iloc[4]):
                    game_mode = row.iloc[4]

                # row.iloc[5] ->Lighting
                if pd.notnull(row.iloc[5]):
                    lighting = row.iloc[5]

                # row.iloc[6] ->Tickets
                if pd.notnull(row.iloc[6]):
                    tickets = row.iloc[6]

                # row.iloc[7] ->Commander
                if pd.notnull(row.iloc[7]):
                    commander = row.iloc[7]

                # row.iloc[8] ->Layer Size*
                if pd.notnull(row.iloc[8]):
                    layer_size = row.iloc[8]

                # row.iloc[10] ->Notes
                if pd.notnull(row.iloc[10]):
                    notes = row.iloc[10]

                # row.iloc[12] ->Totals
                if pd.notnull(row.iloc[12]):
                    totals = row.iloc[12]

                # row.iloc[3] -> Layer Name
                if pd.notnull(row.iloc[3]):
                    layer_name = row.iloc[3]

                    layers.append(Layer(
                        level = level,
                        ID = ID,
                        layer_name = layer_name,
                        game_mode = game_mode,
                        lighting = lighting,
                        tickets = tickets,
                        commander = commander,
                        layer_size = layer_size,
                        notes = notes,
                        totals = totals,

                    ))

            return layers

def read_all_BG_layers(layers):
    # get local director
    current_directory = os.getcwd()

    # get file path
    files = os.listdir(current_directory)

    # get Layers.csv file
    for file in files:
        if file.endswith('ability.csv'):
            BGlayers = []
            for layer in layers:
                BGlayers.append(BGLayer(layer_name = layer.layer_name))

            file_path = os.path.join(current_directory, file)
            df = pd.read_csv(file_path)

            # ,,,Faction,Battle Group Type,Battle Group Name,Usable Teams,Vehicles (Link),,Changes,Notes
            level = ""
            layer_name = ""
            faction = ""
            battle_group_type = ""
            battle_group_name = ""
            usable_team = ""
            vehicles_link = ""

            for index, row in df.iloc[4:-2].iterrows():
                # Usable Teams
                if pd.notnull(row.iloc[6]):
                    # throw default
                    if row.iloc[6].endswith("Default"):
                        continue
                    else:
                        usable_team = row.iloc[6]

                # row.iloc[1] -> Level
                if pd.notnull(row.iloc[1]):
                    level = row.iloc[1]

                # row.iloc[2] -> Layer Name
                if pd.notnull(row.iloc[2]):
                    layer_name = row.iloc[2]

                # row.iloc[3] -> Faction
                if pd.notnull(row.iloc[3]):
                    faction = row.iloc[3]
                    battle_group_type = "CombinedArms"

                # row.iloc[4] -> Battle Group Type
                if pd.notnull(row.iloc[4]):
                    battle_group_type = row.iloc[4]

                # row.iloc[7] -> Vehicles_link
                if pd.notnull(row.iloc[7]):
                    vehicles_link = row.iloc[7]

                # row.iloc[5] -> Battle Group Name
                if pd.notnull(row.iloc[5]):
                    battle_group_name = row.iloc[5]

                    for index in range(0,len(BGlayers)):
                        if BGlayers[index].layer_name == layer_name:
                            # BlueForce Independent PAC RedForce
                            # BlueForce:    ADF BAF CAF USA USMC
                            # Independent:  IMF	MEI	MEA	TLF	WPMC
                            # PAC:          PLA	PLAAGF	PLANMC
                            # RedForce:     RGF	VDV
                            if faction == "ADF" or faction == "BAF" or faction == "CAF" or faction == "USA" or faction == "USMC":
                                BGlayers[index].blue_force.add(faction)
                            elif faction == "IMF" or faction == "INS" or faction == "MEA" or faction == "TLF" or faction == "WPMC":
                                BGlayers[index].independent.add(faction)
                            elif faction == "PLA" or faction == "PLAAGF" or faction == "PLANMC":
                                BGlayers[index].PAC.add(faction)
                            else:
                                BGlayers[index].red_force.add(faction)

                            temp = f"{faction}+{battle_group_type}"
                            if usable_team == "Team1":
                                BGlayers[index].team1.append(temp)
                            elif usable_team == "Team2":
                                BGlayers[index].team2.append(temp)
                            else:
                                BGlayers[index].team1.append(temp)
                                BGlayers[index].team2.append(temp)
                            break
            return BGlayers

def update_level(level, layer):
    mode = layer.game_mode
    if mode == "AAS" or mode == "RAAS":
        level.r_aas.append(layer)
        level.valid_count += 1
    elif mode == "Destruction":
        level.destruction.append(layer)
        level.valid_count += 1
    elif mode == "Insurgency":
        level.insurgency.append(layer)
        level.valid_count += 1
    elif mode == "Invasion":
        level.invasion.append(layer)
        level.valid_count += 1
    elif mode == "Seed":
        level.seed.append(layer)
    elif mode == "Skirmish":
        level.skirmish.append(layer)
        level.valid_count += 1
    elif mode == "TA":
        level.ta.append(layer)
    elif mode == "TerritoryControl":
        level.tc.append(layer)
        level.valid_count += 1
    elif mode == "Training":
        level.training.append(layer)

    return level

def get_level(layers):
    levels = []
    for layer in layers:
        flag = False
        if len(levels) == 0:
            name = layer.level.replace(" ", "")
            level = Level(name=name)
            level = update_level(level, layer)
            levels.append(level)
        else:
            for index, level in enumerate(levels):
                if level.name == layer.level.replace(" ", ""):
                    flag = True
                    levels[index] = update_level(level, layer)
                    break

            if not flag:
                name = layer.level.replace(" ","")
                level = Level(name = name)
                level = update_level(level, layer)
                levels.append(level)

    return levels

def get_candidate_layers(levels):
    # get level
    random_number_level = random.randint(0, len(levels) - 1)
    if levels[random_number_level].name == "JensensRange":
        return False, None
    else:
        temp_layer_list = []

        random_number_layer = random.randint(1, sum(WEIGHT_MODE))
        milestone = get_milestone(WEIGHT_MODE)

        if random_number_layer <= milestone[0]:
            for layer in levels[random_number_level].r_aas:
                temp_layer_list.append(layer)
        elif random_number_layer <= milestone[1]:
            for layer in levels[random_number_level].invasion:
                temp_layer_list.append(layer)
        elif random_number_layer <= milestone[2]:
            for layer in levels[random_number_level].skirmish:
                temp_layer_list.append(layer)
        elif random_number_layer <= milestone[3]:
            for layer in levels[random_number_level].tc:
                temp_layer_list.append(layer)
        else:
            for layer in levels[random_number_level].insurgency:
                temp_layer_list.append(layer)
            for layer in levels[random_number_level].destruction:
                temp_layer_list.append(layer)

        if len(temp_layer_list) == 0:
            return False, None
        else:
            random_number_layer_potential = random.randint(0, len(temp_layer_list) - 1)
            candidate = temp_layer_list[random_number_layer_potential]

        # check
        # at 70% Daytime
        random_number_layer_lighting = random.randint(1, sum(WEIGHT_LIGHT))
        milestone = get_milestone(WEIGHT_LIGHT)
        if random_number_layer_lighting <= milestone[0]:
            if candidate.lighting != "Daytime":
                return False, None
        else :
            if candidate.lighting == "Daytime":
                return False, None

        # at 60% Large
        random_number_layer_layer_size = random.randint(1, sum(WEIGHT_SIZE))
        milestone = get_milestone(WEIGHT_SIZE)
        if random_number_layer_layer_size <= milestone[0]:
            if candidate.layer_size != "Large":
                return False, None
        else :
            if candidate.layer_size == "Large":
                return False, None
    return True, candidate

def is_repeat(stack, target):
    test_set = set(stack)
    length_stake_before = len(test_set)
    test_set.add(target)
    if length_stake_before == len(test_set):
        return True
    else:
        return False

def update_stack(stack, stack_capacity, target):
    temp_stack = stack[:]
    temp_stack.append(target)
    if len(temp_stack)  <= stack_capacity:
        return temp_stack
    else:
        return temp_stack[-stack_capacity:]

def mode_IID_overflow(stack, stack_capacity, target):
    # Invasion/Insurgency/Destruction
    temp_stack = stack[:]
    temp_stack.append(target)
    count = 0
    if len(temp_stack) <= stack_capacity:
        temp = temp_stack
    else:
        temp = temp_stack[-stack_capacity:]

    for item in temp:
        if item == "Invasion" or item == "Insurgency" or item == "Destruction":
            count += 1

    if count > 1:
        return True
    else:
        return False

def lighting_not_daytime_overflow(stack, stack_capacity, target):
    temp_stack = stack[:]
    temp_stack.append(target)
    count = 0
    if len(temp_stack) <= stack_capacity:
        temp = temp_stack
    else:
        temp = temp_stack[-stack_capacity:]

    for item in temp:
        if item != "Daytime":
            count += 1

    if count > 1:
        return True
    else:
        return False

def layer_size_not_large_overflow(stack, stack_capacity, target):
    temp_stack = stack[:]
    temp_stack.append(target)
    count = 0
    if len(temp_stack) <= stack_capacity:
        temp = temp_stack
    else:
        temp = temp_stack[-stack_capacity:]

    for item in temp:
        if item != "Large":
            count += 1

    if count > 1:
        return True
    else:
        return False

def candidate_level_check(level_stack, mode_stack, lighting_stack, size_stack, candidate):
    _level_stack = level_stack
    _mode_stack = mode_stack
    _lighting_stack = lighting_stack
    _size_stack = size_stack
    if is_repeat(_level_stack, candidate.level):
        return False, None, None, None, None
    else:
        return_level_stack = update_stack(_level_stack, 10, candidate.level)

    if mode_IID_overflow(_mode_stack, 5, candidate.game_mode):
        return False, None, None, None, None
    else:
        return_mode_stack = update_stack(_mode_stack, 5, candidate.game_mode)

    if lighting_not_daytime_overflow(_lighting_stack, 5, candidate.lighting):
        return False, None, None, None, None
    else:
        return_lighting_stack = update_stack(_lighting_stack, 5, candidate.lighting)

    if layer_size_not_large_overflow(_size_stack, 3, candidate.layer_size):
        return False, None, None, None, None
    else:
        return_size_stack = update_stack(_size_stack, 3, candidate.layer_size)

    return True, return_level_stack, return_mode_stack, return_lighting_stack, return_size_stack

def get_factions(BG_layer):
    # B-I B-P B-R I-P I-R P-R I-I
    random_number_alliance = random.randint(1, sum(WEIGHT_ALLIANCE))
    milestone = get_milestone(WEIGHT_ALLIANCE)
    if random_number_alliance <= milestone[0]:
        # B-I blue_force = set()
        #         self.independent = set()
        #         self.red_force = set()
        #         self.PAC
        if len(BG_layer.blue_force) != 0 and len(BG_layer.independent) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.independent)
        else:
            return False, None, None
    elif random_number_alliance <= milestone[1]:
        # B-P
        if len(BG_layer.blue_force) != 0 and len(BG_layer.PAC) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.PAC)
        else:
            return False, None, None
    elif random_number_alliance <= milestone[2]:
        # B-R
        if len(BG_layer.blue_force) != 0 and len(BG_layer.red_force) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.red_force)
        else:
            return False, None, None
    elif random_number_alliance <= milestone[3]:
        # I-P
        if len(BG_layer.independent) != 0 and len(BG_layer.PAC) != 0:
            faction1_list = list(BG_layer.independent)
            faction2_list = list(BG_layer.PAC)
        else:
            return False, None, None
    elif random_number_alliance <= milestone[4]:
        # I-R
        if len(BG_layer.independent) != 0 and len(BG_layer.red_force) != 0:
            faction1_list = list(BG_layer.independent)
            faction2_list = list(BG_layer.red_force)
        else:
            return False, None, None
    elif random_number_alliance <= milestone[5]:
        # P-R
        if len(BG_layer.PAC) != 0 and len(BG_layer.red_force) != 0:
            faction1_list = list(BG_layer.PAC)
            faction2_list = list(BG_layer.red_force)
        else:
            return False, None, None
    else:
        # I-I
        if len(BG_layer.independent) >= 2:
            random_elements = random.sample(list(BG_layer.independent), 2)
            return True, random_elements[0], random_elements[1]
        else:
            return False, None, None

    return True, random.sample(faction1_list, 1)[0], random.sample(faction2_list, 1)[0]

def get_battle_group(faction1, faction2, BG_layer):
    # faction1 vs faction2
    battle_group_type1 = []
    battle_group_type2 = []
    for item in BG_layer.team1:
        if item.startswith(faction1):
            battle_group_type1.append(item.split("+")[1])
    for item in BG_layer.team2:
        if item.startswith(faction2):
            battle_group_type2.append(item.split("+")[1])

    random_number_level_battle_group_equal = random.randint(1, sum(WEIGHT_EQUAL))
    milestone = get_milestone(WEIGHT_EQUAL)

    # TODO: AI?
    if random_number_level_battle_group_equal <= milestone[0]:
        intersection = set(battle_group_type1).intersection(set(battle_group_type2))
        if len(intersection) != 0:
            select = random.sample(list(intersection), 1)[0]
            battle_group = f"{faction1}+{select} {faction2}+{select}"
            return True, True, battle_group
        else:
            return False, False, None
    else:
        if len(battle_group_type1) > 0 and len(battle_group_type2) > 0:
            battle_group_type1_select = random.sample(battle_group_type1, 1)[0]
            battle_group_type2_select = random.sample(battle_group_type2, 1)[0]
            battle_group = f"{faction1}+{battle_group_type1_select} {faction2}+{battle_group_type2_select}"
            if battle_group_type1_select == battle_group_type2_select:
                return True, True, battle_group
            else:
                return True, False, battle_group
        else:
            return False, False, None

def battle_group_not_balance_overflow(stack, stack_capacity, target):
    temp_stack = stack[:]
    temp_stack.append(target)
    count = 0
    if len(temp_stack) <= stack_capacity:
        temp = temp_stack
    else:
        temp = temp_stack[-stack_capacity:]

    for item in temp:
        if item != True:
            count += 1

    if count > 1:
        return True
    else:
        return False

def balance_check(balance_stack, target):
    if battle_group_not_balance_overflow(balance_stack, 5, target):
        return False, None
    else:
        balance_stack = update_stack(balance_stack, 5, target)
        return True, balance_stack

def map_get_or_default(map, key, default):
    if key in map:
        return map[key]
    else:
        return default

def get_alliance(str):
    if str == "ADF" or str == "BAF" or str == "CAF" or str == "USA" or str == "USMC":
        return "BlueForce"
    elif str == "IMF" or str == "INS" or str == "MEA" or str == "TLF" or str == "WPMC":
        return "Independent"
    elif str == "PLA" or str == "PLAAGF" or str == "PLANMC":
        return "PAC"
    else:
        return "RedForce"

def validating(output_layers):
    validation_result = []
    map_level = {}
    map_mode = {}
    map_alliance = {}
    map_faction = {}
    map_battle_group_type = {}
    count_balance = 0
    for str in output_layers:
        # map_level
        val_level = str.split(" ")[0].split("_")[0]
        map_level[val_level] = map_get_or_default(map_level, val_level, 0) + 1

        # map_mode
        val_mode = str.split(" ")[0].split("_")[1]
        map_mode[val_mode] = map_get_or_default(map_mode, val_mode, 0) + 1

        # map_faction
        val_faction1 = str.split(" ")[1].split("+")[0]
        val_faction2 = str.split(" ")[2].split("+")[0]
        map_faction[val_faction1] = map_get_or_default(map_faction, val_faction1, 0) + 1
        map_faction[val_faction2] = map_get_or_default(map_faction, val_faction2, 0) + 1
        # map_alliance
        val_alliance1 = get_alliance(val_faction1)
        val_alliance2 = get_alliance(val_faction2)
        map_alliance[val_alliance1] = map_get_or_default(map_alliance, val_alliance1, 0) + 1
        map_alliance[val_alliance2] = map_get_or_default(map_alliance, val_alliance2, 0) + 1

        # map_battle_group_type
        val_battle_group_type1 = str.split(" ")[1].split("+")[1]
        val_battle_group_type2 = str.split(" ")[2].split("+")[1]
        map_battle_group_type[val_battle_group_type1] = map_get_or_default(map_battle_group_type,
                                                                           val_battle_group_type1, 0) + 1
        map_battle_group_type[val_battle_group_type2] = map_get_or_default(map_battle_group_type,
                                                                           val_battle_group_type2, 0) + 1

        # balance count
        if val_battle_group_type1 == val_battle_group_type2:
            count_balance += 1

    validation_result.append("// ----------------------------------------------------------------")
    validation_result.append("// Level rate: ")
    for key, value in map_level.items():
        validation_result.append(f"// {key}: {100 * value / len(output_layers)}%")
    validation_result.append("// --------------------------------")
    validation_result.append("// Mode rate: ")
    for key, value in map_mode.items():
        validation_result.append(f"// {key}: {100 * value / len(output_layers)}%")
    validation_result.append("// --------------------------------")
    validation_result.append("// Alliance rate: ")
    for key, value in map_alliance.items():
        validation_result.append(f"// {key}: {100 * value / len(output_layers)}%")
    validation_result.append("// --------------------------------")
    validation_result.append("// Faction rate: ")
    for key, value in map_faction.items():
        validation_result.append(f"// {key}: {100 * value / len(output_layers)}%")
    validation_result.append("// --------------------------------")
    validation_result.append("// Battle group type rate: ")
    for key, value in map_battle_group_type.items():
        validation_result.append(f"// {key}: {100 * value / len(output_layers)}%")
    validation_result.append("// --------------------------------")
    validation_result.append(f"// Balanced rate: {100 * count_balance / len(output_layers)}%")
    validation_result.append("// ----------------------------------------------------------------")

    return validation_result

def main():
    # get layers from Map Layers.csv
    layers = read_all_layers()
    # get factions for layer from BG Layer Availability.
    BGLayers = read_all_BG_layers(layers)

    # get total Level
    levels = get_level(layers)

    output_layers = []

    level_stack = []
    mode_stack = []
    lighting_stack = []
    size_stack = []

    balance_stack = []

    while len(output_layers) < TOTAL_NUMBER:
    # for i in range(TOTAL_NUMBER):
        flag, candidate = get_candidate_layers(levels)
        if flag:
            check_result, temp_level_stack, temp_mode_stack, temp_lighting_stack, temp_size_stack= candidate_level_check(level_stack, mode_stack, lighting_stack, size_stack, candidate)
            if check_result:
                for BG_layer in BGLayers:
                    if BG_layer.layer_name == candidate.layer_name:
                        success_get_faction, faction1, faction2 = get_factions(BG_layer)

                        if success_get_faction:
                            random_number_level_faction_side = random.randint(0, 1)
                            if random_number_level_faction_side == 0:
                                success_get_battle_group, balance, battle_group = get_battle_group(faction1,
                                                                                                   faction2,
                                                                                                   BG_layer)
                            else:
                                success_get_battle_group, balance, battle_group = get_battle_group(faction2,
                                                                                                   faction1,
                                                                                                   BG_layer)

                            if success_get_battle_group:
                                sequential_balance_check, temp_balance_stack = balance_check(balance_stack, balance)
                                if sequential_balance_check:
                                    balance_stack = temp_balance_stack
                                    level_stack = temp_level_stack
                                    mode_stack = temp_mode_stack
                                    lighting_stack = temp_lighting_stack
                                    size_stack = temp_size_stack
                                    output_str = f"{candidate.layer_name} {battle_group}"
                                    output_layers.append(output_str)
                                    break
        else:
            continue

    validation_result = validating(output_layers)
    validation_file = os.path.join(FILEPATH, "LayerRotation_validation.txt")
    with open(validation_file, 'w') as file:
        for str in validation_result:
            print(str)
            file.write(str + '\n')
        
    file_index = 0
    start = True
    temp_list = []
    for i in range(len(output_layers)):
        if i % 200 == 0:
            if start:
                start = False
            else:
                layer_rotation_file_name = os.path.join(FILEPATH, f"LayerRotation_{file_index}.cfg")
                with open(layer_rotation_file_name, 'w') as file:
                    for str in temp_list:
                        file.write(str + '\n')
                temp_list = []
                file_index += 1
        temp_list.append(output_layers[i])
    layer_rotation_file_name = os.path.join(FILEPATH, f"LayerRotation_{file_index}.cfg")
    with open(layer_rotation_file_name, 'w') as file:
        for str in temp_list:
            file.write(str + '\n')


if __name__ == "__main__":
    main()