# SUTS-for-CVLMs
This repository contains a spatial understanding (SU) test suite (TS) for vision-language models (VLMs) in fulfillment of the project option for the CLMS degree from the University of Washington. Read the paper at docs/Final Paper.pdf

The test suite consists of pairs of true and false sentences which truly or falsely describe a caption. THe goal of the VLM is to identify the true caption. By using different sentence structure, I can test what lingustic features affect the performance of VLM.

The two steps to creating this data set were:
* Synthetic Image Generation: I used Unity to generate images (not included in this repo).
* Sentence Generation: From the spatial relation metadata associated with the images made in the previous step, I use python to generate a set of true and false sentences.

I tested CLIP's performance on this test suite, and it performed very poorly, at or worse than random guessing.

More information about this test suite can be found at the [the wiki.](../../wiki)
