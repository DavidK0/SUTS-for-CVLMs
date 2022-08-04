import sys, json

with open(sys.argv[1]) as in_file:
    data = json.load(in_file)

for image, sentences in data.items():

    if image == "image_4.png":
        for sentence in sentences:
            if "orientation" in sentence["tags"]:
                #print(f"{sentence['true']},{sentence['false']}")
                pass
            print(sentence)
                