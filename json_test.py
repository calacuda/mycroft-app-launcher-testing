from json import loads as json_reader

with open("settingsmeta.json", "r") as json_f:
    settings = json_reader(json_f.read())

print(json_reader(settings.get('skillMetadata').get('sections')[0].get('fields')[4].get('value').replace("'", '"')))
