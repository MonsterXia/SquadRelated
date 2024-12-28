import os
import random
import pandas as pd

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

# returns layers = [Layer, Layer, ...]
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
    elif mode == "TC":
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
        random_number_layer = random.randint(1, 100)
        if random_number_layer <= 40:
            for layer in levels[random_number_level].r_aas:
                temp_layer_list.append(layer)
        elif random_number_layer <= 55:
            for layer in levels[random_number_level].invasion:
                temp_layer_list.append(layer)
        elif random_number_layer <= 65:
            for layer in levels[random_number_level].skirmish:
                temp_layer_list.append(layer)
        elif random_number_layer <= 90:
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
        random_number_layer_lighting = random.randint(1, 10)
        if random_number_layer_lighting <= 7:
            if candidate.lighting != "Daytime":
                return False, None
        else :
            if candidate.lighting == "Daytime":
                return False, None

        # at 60% Large
        random_number_layer_layer_size = random.randint(1, 10)
        if random_number_layer_layer_size <= 6:
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
    stack.append(target)
    if len(stack)  <= stack_capacity:
        return stack
    else:
        return stack[-stack_capacity:]

def mode_IID_overflow(stack, stack_capacity, target):
    # Invasion/Insurgency/Destruction
    stack.append(target)
    count = 0
    if len(stack) <= stack_capacity:
        temp = stack
    else:
        temp = stack[-stack_capacity:]

    for item in temp:
        if item == "Invasion" or item == "Insurgency" or item == "Destruction":
            count += 1

    if count > 1:
        return True
    else:
        return False

def lighting_not_daytime_overflow(stack, stack_capacity, target):
    stack.append(target)
    count = 0
    if len(stack) <= stack_capacity:
        temp = stack
    else:
        temp = stack[-stack_capacity:]

    for item in temp:
        if item != "Daytime":
            count += 1

    if count > 1:
        return True
    else:
        return False

def layer_size_not_large_overflow(stack, stack_capacity, target):
    stack.append(target)
    count = 0
    if len(stack) <= stack_capacity:
        temp = stack
    else:
        temp = stack[-stack_capacity:]

    for item in temp:
        if item != "Large":
            count += 1

    if count > 1:
        return True
    else:
        return False

def candidate_level_check(level_stack, mode_stack, lighting_stack, size_stack, candidate):
    if is_repeat(level_stack, candidate.level):
        return False, None, None, None, None
    else:
        return_level_stack = update_stack(level_stack, 10, candidate.level)

    if mode_IID_overflow(mode_stack, 5, candidate.level):
        return False, None, None, None, None
    else:
        return_mode_stack = update_stack(mode_stack, 5, candidate.game_mode)

    if lighting_not_daytime_overflow(lighting_stack, 5, candidate.lighting):
        return False, None, None, None, None
    else:
        return_lighting_stack = update_stack(lighting_stack, 5, candidate.lighting)

    if layer_size_not_large_overflow(size_stack, 3, candidate.layer_size):
        return False, None, None, None, None
    else:
        return_size_stack = update_stack(size_stack, 3, candidate.layer_size)

    return True, return_level_stack, return_mode_stack, return_lighting_stack, return_size_stack

def get_factions(BG_layer):
    # B-I B-P B-R I-P I-R P-R I-I
    random_number_alliance = random.randint(1, 7)
    if random_number_alliance == 1:
        # B-I blue_force = set()
        #         self.independent = set()
        #         self.red_force = set()
        #         self.PAC
        if len(BG_layer.blue_force) != 0 and len(BG_layer.independent) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.independent)
        else:
            return False, None, None
    elif random_number_alliance == 2:
        # B-P
        if len(BG_layer.blue_force) != 0 and len(BG_layer.PAC) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.PAC)
        else:
            return False, None, None
    elif random_number_alliance == 3:
        # B-R
        if len(BG_layer.blue_force) != 0 and len(BG_layer.red_force) != 0:
            faction1_list = list(BG_layer.blue_force)
            faction2_list = list(BG_layer.red_force)
        else:
            return False, None, None
    elif random_number_alliance == 4:
        # I-P
        if len(BG_layer.independent) != 0 and len(BG_layer.PAC) != 0:
            faction1_list = list(BG_layer.independent)
            faction2_list = list(BG_layer.PAC)
        else:
            return False, None, None
    elif random_number_alliance == 5:
        # I-R
        if len(BG_layer.independent) != 0 and len(BG_layer.red_force) != 0:
            faction1_list = list(BG_layer.independent)
            faction2_list = list(BG_layer.red_force)
        else:
            return False, None, None
    elif random_number_alliance == 6:
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

    random_number_level_battle_group_equal = random.randint(1, 5)
    if random_number_level_battle_group_equal <= 4:
        intersection = set(battle_group_type1).intersection(set(battle_group_type2))
        if len(intersection) != 0:
            select = random.sample(list(intersection), 1)[0]
            battle_group = f"{faction1}+{select} {faction2}+{select}"
            return True, True, battle_group
        else:
            return False, False, None
    else:
        if len(battle_group_type1) > 0 and len(battle_group_type2) > 0:
            battle_group = f"{faction1}+{random.sample(battle_group_type1, 1)[0]} {faction2}+{random.sample(battle_group_type2, 1)[0]}"
            return True, False, battle_group
        else:
            return False, False, None

def battle_group_not_balance_overflow(stack, stack_capacity, target):
    stack.append(target)
    count = 0
    if len(stack) <= stack_capacity:
        temp = stack
    else:
        temp = stack[-stack_capacity:]

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


def main():
    TOTAL_NUMBER = 3000

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
            if len(output_layers) == 0:
                output_layers.append(candidate)
                level_stack.append(candidate.level)
                mode_stack.append(candidate.game_mode)
                lighting_stack.append(candidate.lighting)
                size_stack.append(candidate.layer_size)
            else:
                check_result, temp_level_stack, temp_mode_stack, temp_lighting_stack, temp_size_stack= candidate_level_check(level_stack, mode_stack, lighting_stack, size_stack, candidate)
                if check_result:
                    level_stack = temp_level_stack
                    mode_stack = temp_mode_stack
                    lighting_stack = temp_lighting_stack
                    size_stack = temp_size_stack
                    output_layers.append(candidate)
                else:
                    continue

            # Battle Group:
            # BlueForce Independent PAC RedForce
            # BlueForce:    ADF BAF CAF USA USMC
            # Independent:  IMF	INS	MEA	TLF	WPMC
            # PAC:          PLA	PLAAGF	PLANMC
            # RedForce:     RGF	VDV

            for BG_layer in BGLayers:
                if BG_layer.layer_name == candidate.layer_name:
                    print(BG_layer.layer_name, len(output_layers))
                    # # TODO: Insurgency?
                    # MAX_TRY = 200
                    # count = 0
                    # while count < MAX_TRY:
                    #     count += 1
                    #     success_get_faction, faction1, faction2 = get_factions(BG_layer)
                    #
                    #     if success_get_faction:
                    #         random_number_level_faction_side = random.randint(0, 1)
                    #         if random_number_level_faction_side == 0:
                    #             success_get_battle_group, balance, battle_group = get_battle_group(faction1, faction2,
                    #                                                                                BG_layer)
                    #         else:
                    #             success_get_battle_group, balance, battle_group = get_battle_group(faction2, faction1,
                    #                                                                                BG_layer)
                    #
                    #         if success_get_battle_group:
                    #             sequential_balance_check, temp_balance_stack = balance_check(balance_stack, balance)
                    #             if sequential_balance_check:
                    #                 balance_stack = temp_balance_stack
                    #                 print(f"{candidate.layer_name} {battle_group}")
                    #                 break
        else:
            continue

if __name__ == "__main__":
    main()









