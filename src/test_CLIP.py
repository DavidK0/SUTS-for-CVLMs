# This script loads CLIP and runs it though the test suite

import argparse, os, sys, json

parser = argparse.ArgumentParser(description='Runs CLIP')
parser.add_argument("input_file",type=str, help="A .txt containing the sentences")
parser.add_argument("images_dir",type=str, help="The directory containing the images")
parser.add_argument("output_file",type=str, help="The output file")
#parser.add_argument('--start_index', type=int, help="Where to start the run (default: 0)", default=0)
#parser.add_argument('--max_images',  type=int, help="How many images to read (default: 10,000)", default=10000)
#parser.add_argument('--model', type=int, help="0=ViT-B/32, 1=RN50x16")
args = parser.parse_args()

import torch
import clip
from PIL import Image
device = "cuda" if torch.cuda.is_available() else "cpu"
#if args.model == 0:
#    model_name = "ViT-B/32"
#elif args.model == 1:
#    model_name = "RN50x16"

# available models:
# RN50, RN101, RN50x4, RN50x16, RN50x64, ViT-B/32, ViT-B/16, ViT-L/14, ViT-L/14@336px

model_name = "ViT-B/32"
model, preprocess = clip.load(model_name, device=device) # load the model

# takes an image file name (eg. 2008_000003.jpg) and a text description
# returns the cosine similarity according to CLIP
#def CLIP_similarity(image: str, text: str):


    ## pre process
    #text = clip.tokenize(text).to(device)
    #image = preprocess(Image.open(image)).unsqueeze(0).to(device)
    #
    ## run through clip
    #with torch.no_grad():        
    #    logits_per_image, logits_per_text = model(image, text)
    #    probs = logits_per_image.cpu().numpy()
    #
    ## return cosine similarity
    #return probs[0][0]

# load the sentences
scenes = {}
curr_image = ""
with open(args.input_file) as in_file:
    scenes = json.load(in_file)

# count sentence
total_sentences = 0
for image_name, sentences in scenes.items():
    total_sentences += len(sentences)
#print("Total scentences: " + total_sentences)

# MAIN LOOP
sentence_counter = 0
correct = 0
for image_name, sentences in scenes.items():
    image_file = os.path.join(args.images_dir, image_name)
    image_input = preprocess(Image.open(image_file)).unsqueeze(0).to(device)
    for sentence in sentences:
        # Prepare the inputs
        true_text = clip.tokenize(sentence["true"])
        false_text = clip.tokenize(sentence["false"])
        text_inputs = torch.cat([true_text,false_text]).to(device)

        # Calculate features
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_inputs)

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(2)
        
        #for value, index in zip(values, indices):
        #    print(value, index)
        if indices[0] == 0:
            result = float(values[0]) > float(values[1])
        else:
            result = float(values[1]) > float(values[0])
        
        # get result
        #true_similarity  = CLIP_similarity(image_file, sentence["true"])
        #false_similarity = CLIP_similarity(image_file, sentence["false"])
        #result = int(true_similarity > false_similarity)
        
        # record result
        if result:
            correct += 1
        sentence["result"] = str(result)
        
        # print progress to console
        sentence_counter += 1
        progress = sentence_counter/total_sentences
        accuracy = correct/sentence_counter
        print(f"Progress: {progress:.1%}\tAccuracy: {accuracy:.1%}",end="\r")

print()

# export the new dataset
with open(args.output_file, "w") as out_file:
    out_file.write(json.dumps(scenes))

sys.exit()