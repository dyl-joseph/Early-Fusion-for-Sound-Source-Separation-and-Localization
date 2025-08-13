import torch
import torchvision
from .networks import Resnet, AudioVisual7layerUNet, AudioVisual5layerUNet, weights_init


class ModelBuilder():
    # builder for visual stream
    def build_visual(self, pool_type='avgpool', input_channel=3, fc_out=512, weights=''):
        net_vector = Resnet()
        
        return net_vector

    #builder for audio stream
    def build_unet(self, unet_num_layers=5, ngf=64, input_nc=1, output_nc=1, weights=''):
        if unet_num_layers == 7:
            net = AudioVisual7layerUNet(ngf, input_nc, output_nc)
        elif unet_num_layers == 5:
            net = AudioVisual5layerUNet(ngf, input_nc, output_nc)
        else:
            raise ValueError(f"Unsupported unet_num_layers: {unet_num_layers}")
        
        net.apply(weights_init)

        if len(weights) > 0:
            print('Loading weights for UNet')
            net.load_state_dict(torch.load(weights))
        
        return net

    def build_criterion(self, arch):
        if arch == 'bce':
            net = BCELoss()
        elif arch == 'l1':
            net = L1Loss()
        elif arch == 'l2':
            net = L2Loss()
        else:
            raise Exception('Architecture undefined!')
        return net
