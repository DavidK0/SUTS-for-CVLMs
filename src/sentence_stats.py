import sys, json

with open(sys.argv[1]) as in_file:
    data = json.load(in_file)

class TagSet:
    def __init__(self, tags):
        self.tags = tags
    
    def __hash__(self):
        return "".join(self.tags).__hash__()
    
    def __eq__(self, other):
        boo = True
        for tag in self.tags:
            if tag not in other.tags:
                boo = False
        for tag in other.tags:
            if tag not in self.tags:
                boo = False
        return boo

tags = {}
objects = {}
tagSets = {}

object_detection = [0,0]

tag_vals = {}
tag_vals["abs_frame_pos"] = [0,0]
tag_vals["rel_frame_pos"] = [0,0]
tag_vals["placement"] = [0,0]
tag_vals["verb"] = [0,0]
tag_vals["adverb"] = [0,0]
tag_vals["adjective"] = [0,0]
tag_vals["question"] = [0,0]
tag_vals["command"] = [0,0]
tag_vals["filler"] = [0,0]
tag_vals["style_render"] = [0,0]
tag_vals["style_picture"] = [0,0]
tag_vals["repeat"] = [0,0]

total_sentences = 0
for image, sentences in data.items():
    total_sentences += len(sentences)
    for sentence in sentences:
        skip_tagSet = False
        for tag in sentence["tags"]:
            if tag not in tags:
                tags[tag] = [0,0]
            tags[tag][1] += 1
            if "result" in sentence and sentence["result"] == "True":
                tags[tag][0] += 1
            
            # count object detection
            if tag[:17] == "object_detection_":
                skip_tagSet = True
                name = tag[17:]
                if name not in objects:
                    objects[name] = 0
                objects[name] += 1
                object_detection[1] += 1
                if "result" in sentence and sentence["result"] == "True":
                    object_detection[0] += 1
        
        # tag set
        if not skip_tagSet:
            tagSet = TagSet(sentence["tags"])
            if tagSet not in tagSets:
                tagSets[tagSet] = [0,0]
            tagSets[tagSet][1] += 1
            if "result" in sentence and sentence["result"] == "True":
                tagSets[tagSet][0] += 1

for obj in objects:
    print(f"{obj}: {int(objects[obj]/3)}")
print()

def print_tag(tag):
    accuracy = tags[tag][0]/tags[tag][1]
    print(f"{tag}: {tags[tag][1]}, {accuracy:.1%}")

for tag in tags:
    print_tag(tag)
print()

print_tag("abs_frame_pos")
print_tag("rel_frame_pos")
print_tag("placement")
print()
print_tag("verb")
print_tag("adverb")
print_tag("adjective")
print()
print_tag("question")
print_tag("command")
print_tag("filler")
print()
print_tag("style_picture")
print_tag("style_render")
print_tag("repeat")
print()

print(f"object detection: {(object_detection[0]/object_detection[1]):.1%}")
print()

for tagSet, result in tagSets.items():
    print(f"{tagSet.tags}, {result}, {(result[0]/result[1]):.1%}")

print()
print(f"Total images: {len(data)}")
print(f"Total sentences: {total_sentences}")