# This script takes the models file and scenes file from the unity scene generator
#   and then it generates true sentences about the images

import json

# the location of the key files
modelsFile = "C:/Users/David/Documents/Programing/Unity/Master's Project/Assets/Output/modelData.json"
scenesFile = "C:/Users/David/Documents/Programing/Unity/Master's Project/Assets/Output/sceneData.json"

# load the files
with open(modelsFile) as in_file:
	modelsData = json.load(in_file)["models"]
with open(scenesFile) as in_file:
	scenesData = json.load(in_file)["scenes"]

# process models so it is accessed according to model_ID
#   model_ID = noun + nounIndex
models = {}
for model in modelsData:
	models[model["noun"] + "_" + str(model["nounIndex"])] = model

for model in models:
	print(model)

print()
	
for object in scenesData[0]["objects"]:
	print(models[object["model"]])