import sys, json

# load the results
with open(sys.argv[1]) as in_file:
    results = json.load(in_file)

tags = {}

for image, sentences in results.items():
    for sentence in sentences:
        for tag in sentence["tags"]:
            if tag not in tags:
                tags[tag] = [0,0]
            tags[tag][1] += 1
            if sentence["result"] == "True":
                tags[tag][0] += 1

for tag in tags:
    accuracy = tags[tag][0]/tags[tag][1]
    
    print(f"{tag}: {accuracy:.1%}")