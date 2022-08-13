# This script takes the models file and scenes file from the unity scene generator
#   and then it generates true sentences about the images
# It takes an input a directory containing modelData.json and sceneData.json

import sys, json, os, random, re

scenesFiles = []
for i in range(5):
    scenesFiles.append(os.path.join(sys.argv[1], f"scene_{i}_data.json"))

for scenesFile in scenesFiles:
    if not os.path.isfile(scenesFile):
        print(f"Couldn't find sceneData.json.json at {scenesFile}")
        sys.exit()

scenesDatas = []
for scenesFile in scenesFiles:
    scenesDatas.append([])
    with open(scenesFile) as in_file:
        scenesDatas[len(scenesDatas)-1] += json.load(in_file)["scenes"]

output = {}
rels = 0
imgs = 0
for i in range(len(scenesDatas)):
    scenesData = scenesDatas[i]
    for scene in scenesData:
        imgs += 1
        for obj in scene["objects"]:
            rels += len(obj["relations"])
print(rels,imgs)