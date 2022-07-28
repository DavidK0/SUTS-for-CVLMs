# This script takes the models file and scenes file from the unity scene generator
#   and then it generates true sentences about the images
# It takes an input a directory containing modelData.json and sceneData.json

import sys, json, os, random

os.system("cls")

# check for correct useage
if not (len(sys.argv) > 1 and os.path.isdir(sys.argv[1])):
    print(f"Usage: {sys.argv[0]} <output_directory>")
    sys.exit()

# find the important files
modelsFile = os.path.join(sys.argv[1], "modelData.json")
scenesFile = os.path.join(sys.argv[1], "sceneData.json")

# check that the important files exist
if not os.path.isfile(modelsFile):
    print(f"Couldn't find modelData.json at {modelsFile}")
    sys.exit()
if not os.path.isfile(scenesFile):
    sys.exit()
    print(f"Couldn't find sceneData.json.json at {scenesFile}")

# load the important files
with open(modelsFile) as in_file:
    modelsData = json.load(in_file)["models"]
with open(scenesFile) as in_file:
    scenesData = json.load(in_file)["scenes"]

# process models so it is accessed according to model_ID
#   model_ID = noun_nounIndex
models = {}
for model in modelsData:
    model_ID = model["noun"] + "_" + str(model["nounIndex"])
    models[model_ID] = model

# represents a single test instance 
class Sentence:
    
    def __init__(self, tags):
        assert(type(tags) == type(list()))
        self.tags = tags
        self.trueString = ""
        self.falseString = ""
    
    # (not implemented)
    # returns true iff the following condition are met
    #   exactly one tag is in the set (framePos,placement,orientation,size])
    #   exactly one tag is in the set (absolute,relative)
    #   exactly one tag is in neither of those sets
    #   'string' is non-empty
    def Check(self):
        hasTrueString = self.trueString != ""
        hasFalseString = self.falseString != ""
        
        return True
        return hasTrueString and hasFalseString
    
    
    def SetTrueString(self, string):
        self.trueString = string
    
    
    def SetFalseString(self, string):
        self.falseString = string
    
    # exports the test instance
    def __str__(self):
        assert(self.Check())
        
        return json.dumps({
            "true" : self.trueString,
            "false" : self.falseString}
        )
        #return json.dumps({
        #    "true" : self.trueString,
        #    "false" : self.falseString,
        #    "tags" : self.tags}
        #)

# returns a PP
def getFramePosString(framePosIndex):
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
    else:
        assert False, f"Unknown frame position index \"{framePosIndex}\""

# returns a P
def GetDirStringReversed(relation):
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

# returns 'abs' or 'rel'
def GetDirType(relation):
    relType = relation['type'].split("_")[0]
    if relType == "abs" or relType == "rel":
        return relType
    assert False, f"Invalid relation {relation}"

# returns up, down, left, etc.
def GetDirDir(relation):
    return relation['type'].split("_")[1]

# takes a scene, scene index, and returns a model ID
def getModelID(scene, index):
    for obj in scene["objects"]:
        if obj["index"] == index:
            return obj["model"]

# returns an N
def GetNoun(model):
    return models[model["model"]]["noun"]

# returns a list of adjs
def GetAdjectives(model):
    return models[model["model"]]["adjectives"]

# returns an V
def GetVerbs(model):
    return models[model["model"]]["verbs"]


# returns true if there is only one object with the given noun in the given scene
def IsUnique(scene, noun):
    noun = GetNoun(scene["objects"][index])
    
    # check if this is the object of this 'noun' type in the scene
    nameCount = 0
    for obj in scene["objects"]:
        if GetNoun(obj) == name:
            nameCount += 1
    assert nameCount > 0, f"Noun \"{noun}\" not found"
    return nameCount == 1

def Present3rdSG(verb):
    return f"{verb}s"

# returns an expected adverb for the given verb
def GetAdverb(verb):
    if verb == "sit" or verb == "stand":
        return "calmly"
    else:
        assert False, f"Unknown verb \"{verb}\""

# returns the list of objects from the given scene
#   which match the given object by noun
def GetByNoun(scene, noun):
    return_list = []
    for obj in scene["objects"]:
        if GetNoun(obj) == noun:
            return_list.append(obj)
    assert len(return_list) > 0, f"No matching objects found: {noun}"
    return return_list

# returns the list of objects from the given scene
#   which match the given object by noun and adjective
def GetByNounAndAdjective(scene, noun, adjective):
    return_list = []
    for obj in scene["objects"]:
        if GetNoun(obj) == noun and adjective in models[obj["model"]]["adjectives"]:
            return_list.append(obj)
    assert len(return_list) > 0, f"No matching objects found: {noun, adjective}"
    return return_list

# returns the list of objects from the given scene
#   which match the given object by noun and verb
def GetByNounAndVerb(scene, noun, verb):
    return_list = []
    for obj in scene["objects"]:
        if GetNoun(obj) == noun and verb in models[obj["model"]]["verbs"]:
            return_list.append(obj)
    assert len(return_list) > 0, f"No matching objects found: {noun, verb}"
    return return_list

# returns a random frame position from the list of frame positions
#   which do not contain any of the given objects
def GetEmptyFramePosition(scene, objects):
    positions = set([1,2,3,4,5,6,7,8,9])
    for i in range(1,10):
        for obj in objects:
            if obj["framePos"] == i:
                positions.remove(i)
                break
    assert(len(positions)) > 0 # no valid positions
    return random.choice(list(positions))

# returns one random directions for which there is no element from arg1s
#   which is in the that direction of any of the arg0s
def GetDirString(arg0s, arg1s):
    dirs = set(["up", "down", "left", "right", "front", "back"])
    for obj1 in arg0s:
        for rel in obj1["relations"]:
            index1 = rel["args"][0]
            empty = True
            for obj2 in arg1s:
                index2 = obj2["index"]
                if index1 == index2:
                    empty = False
                    break
            if empty == False:
                dirs.remove(GetDirDir(rel))
                break
    
    return random.choice(list(dirs))
                

def AbsoluteFramePosition(scene):
    print(f"\nimage {scene['imageID']}")
    
    for obj in scene["objects"]:
        #print(obj)
        
        # infromation about the object
        model = models[obj["model"]]
        noun = GetNoun(obj)

        framePos = getFramePosString(obj["framePos"])
        adjectives = model["adjectives"]
        
        # Sentence patterns
        
        # Basic
        s = Sentence(["framePos", "absolute", "basic"])
        s.SetTrueString(f"A {noun} is {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"A {noun} is {emptyFramePos}.")
        print(s)
        
        # Adjectives (visible)
        for adjective in adjectives:
            s = Sentence(["framePos", "absolute", "adjective", "visible_adjective"])
            s.SetTrueString(f"A {adjective} {noun} is {framePos}.")
            emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndAdjective(scene, noun, adjective)))
            s.SetFalseString(f"A {adjective} {noun} is {emptyFramePos}.")
            print(s)
        
        # Verb
        for verb in model["verbs"]:
            s = Sentence(["framePos", "absolute", "verb"])
            s.SetTrueString(f"A {noun} {Present3rdSG(verb)} {framePos}")
            emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndVerb(scene, noun, verb)))
            s.SetFalseString(f"A {noun} {Present3rdSG(verb)} {emptyFramePos}")
            print(s)
            
            # Adverb (expected)
            adverb = GetAdverb(verb)
            if adverb != None:
                s = Sentence(["framePos", "absolute", "verb", "adverb"])
                s.SetTrueString(f"A {noun} {Present3rdSG(verb)} {adverb} {framePos}")
                emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndVerb(scene, noun, verb)))
                s.SetFalseString(f"A {noun} {Present3rdSG(verb)} {adverb} {emptyFramePos}")
                print(s)
        
        # Question
        s = Sentence(["framePos", "absolute", "question"])
        s.SetTrueString(f"Is a {noun} {framePos}?")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"Is a {noun} {emptyFramePos}?")
        print(s)
        
        # Command
        s = Sentence(["framePos", "absolute", "command"])
        s.SetTrueString(f"Put a {noun} {framePos}!")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"Put a {noun} {emptyFramePos}!")
        print(s)
        
        # Ungrammatical
        s = Sentence(["framePos", "absolute", "ungrammatical"])
        s.SetTrueString(f"Than {noun} about is a {framePos}?")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"Than {noun} about is a {emptyFramePos}?")
        print(s)
        
        # Filler
        s = Sentence(["framePos", "absolute", "filler"])
        s.SetTrueString(f"Here is a {noun} which is {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"Here is a {noun} which is {emptyFramePos}.")
        print(s)

def RelativeFramePosition(scene):
    print(f"\nimage {scene['imageID']}")
    
    for obj in scene["objects"]:
        #print(obj)
        for rel in obj["relations"]:
            if GetDirType(rel) != "abs":
                continue
        
        # infromation about the object
        model = models[obj["model"]]
        
        noun       = GetNoun(obj)
        adjectives = GetAdjectives(obj)
        verbs      = GetVerbs(obj)
        
        direc = GetDirStringReversed(rel)
        arg1Noun = GetNoun(scene["objects"][rel["args"][0]])
        arg1Adjectives = GetAdjectives(scene["objects"][rel["args"][0]])
        arg1Verb = GetVerbs(scene["objects"][rel["args"][0]])
        
        # Sentence patterns
        
        # Basic
        s = Sentence(["framePos", "absolute", "basic"])
        s.SetTrueString(f"A {arg1Noun} is {direc} a {noun}.")
        emptyFrameDir = GetDirString(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
        emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
        s.SetFalseString(f"A {arg1Noun} is {emptyFrameDir} a {noun}.")
        print(s)
        
        # Adjectives (visible)
        for adjective in adjectives:
            s = Sentence(["framePos", "absolute", "adjective", "visible_adjective"])
            if len(arg1Adjectives) > 0:
                arg1Adjective = arg1Adjectives[0] + " "
                emptyFrameDir = GetDirString(GetByNounAndAdjective(scene, noun, adjective), GetByNounAndAdjective(scene, arg1Noun, arg1Adjectives[0]))
            else:
                arg1Adjective = ""
                emptyFrameDir = GetDirString(GetByNounAndAdjective(scene, noun, adjective), GetByNoun(scene, arg1Noun))
            s.SetTrueString(f"A {adjective} {arg1Noun} is {direc} a {arg1Adjective}{noun}.")
            emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"A {adjective} {arg1Noun} is {emptyFrameDir} a {arg1Adjective}{noun}.")
            print(s)
        
        # Verb
        for verb in verbs:
            s = Sentence(["framePos", "absolute", "verb"])
            s.SetTrueString(f"A {arg1Noun} {Present3rdSG(verb)} {direc} a {noun}")
            emptyFrameDir = GetDirString(GetByNounAndVerb(scene, noun, verb), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"A {arg1Noun} {Present3rdSG(verb)} {emptyFrameDir} a {noun}")
            print(s)
            
            # Adverb (expected)
            adverb = GetAdverb(verb)
            if adverb != None:
                s = Sentence(["framePos", "absolute", "verb", "adverb"])
                s.SetTrueString(f"A {arg1Noun} {Present3rdSG(verb)} {adverb} {direc} a {noun}")
                emptyFrameDir = GetDirString(GetByNounAndVerb(scene, noun, verb), GetByNoun(scene, arg1Noun))
                emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
                s.SetFalseString(f"A {arg1Noun} {Present3rdSG(verb)} {adverb} {emptyFrameDir} a {noun}")
                print(s)
        
        # Question
        s = Sentence(["framePos", "absolute", "question"])
        s.SetTrueString(f"Is a {arg1Noun} {direc} a {noun}?")
        emptyFrameDir = GetDirString(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
        emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
        s.SetFalseString(f"Is a {arg1Noun} {emptyFrameDir} a {noun}?")
        print(s)
        
        # Command
        s = Sentence(["framePos", "absolute", "command"])
        s.SetTrueString(f"Put a {arg1Noun} {direc} a {noun}!")
        emptyFrameDir = GetDirString(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
        emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
        s.SetFalseString(f"Put a {arg1Noun} {emptyFrameDir} a {noun}!")
        print(s)
        return
        
        # Ungrammatical
        s = Sentence(["framePos", "absolute", "ungrammatical"])
        s.SetTrueString(f"Than {arg1Noun} about is a {framePos}?")
        emptyFrameDir = GetDirString(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
        emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
        s.SetFalseString(f"Than {arg1Noun} about is a {emptyFramePos}?")
        print(s)
        
        # Filler
        s = Sentence(["framePos", "absolute", "filler"])
        s.SetTrueString(f"Here is a {arg1Noun} which is {framePos}.")
        emptyFrameDir = GetDirString(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
        emptyFrameDir = GetDirStringReversed({"type" : f"_{emptyFrameDir}"})
        s.SetFalseString(f"Here is a {noun} which is {emptyFramePos}.")
        print(s)
        
        print()

def other():
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

# create and overwrite this file
sys.stdout = open('framePos.txt', 'w')
sys.stdout.close()
sys.stdout = sys.__stdout__

for scene in scenesData:
    #print(f"\nimage {scene['imageID']}")
    
    #sys.stdout = open('framePos.txt', 'a')
    
    AbsoluteFramePosition(scene)
    #RelativeFramePosition(scene)
    
    #sys.stdout = sys.__stdout__
