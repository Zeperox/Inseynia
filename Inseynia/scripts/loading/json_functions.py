import os, json

def load_json(location_list):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "r", encoding="utf8") as f:
        return json.load(f)

def dump_json(location_list, var):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "w", encoding="utf8") as f:
        json.dump(var, f, indent=4)