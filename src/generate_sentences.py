# This script takes the models file and scenes file from the unity scene generator
#   and then it generates true sentences about the images
# It takes an input a directory containing modelData.json and sceneData.json

import sys, json, os, random, re

# check for correct useage
if not (len(sys.argv) > 2 and os.path.isdir(sys.argv[1])):
    print(f"Usage: {sys.argv[0]} <input_directory> <output_file>")
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
        self.true = ""
        self.false = ""
    
    # (not implemented)
    # returns true iff the following condition are met
    #   exactly one tag is in the set (framePos,placement,orientation,size])
    #   exactly one tag is in the set (absolute,relative)
    #   exactly one tag is in neither of those sets
    #   'string' is non-empty
    def Check(self):
        hasTrueString = self.true != ""
        hasFalseString = self.false != ""
        
        return True
        return hasTrueString and hasFalseString
    
    
    def SetTrueString(self, string):
        self.true = self.Capitalize(self.FixArticles(string))
    
    
    def SetFalseString(self, string):
        self.false = self.Capitalize(self.FixArticles(string))
    
    # returns the capitalized version of the given string
    def Capitalize(self, string):
        return string[0].upper() + string[1:]
    
    # changes 'a' to 'an' where approriate
    # returns the resulting string
    def FixArticles(self, string):
        string = re.sub(" a ([aeiou])", r" an \1", string)
        string = re.sub("^a ([aeiou])", r"an \1", string)
        return string
    
    # exports the test instance
    def __str__(self):
        assert(self.Check())
        
        #return json.dumps({
        #    "true" : self.trueString,
        #    "false" : self.falseString}
        #)
        true = self.Capitalize(self.FixArticles(self.true))
        false = self.Capitalize(self.FixArticles(self.false))
        return json.dumps({
            "true" : true,
            "false" : false,
            "tags" : self.tags}
        )
    
    # equals only compares the true strings
    def __eq__(self, other):
        return self.true == other.true
    
    def __hash__(self):
        return self.true.__hash__()

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
    
## returns a tuple
## used in something like "the cat's left
#def GetPossesiveRelString(rel):
#    if GetRelType(rel) == "abs":
#        assert False, "Relative relation expected"
#    direc = GetRelDir(rel)
#    if direc == "up":
#        return "above"
#    elif direc == "down":
#        return "under"
#    elif direc == "left":
#        return "to the left of"
#    elif direc == "right":
#        return "to the right of"
#    elif direc == "forward":
#        return "in front of"
#    elif direc == "back":
#        return "behind"

# returns a P
def GetRelString(rel):
    direc = GetRelDir(rel)
    if direc == "up":
        return "above"
    elif direc == "down":
        return "under"
    elif direc == "left":
        return "to the left of"
    elif direc == "right":
        return "to the right of"
    elif direc == "forward":
        return "in front of"
    elif direc == "back":
        return "behind"
    else:
        assert False, f"Invalid relations {rel}, {direc}"

# returns a P
#def GetRelPlacementString(rel):
#    direc = GetRelDir(rel)
#    if direc == "left":
#        return "to the left of"
#    elif direc == "right":
#        return "to the right of"
#    elif direc == "forward":
#        return "facing"
#    elif direc == "back":
#        return "facing away from"
#    else:
#        assert False, f"Invalid relations {rel}, {direc}"

# returns 'abs' or 'rel'
def GetRelType(relation):
    relType = relation['type'].split("_")[0]
    if relType == "abs" or relType == "rel":
        return relType
    assert False, f"Invalid relation {relation}"

# returns up, down, left, etc.
def GetRelDir(relation):
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
    # check if this is the object of this 'noun' type in the scene
    nameCount = 0
    for obj in scene["objects"]:
        if GetNoun(obj) == noun:
            nameCount += 1
    assert nameCount > 0, f"Noun \"{noun}\" not found"
    return nameCount == 1

def Present3rdSG(verb):
    return f"{verb}s"

# returns an expected adverb for the given verb
def GetAdverb(verb):
    if verb == "sit" or verb == "stand":
        return "calmly"
    elif verb == "is":
        return ""
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
# uses both abs and rel relations
# set excludeVertical to true to not allow 'up' or 'down'
def GetEmptyDir(arg0s, arg1s, excludeVertical=False):
    if excludeVertical:
        dirs = set(["left", "right", "forward", "back"])
    else:
        dirs = set(["up", "down", "left", "right", "forward", "back"])
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
                if GetRelDir(rel) in dirs:
                    dirs.remove(GetRelDir(rel))
                break
    
    return random.choice(list(dirs))


def AbsoluteFramePosition(scene):
    #print(f"\nimage {scene['imageID']}")
    
    sentences = set()
    
    for obj in scene["objects"]:
        #print(obj)
        
        # infromation about the object
        model = models[obj["model"]]
        noun = GetNoun(obj)

        framePos = getFramePosString(obj["framePos"])
        adjectives = model["adjectives"]
        
        if IsUnique(scene, noun):
            art = "the"
        else:
            art = "a"
        
        # Sentence patterns
        
        # Basic
        s = Sentence(["abs_frame_pos", "basic"])
        s.SetTrueString(f"{art} {noun} is {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"{art} {noun} is {emptyFramePos}.")
        sentences.add(s)
        
        # Adjectives (visible)
        for adjective in adjectives:
            s = Sentence(["abs_frame_pos", "adjective", "visible_adjective"])
            s.SetTrueString(f"a {adjective} {noun} is {framePos}.")
            emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndAdjective(scene, noun, adjective)))
            s.SetFalseString(f"a {adjective} {noun} is {emptyFramePos}.")
            sentences.add(s)
        
        # Verb
        for verb in model["verbs"]:
            s = Sentence(["abs_frame_pos", "verb"])
            s.SetTrueString(f"a {noun} {Present3rdSG(verb)} {framePos}")
            emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndVerb(scene, noun, verb)))
            s.SetFalseString(f"a {noun} {Present3rdSG(verb)} {emptyFramePos}")
            sentences.add(s)
            
            # Adverb (expected)
            adverb = GetAdverb(verb)
            if adverb != None:
                s = Sentence(["abs_frame_pos", "verb", "adverb"])
                s.SetTrueString(f"a {noun} {Present3rdSG(verb)} {adverb} {framePos}")
                emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNounAndVerb(scene, noun, verb)))
                s.SetFalseString(f"a {noun} {Present3rdSG(verb)} {adverb} {emptyFramePos}")
                sentences.add(s)
        
        # Question
        s = Sentence(["abs_frame_pos", "question"])
        s.SetTrueString(f"is {art} {noun} {framePos}?")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"is {art} {noun} {emptyFramePos}?")
        sentences.add(s)
        
        # Command
        s = Sentence(["abs_frame_pos", "command"])
        s.SetTrueString(f"put {art} {noun} {framePos}!")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"put {art} {noun} {emptyFramePos}!")
        sentences.add(s)
        
        # Ungrammatical
        s = Sentence(["abs_frame_pos", "ungrammatical"])
        s.SetTrueString(f"than {noun} about is a {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"than {noun} about is a {emptyFramePos}.")
        sentences.add(s)
        
        # Filler
        s = Sentence(["abs_frame_pos", "filler"])
        s.SetTrueString(f"here is {art} {noun} which is {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"here is {art} {noun} which is {emptyFramePos}.")
        sentences.add(s)
        
        # Prompt-engineer: style_render
        s = Sentence(["abs_frame_pos", "style_render"])
        s.SetTrueString(f"a 3D render of a {noun} is {framePos}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"a 3D render of a {noun} is {emptyFramePos}.")
        sentences.add(s)
        
        # Prompt-engineer: style_picture
        s = Sentence(["abs_frame_pos", "style_picture"])
        s.SetTrueString(f"{art} {noun} is {framePos} of this picture.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"{art} {noun} is {emptyFramePos} of this picture.")
        sentences.add(s)
        
        # Prompt-engineer: repeat
        s = Sentence(["abs_frame_pos", "repeat"])
        s.SetTrueString(f"{art} {noun} is {framePos}. {framePos} is {art} {noun}.")
        emptyFramePos = getFramePosString(GetEmptyFramePosition(scene, GetByNoun(scene, noun)))
        s.SetFalseString(f"{art} {noun} is {emptyFramePos}. {emptyFramePos} is {art} {noun}.")
        sentences.add(s)
    return sentences

def RelativeFramePosition(scene):
    #print(f"\nimage {scene['imageID']}")
    
    sentences = set()
    
    for obj in scene["objects"]:
        #print(obj)
        for rel in obj["relations"]:
            if GetRelType(rel) != "abs":
                continue
            
            # infromation about the object
            model = models[obj["model"]]
            
            noun       = GetNoun(obj)
            adjectives = GetAdjectives(obj)
            
            direc = GetRelString(rel)
            arg1Noun = GetNoun(scene["objects"][rel["args"][0]])
            arg1Adjectives = GetAdjectives(scene["objects"][rel["args"][0]])
            arg1verbs = GetVerbs(scene["objects"][rel["args"][0]])
            
            if IsUnique(scene, noun):
                arg0Art = "the"
            else:
                arg0Art = "a"
            if IsUnique(scene, arg1Noun):
                arg1Art = "the"
            else:
                arg1Art = "a"
            
            # Sentence patterns
            
            # Basic 1
            s = Sentence(["rel_frame_pos", "basic1"])
            s.SetTrueString(f"{arg1Art} {arg1Noun} is {direc} {arg0Art} {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"{arg1Art} {arg1Noun} is {emptyFrameDir} {arg0Art} {noun}.")
            sentences.add(s)
            
            # Basic 2
            s = Sentence(["rel_frame_pos", "basic2"])
            dirRaw = rel['type'].split("_")[1]
            s.SetTrueString(f"{arg1Art} {arg1Noun} is further {dirRaw} than {arg0Art} {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            s.SetFalseString(f"{arg1Art} {arg1Noun} is further {emptyFrameDir} than {arg0Art} {noun}.")
            sentences.add(s)
            
            # Adjectives (visible)
            for adjective in adjectives:
                s = Sentence(["rel_frame_pos", "adjective", "visible_adjective"])
                if len(arg1Adjectives) > 0:
                    arg1Adjective = arg1Adjectives[0] + " "
                    emptyFrameDir = GetEmptyDir(GetByNounAndAdjective(scene, noun, adjective), GetByNounAndAdjective(scene, arg1Noun, arg1Adjectives[0]))
                else:
                    arg1Adjective = ""
                    emptyFrameDir = GetEmptyDir(GetByNounAndAdjective(scene, noun, adjective), GetByNoun(scene, arg1Noun))
                s.SetTrueString(f"a {arg1Adjective}{arg1Noun} is {direc} a {adjective} {noun}.")
                emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
                s.SetFalseString(f"a {arg1Adjective}{arg1Noun} is {emptyFrameDir} a {adjective} {noun}.")
                sentences.add(s)
            
            # Verb
            for verb in arg1verbs:
                s = Sentence(["rel_frame_pos", "verb"])
                s.SetTrueString(f"a {arg1Noun} {Present3rdSG(verb)} {direc} a {noun}")
                emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNounAndVerb(scene, arg1Noun, verb))
                emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
                s.SetFalseString(f"a {arg1Noun} {Present3rdSG(verb)} {emptyFrameDir} a {noun}")
                sentences.add(s)
                
                # Adverb (expected)
                adverb = GetAdverb(verb)
                if adverb != None:
                    s = Sentence(["rel_frame_pos", "verb", "adverb"])
                    s.SetTrueString(f"a {arg1Noun} {Present3rdSG(verb)} {adverb} {direc} a {noun}")
                    emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNounAndVerb(scene, arg1Noun, verb))
                    emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
                    s.SetFalseString(f"a {arg1Noun} {Present3rdSG(verb)} {adverb} {emptyFrameDir} a {noun}")
                    sentences.add(s)
            
            # Question
            s = Sentence(["rel_frame_pos", "question"])
            s.SetTrueString(f"is {arg1Art} {arg1Noun} {direc} {arg0Art} {noun}?")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"is {arg1Art} {arg1Noun} {emptyFrameDir} {arg0Art} {noun}?")
            sentences.add(s)
            
            # Command
            s = Sentence(["rel_frame_pos", "command"])
            s.SetTrueString(f"put {arg1Art} {arg1Noun} {direc} {arg0Art} {noun}!")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"put {arg1Art} {arg1Noun} {emptyFrameDir} {arg0Art} {noun}!")
            sentences.add(s)
            
            # Ungrammatical
            s = Sentence(["rel_frame_pos", "ungrammatical"])
            s.SetTrueString(f"than {arg1Noun} about is {direc} so {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"than {arg1Noun} about is {emptyFrameDir} so {noun}.")
            sentences.add(s)
            
            # Filler
            s = Sentence(["rel_frame_pos", "filler"])
            s.SetTrueString(f"here is {arg1Art} {arg1Noun} which is {direc} a {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"here is {arg1Art} {noun} which is {emptyFrameDir} {arg0Art} {noun}.")
            sentences.add(s)
        
            # Prompt-engineer: style_render
            s = Sentence(["rel_frame_pos", "style_render"])
            s.SetTrueString(f"a 3D render of a {arg1Noun} {direc} a {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"a 3D render of a {arg1Noun} {emptyFrameDir} a {noun}.")
            sentences.add(s)
            
            # Prompt-engineer: style_picture
            s = Sentence(["rel_frame_pos", "style_picture"])
            s.SetTrueString(f"in this picture, {arg1Art} {arg1Noun} is {direc} {arg0Art} {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"in this picture, {arg1Art} {arg1Noun} is {emptyFrameDir} {arg0Art} {noun}.")
            sentences.add(s)
            
            # Prompt-engineer: repeat
            s = Sentence(["rel_frame_pos", "repeat"])
            s.SetTrueString(f"{arg1Art} {arg1Noun} is {direc} {arg0Art} {noun}. {arg1Art} {arg1Noun} {direc} {arg0Art} {noun}.")
            emptyFrameDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyFrameDir = GetRelString({"type" : f"_{emptyFrameDir}"})
            s.SetFalseString(f"{arg1Art} {arg1Noun} is {emptyFrameDir} {arg0Art} {noun}. {arg1Art} {arg1Noun} {emptyFrameDir} {arg0Art} {noun}")
            sentences.add(s)
    return sentences

def GetRelativePlacementString(noun0, art0, noun1, art1, rel, adj1="", verb1="is", adj0="", verb0="is", adverb0="",adverb1=""):
    #print(noun0, art0, noun1, art1, rel, adj1, verb1, adj0)
    if adj0 != "":
        adj0 = adj0 + " "
    if adj1 != "":
        adj1 = adj1 + " "
    if verb0 != "":
        verb0 = " " + verb0
    if verb1 != "":
        verb1 = " " + verb1
    if adverb0 != "":
        adverb0 = " " + adverb0
    if adverb1 != "":
        adverb1 = " " + adverb1
    if verb0 != " is" and verb0 != "":
        verb0 = Present3rdSG(verb0)
    if verb1 != " is" and verb1 != "":
        verb1 = Present3rdSG(verb1)
    
    direc = GetRelDir(rel)
    if direc == "right" or direc == "left":
        return f"{art1} {adj1}{noun1}{verb1}{adverb1} to {art0} {adj0}{noun0}'s {direc}"
    elif direc == "forward":
        return f"{art0} {adj0}{noun0}{verb0}{adverb0} facing {art1} {adj1}{noun1}"
    elif direc == "back":
        return f"{art0} {adj0}{noun0}{verb0}{adverb0} facing away from {art1} {adj1}{noun1}"
    else:
        assert False, f"invalid relation {rel}"

def RelativePlacement(scene):
    #print(f"\nimage {scene['imageID']}")
    
    sentences = set()
    
    for obj in scene["objects"]:
        #print(obj)
        for rel in obj["relations"]:
            dirRaw = GetRelDir(rel)
            if GetRelType(rel) != "rel" or dirRaw == "up" or dirRaw == "down":
                continue
            #if
            #    # basic 1
            #    A toaster is to a cat's left.
            #    # basic 2
            #    A toaster is to the left of a cat.
            #else
            #    # basic 1
            #    A toaster is in front of a cat
            #    # basic 2
            #    A toaster is facing a cat
            
            # infromation about the object
            
            # infromation about the object
            model = models[obj["model"]]
            
            noun       = GetNoun(obj)
            adjectives = GetAdjectives(obj)
            
            #direc = GetRelPlacementString(rel)
            arg1Noun = GetNoun(scene["objects"][rel["args"][0]])
            arg1Adjectives = GetAdjectives(scene["objects"][rel["args"][0]])
            arg1verbs = GetVerbs(scene["objects"][rel["args"][0]])
            
            arg0verbs = GetVerbs(obj)
            if len(arg0verbs) == 0:
                arg0verbs = ["is"]
            verb0 = arg0verbs[0]
            adverb0 = GetAdverb(verb0)
            
            if IsUnique(scene, noun):
                arg0Art = "the"
            else:
                arg0Art = "a"
            if IsUnique(scene, arg1Noun):
                arg1Art = "the"
            else:
                arg1Art = "a"
            
            # Sentence patterns
            
            # Basic 1
            s = Sentence(["placement", "basic1"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel)
            s.SetTrueString(true + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"})
            s.SetFalseString(false + ".")
            sentences.add(s)
            
            # Basic 2
            s = Sentence(["placement", "basic2"])
            s.SetTrueString(f"{arg1Art} {arg1Noun} is {GetRelString(rel)} {arg0Art} {noun}.")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun))
            emptyDir = GetRelString({"type" : f"_{emptyDir}"})
            s.SetFalseString(f"{arg1Art} {arg1Noun} is {emptyDir} {arg0Art} {noun}.")
            sentences.add(s)
            
            # Adjectives (visible)
            for adjective in adjectives:
                s = Sentence(["placement", "adjective", "visible_adjective"])
                if len(arg1Adjectives) > 0:
                    arg1Adjective = arg1Adjectives[0]
                    emptyDir = GetEmptyDir(GetByNounAndAdjective(scene, noun, adjective), GetByNounAndAdjective(scene, arg1Noun, arg1Adjectives[0]), True)
                else:
                    arg1Adjective = ""
                    emptyDir = GetEmptyDir(GetByNounAndAdjective(scene, noun, adjective), GetByNoun(scene, arg1Noun), True)
                
                true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel, adj0=adjective,adj1=arg1Adjective)
                s.SetTrueString(true + ".")
                false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"}, adj0=adjective,adj1=arg1Adjective)
                s.SetFalseString(false + ".")
                sentences.add(s)
            
            # Verb
            if len(arg0verbs) == 0:
                arg0verbs.append("is")
            for verb1 in arg1verbs:
                s = Sentence(["placement", "verb"])
                true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb1=verb1,verb0=arg0verbs[0])
                s.SetTrueString(true + ".")
                emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
                verb0 = arg0verbs[0]
                false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb1=verb1,verb0=verb0)
                s.SetFalseString(false + ".")
                sentences.add(s)
            
                # Adverb (expected)
                
                adverb1 = GetAdverb(verb1)
                if adverb1 != None:
                    s = Sentence(["placement", "verb", "adverb"])
                    true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb1=verb1,verb0=arg0verbs[0],adverb1=adverb1,adverb0=adverb0)
                    s.SetTrueString(true + ".")
                    emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
                    false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb1=verb1,verb0=arg0verbs[0],adverb1=adverb1,adverb0=adverb0)
                    s.SetFalseString(false + ".")
                    sentences.add(s)
            
            # Question
            s = Sentence(["placement", "question"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb0="",verb1="")
            s.SetTrueString("is " + true + "?")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb0="",verb1="")
            s.SetFalseString("is " + false + "?")
            sentences.add(s)
            
            # Command
            s = Sentence(["placement", "command"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb0="",verb1="")
            s.SetTrueString("put " + true + "!")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb0="",verb1="")
            s.SetFalseString("put " + false + "!")
            sentences.add(s)
            
            # Ungrammatical
            s = Sentence(["placement", "ungrammatical"])
            true = GetRelativePlacementString(noun0=arg1Art,art0=noun,noun1=arg0Art,art1=arg1Noun,rel=rel)
            s.SetTrueString(true + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=arg1Art,art0=noun,noun1=arg0Art,art1=arg1Noun,rel={"type" : f"_{emptyDir}"})
            s.SetFalseString(false + ".")
            sentences.add(s)
            
            # Filler
            s = Sentence(["placement", "filler"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb0="which i",verb1="which i")
            s.SetTrueString("here is " + true + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb0="which i",verb1="which i")
            s.SetFalseString("here is " + false + ".")
            sentences.add(s)
        
            # Prompt-engineer: style_render
            s = Sentence(["placement", "style_render"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel)
            s.SetTrueString("In this 3D render, " + true + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"})
            s.SetFalseString("In this 3D render, " + false + ".")
            sentences.add(s)
            
            # Prompt-engineer: style_picture
            s = Sentence(["placement", "style_picture"])
            true = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel)
            s.SetTrueString("In this picture, " + true + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"})
            s.SetFalseString("In this picture, " + false + ".")
            sentences.add(s)
            
            # Prompt-engineer: repeat
            s = Sentence(["placement", "repeat"])
            true1 = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel)
            true2 = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel=rel,verb0="",verb1="")
            s.SetTrueString(true1 + ". " + true2 + ".")
            emptyDir = GetEmptyDir(GetByNoun(scene, noun), GetByNoun(scene, arg1Noun), True)
            false1 = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"})
            false2 = GetRelativePlacementString(noun0=noun,art0=arg0Art,noun1=arg1Noun,art1=arg1Art,rel={"type" : f"_{emptyDir}"},verb0="",verb1="")
            s.SetFalseString(false1 + ". " + false2 + ".")
            sentences.add(s)
    return sentences

def ObjectDetection(scene):
    sentences = set()
    
    # get the set of all nouns in this scene
    unique_nouns = set()
    for obj in scene["objects"]:
        noun = GetNoun(obj)
        unique_nouns.add(noun)
    
    # get the set of nouns not in this scene
    missing_nouns = set()
    for model in models:
        noun = models[model]["noun"]
        if noun not in unique_nouns:
            missing_nouns.add(noun)
    
    if len(missing_nouns) == 0:
        return sentences
    
    for noun in unique_nouns:
        # basic
        s = Sentence([f"object_detection_{noun}", "basic"])
        s.SetTrueString(f"a {noun}.")
        missing_noun = random.choice(list(missing_nouns))
        s.SetFalseString(f"a {missing_noun}.")
        sentences.add(s)
        
        # Prompt-engineering: style_picture
        s = Sentence([f"object_detection_{noun}", "style_picture"])
        s.SetTrueString(f"this picture has a {noun} in it.")
        missing_noun = random.choice(list(missing_nouns))
        s.SetFalseString(f"this picture has a {missing_noun} in it.")
        sentences.add(s)
        
        # Prompt-engineering: style_render
        s = Sentence([f"object_detection_{noun}", "style_render"])
        s.SetTrueString(f"this 3D render has a {noun} in it.")
        missing_noun = random.choice(list(missing_nouns))
        s.SetFalseString(f"this 3D render has a {missing_noun} in it.")
        sentences.add(s)
    return sentences

# create and overwrite this file
sys.stdout = open('framePos.txt', 'w')
sys.stdout.close()
sys.stdout = sys.__stdout__

output = {}
for scene in scenesData:
    file = f"image_{scene['imageID']}.png"
    output[file] = []
    for s in AbsoluteFramePosition(scene):
        output[file].append(s)
    for s in RelativeFramePosition(scene):
        output[file].append(s)
    for s in RelativePlacement(scene):
        output[file].append(s)
    for s in ObjectDetection(scene):
        output[file].append(s)

with open(sys.argv[2], "w") as out_file:
    out_file.write(json.dumps(output,default=lambda x: x.__dict__))