from markdowngenerator import MarkdownGenerator
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists, splitext
import json

def create_dir_if_ne(dir_name):
    if not exists(dir_name):
        makedirs(dir_name)

def load_pokemon_data():
    print(1)
    # cobblemon/common/src/main/resources/data/cobblemon/species/*/*.json

def load_world_conditions():
    data_path = "./cobblemon/common/src/main/resources/data/cobblemon/spawn_detail_presets/"
    world_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    base_path = "data/world_presets"
    create_dir_if_ne(base_path)

    for world_preset_file in world_files:
        preset_name = base_path + "/" + splitext(world_preset_file)[0]
        world_content = json.loads(open(join(data_path, world_preset_file), "r").read())
        write_world_preset(preset_name, world_content)
        
def write_world_preset(name, preset):
    with MarkdownGenerator(filename=(name + ".md"), enable_write=True) as doc:
        print(name)
        doc.addHeader(1, name)
        doc.addHeader(2, "Conditions")
        if "condition" in preset:
            if "minY" in preset["condition"]:
                doc.writeTextLine("Min Y: " + str(preset["condition"]["minY"]))

            if "maxY" in preset["condition"]:
                doc.writeTextLine("Max Y: " + str(preset["condition"]["maxY"]))

            if "biomes" in preset["condition"]:
                doc.addHeader(3, "Biomes")
                doc.addUnorderedList(preset["condition"]["biomes"])
        
            if "structures" in preset["condition"]:
                doc.addHeader(3, "Structures")
                doc.addUnorderedList(preset["condition"]["structures"])
            
            if "neededBaseBlocks" in preset["condition"]:
                doc.addHeader(3, "Needed Blocks")
                doc.addUnorderedList(preset["condition"]["neededBaseBlocks"])

        if "anticondition" in preset:
            doc.addHeader(2, "Anti-Conditions")
            if "minY" in preset["anticondition"]:
                doc.writeTextLine("Min Y: " + str(preset["anticondition"]["minY"]))
            
            if "maxY" in preset["anticondition"]:
                doc.writeTextLine("Max Y: " + str(preset["anticondition"]["maxY"]))

            if "biomes" in preset["anticondition"]:
                doc.addHeader(3, "Biomes")
                doc.addUnorderedList(preset["anticondition"]["biomes"])
        
            if "structures" in preset["anticondition"]:
                doc.addHeader(3, "Structures")
                doc.addUnorderedList(preset["anticondition"]["structures"])
            
            if "neededBaseBlocks" in preset["anticondition"]:
                doc.addHeader(3, "Needed Blocks")
                doc.addUnorderedList(preset["anticondition"]["neededBaseBlocks"])
        

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
            if spawn["pokemon"] == "dratini":
                print(spawn)
            doc.addHeader(2, spawn["id"])
            doc.writeTextLine("Rarity: " + spawn["bucket"])
            doc.writeTextLine("Levels: " + spawn["level"])
            presets_path = "data/spawn_data"
            if "presets" in spawn:
                doc.addHeader(3, "World Presets")
                for preset in spawn["presets"]:
                    doc.writeTextLine("* " + doc.generateHrefNotation(preset, presets_path + "/" + preset + ".md"))

            preset = spawn
            doc.addHeader(3, "Conditions")
            if "condition" in spawn:
                if "minY" in spawn["condition"]:
                    doc.writeTextLine("Min Y: " + str(preset["condition"]["minY"]))

                if "maxY" in spawn["condition"]:
                    doc.writeTextLine("Max Y: " + str(preset["condition"]["maxY"]))

                if "canSeeSky" in spawn["condition"]:
                    doc.writeTextLine("Can See Sky: " + ("True" if preset["condition"]["canSeeSky"] else "False"))

                if "biomes" in spawn["condition"]:
                    doc.addHeader(4, "Biomes")
                    doc.addUnorderedList(preset["condition"]["biomes"])
            
                if "structures" in spawn["condition"]:
                    doc.addHeader(4, "Structures")
                    doc.addUnorderedList(spawn["condition"]["structures"])
                
                if "neededBaseBlocks" in spawn["condition"]:
                    doc.addHeader(4, "Needed Blocks")
                    doc.addUnorderedList(spawn["condition"]["neededBaseBlocks"])

            if "anticondition" in spawn:
                doc.addHeader(3, "Anti-Conditions")
                if "minY" in spawn["anticondition"]:
                    doc.writeTextLine("Min Y: " + str(spawn["anticondition"]["minY"]))
                
                if "maxY" in spawn["anticondition"]:
                    doc.writeTextLine("Max Y: " + str(spawn["anticondition"]["maxY"]))

                if "canSeeSky" in spawn["anticondition"]:
                    doc.writeTextLine("Can See Sky: " + ("True" if preset["anticondition"]["canSeeSky"] else "False"))

                if "biomes" in spawn["anticondition"]:
                    doc.addHeader(4, "Biomes")
                    doc.addUnorderedList(spawn["anticondition"]["biomes"])
            
                if "structures" in spawn["anticondition"]:
                    doc.addHeader(4, "Structures")
                    doc.addUnorderedList(spawn["anticondition"]["structures"])
                
                if "neededBaseBlocks" in spawn["anticondition"]:
                    doc.addHeader(4, "Needed Blocks")
                    doc.addUnorderedList(spawn["anticondition"]["neededBaseBlocks"])


def main():
    create_dir_if_ne("data")
    load_world_conditions()
    load_pokemon_spawn_pool()

if __name__ == "__main__":
    main()