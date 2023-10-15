from markdowngenerator import MarkdownGenerator
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists, splitext
import json

def create_dir_if_ne(dir_name):
    if not exists(dir_name):
        makedirs(dir_name)

def load_pokemon_data():
    data_path = "./cobblemon/common/src/main/resources/data/cobblemon/species/"
    # cobblemon/common/src/main/resources/data/cobblemon/species/*/*.json
    generation_dirs = [d for d in listdir(data_path) if isdir(join(data_path, d))]

    pokedex_path = "data/pokedex"
    create_dir_if_ne(pokedex_path)

    for gen_dir in generation_dirs:
        generation_dir = join(data_path, gen_dir)
        mon_files = [f for f in listdir(generation_dir) if isfile(join(generation_dir, f))]
        for f in mon_files:
            mon_content = json.loads(open(join(generation_dir, f), "r").read())
            write_mon_data(mon_content)

def write_mon_data(mon):
    if "implemented" not in mon:
        # print(mon["name"])
        return
    if not mon["implemented"]:
        return
    dex_num = mon["nationalPokedexNumber"]
    normalized_num = ("0" * (4 - len(str(dex_num)))) + str(dex_num)
    
    file_name = "data/pokedex/" + (normalized_num + "_" + mon["name"].lower().replace(" ", "-"))
    print(file_name)

    with MarkdownGenerator(filename=(file_name + ".md"), enable_write=True) as doc:
        doc.addHeader(1, mon["name"])
        doc.writeTextLine("Primary Type: " + mon["primaryType"])
        if "secondaryType" in mon:
            doc.writeTextLine("Secondary Type: " + mon["secondaryType"])

        spawns_path = "/data/spawn_presets"
        doc.addHeader(2, "Spawn Locations")
        doc.writeTextLine(doc.generateHrefNotation(mon["name"], spawns_path + "/" + mon["name"].lower() + ".md"))
        
        doc.addHeader(2, "Abilities")
        doc.addUnorderedList(mon["abilities"])

        doc.addHeader(2, "Moves")
        moves_list = []
        for move in mon["moves"]:
            move_dat = move.split(":")
            moves_list.append({"Source" : move_dat[0], "Move" : move_dat[1]})
        doc.addTable(dictionary_list=moves_list)




def load_world_conditions():
    data_path = "./cobblemon/common/src/main/resources/data/cobblemon/spawn_detail_presets/"
    world_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    base_path = "data/world_presets"
    create_dir_if_ne(base_path)

    for world_preset_file in world_files:
        preset_name = base_path + "/" + splitext(world_preset_file)[0]
        world_content = json.loads(open(join(data_path, world_preset_file), "r").read())
        write_world_preset(preset_name, world_content)
        
def write_cond_anticond(doc, preset, depth):
    if "condition" in preset:
        doc.addHeader(depth, "Conditions")
        if "minY" in preset["condition"]:
            doc.writeTextLine("Min Y: " + str(preset["condition"]["minY"]))

        if "maxY" in preset["condition"]:
            doc.writeTextLine("Max Y: " + str(preset["condition"]["maxY"]))

        if "biomes" in preset["condition"]:
            doc.addHeader(depth+1, "Biomes")
            doc.addUnorderedList(preset["condition"]["biomes"])
    
        if "structures" in preset["condition"]:
            doc.addHeader(depth+1, "Structures")
            doc.addUnorderedList(preset["condition"]["structures"])
        
        if "neededBaseBlocks" in preset["condition"]:
            doc.addHeader(depth+1, "Needed Base Blocks")
            doc.addUnorderedList(preset["condition"]["neededBaseBlocks"])

        if "neededNearbyBlocks" in preset["condition"]:
            doc.addHeader(depth+1, "Needed Nearby Blocks")
            doc.addUnorderedList(preset["condition"]["neededNearbyBlocks"])
        
        if "fluid" in preset["condition"]:
            doc.writeTextLine("Fluid: " + str(preset["condition"]["fluid"]))

    if "anticondition" in preset:
        doc.addHeader(depth, "Anti-Conditions")
        if "minY" in preset["anticondition"]:
            doc.writeTextLine("Min Y: " + str(preset["anticondition"]["minY"]))
        
        if "maxY" in preset["anticondition"]:
            doc.writeTextLine("Max Y: " + str(preset["anticondition"]["maxY"]))

        if "biomes" in preset["anticondition"]:
            doc.addHeader(depth+1, "Biomes")
            doc.addUnorderedList(preset["anticondition"]["biomes"])
    
        if "structures" in preset["anticondition"]:
            doc.addHeader(depth+1, "Structures")
            doc.addUnorderedList(preset["anticondition"]["structures"])
        
        if "neededBaseBlocks" in preset["anticondition"]:
            doc.addHeader(depth+1, "Needed Blocks")
            doc.addUnorderedList(preset["anticondition"]["neededBaseBlocks"])

        if "neededNearbyBlocks" in preset["anticondition"]:
            doc.addHeader(depth+1, "Needed Nearby Blocks")
            doc.addUnorderedList(preset["anticondition"]["neededNearbyBlocks"])

        if "fluid" in preset["anticondition"]:
            doc.writeTextLine("Fluid: " + str(preset["anticondition"]["fluid"]))

def write_world_preset(name, preset):
    with MarkdownGenerator(filename=(name + ".md"), enable_write=True) as doc:
        print(name)
        doc.addHeader(1, name)
        write_cond_anticond(doc, preset, 2)
        
        

def load_pokemon_spawn_pool():
    data_path = "./cobblemon/common/src/main/resources/data/cobblemon/spawn_pool_world/"
    spawn_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    base_path = "data/spawn_presets"
    create_dir_if_ne(base_path)

    for spawn_preset_file in spawn_files:
        preset_name = base_path + "/" + splitext(spawn_preset_file.split("_")[1])[0]
        spawn_content = json.loads(open(join(data_path, spawn_preset_file), "r").read())
        write_spawn_data(preset_name, spawn_content)

def write_spawn_data(name, data):
    # Ignore unimplemented 'mons
    if not data["enabled"]:
        return
    # print(name)
    spawns = data["spawns"]
    with MarkdownGenerator(filename=(name + ".md"), enable_write=True) as doc:
        doc.addHeader(1, name + " spawns")
        for spawn in spawns:
            doc.addHeader(2, spawn["id"])
            doc.writeTextLine("Rarity: " + spawn["bucket"])
            doc.writeTextLine("Levels: " + spawn["level"])
            presets_path = "/data/world_presets"
            if "presets" in spawn:
                doc.addHeader(3, "World Presets")
                for preset in spawn["presets"]:
                    doc.writeTextLine("* " + doc.generateHrefNotation(preset, presets_path + "/" + preset + ".md"))

            preset = spawn
            write_cond_anticond(doc, preset, 3)


def main():
    create_dir_if_ne("data")
    load_world_conditions()
    load_pokemon_spawn_pool()
    load_pokemon_data()

if __name__ == "__main__":
    main()