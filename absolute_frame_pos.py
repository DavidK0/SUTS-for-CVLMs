# returns a PP
def getFramePos(framePosIndex):
    if framePosIndex == 0:
        return "out of frame"
    elif framePosIndex == 1:
        return "at the top left"
    elif framePosIndex == 2:
        return "on the top"
    elif framePosIndex == 3:
        return "at the top right"
    elif framePosIndex == 4:
        return "on the left"
    elif framePosIndex == 5:
        return "in the middle"
    elif framePosIndex == 6:
        return "on the right"
    elif framePosIndex == 7:
        return "at the bottom left"
    elif framePosIndex == 8:
        return "on the bottom"
    elif framePosIndex == 9:
        return "at the bottom right"

# returns a P
def getRelationType(relation):
    relType = relation['type'].split("_")[1]
    if relType == "up":
        return "above"
    elif relType == "down":
        return "under"
    elif relType == "left":
        return "to the left of"
    elif relType == "right":
        return "to the right of"
    elif relType == "front":
        return "in front of"
    elif relType == "back":
        return "behind"

# takes a scene, scene index, and returns a model ID
def getModelID(scene, index):
    for obj in scene["objects"]:
        if obj["index"] == index:
            return obj["model"]

def run(scene):
    for obj in scene["objects"]:
        #print(obj)
        
        # infromation about the object
        name = getName(obj["model"])

        framePos = getFramePos(obj["framePos"])
        adjectives = models[obj["model"]]["adjectives"]
        
        # print its frame location
        print(f"The {name} is {framePos}.")
        
        # print its adjectives
        for adjective in adjectives:
            print(f"The {name} is {adjective}.")
        
        # print the relations
        for relation in obj["relations"]:
            rel_type = getRelationType(relation)
            rel_arg = getModelID(scene, relation["args"][0])
            print(f"The {name} is {rel_type} the {getName(rel_arg)}")