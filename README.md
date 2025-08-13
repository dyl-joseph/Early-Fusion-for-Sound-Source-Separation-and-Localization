# Early Fusion for Sound Separation and Localization via Sound and Video 
Inspired by the _Sound of Pixels_ paper, I slightly modify their architecture, because the audio generation does not take into account visual cues within a frame that could help with understanding where and how sound is produced at a region ([Zhao et. al. 2018](https://arxiv.org/abs/1804.03160)).

Using the early fusion method from _Co-Separating Sounds of Visual Objects_, I switched out the image backbone for a video backbone (3D ResNet) to encode video frames ([Gao and Grauman 2019](https://vision.cs.utexas.edu/projects/coseparation/)).

Unable to continue training due to insufficient compute. I was able to use a RTX 3060 (12 GB) to train for one epoch; however, I had to use a batch size of 2 (VRAM issue). Also, cost to train model :( 
