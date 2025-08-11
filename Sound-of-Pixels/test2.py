import torch
from arguments import ArgParser
from dataset import MUSICMixDataset
from models import networks
from utils import AverageMeter, \
    recover_rgb, magnitude2heatmap,\
    istft_reconstruction, warpgrid, \
    combine_video_audio, save_video, makedirs, save_wav
import torch.nn.functional as F
import matplotlib.pyplot as plt



parser = ArgParser()
args = parser.parse_train_arguments()
device = 'cuda'

visual_extractor = networks.Resnet()
visual_extractor.eval()
visual_extractor.to(device)

audio_net = networks.AudioVisual7layerUNet()
audio_net.eval()
audio_net.to(device)



dataset_train = MUSICMixDataset(
		args.list_val, args, split='val')

loader_train = torch.utils.data.DataLoader(
		dataset_train,
		batch_size=8,
		shuffle=True,
		num_workers=6,
		drop_last=True)

for i, batch_data in enumerate(loader_train):
	
	mag_mix = batch_data['mag_mix']
	mags = batch_data['mags']
	frames = batch_data['frames']
	
	mag_mix = mag_mix + 1e-10

	N = args.num_mix
	B = mag_mix.size(0)
	T = mag_mix.size(3)

	### calculate video features ###
	frames = frames.to(device)
	print(f"input size: {frames.shape}")
	
	video_1, video_2 = frames[:,0,:,:,:,:], frames[:,1,:,:,:,:]
	# print(video_1.shape)
	# print(video_2.shape)

	out1 = visual_extractor(video_1)  
	out2 = visual_extractor(video_2)
	print(f"out vals {out1.shape}")

	### calculate audio features ###
	
	feat_sound = audio_net(log_mag_mix, out1)

	print(feat_sound.shape)
	
	### visualize outputs ###
	break