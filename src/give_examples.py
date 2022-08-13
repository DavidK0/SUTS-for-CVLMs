import sys, json

with open(sys.argv[1]) as in_file:
    data = json.load(in_file)

for image, sentences in data.items():
    for sentence in sentences:
        if "abs_frame_pos" in sentence["tags"] and "result" in sentence and sentence['result'] == "False" and "style_picture" in sentence["tags"] and "middle" not in sentence['true'] and "bottom" not in sentence['true']:
            print(f"{image}, {sentence['true']}, {sentence['false']}")

    #if image == "image_4.png":
    #        if "orientation" in sentence["tags"]:
    #            #print(f"{sentence['true']},{sentence['false']}")
    #            pass
    #        print(sentence)
                