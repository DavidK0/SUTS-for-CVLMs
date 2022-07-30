# SUTS-for-CVLMs
This is project that I am completing as partial requirement for my CLMS degree from the UW. There are three main parts to the pipeline.
## Synthetic Image Generation
I used Unity to generate images. The Unity code is not included in this repo (yet).
## Sentence Generation
From the spatial relation metadata associated with the images made in the previous step, I use python to generate a set of true and false sentences.
## CVLM Testing
This test suite is designed to be used by contrastive vision-language models (CVLMs). For initial testing, I run the test suite through CLIP[[1]](#1).
## References
<a id="1">[1]</a> 
Dijkstra, E. W. (1968). 
Go to statement considered harmful. 
Communications of the ACM, 11(3), 147-148.