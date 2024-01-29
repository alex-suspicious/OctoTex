import torch
import torch.nn as nn
import torch.nn.functional as F


# Define a Convolution-BatchNorm-ReLU block

class down_sample(nn.Module):
    def __init__(self, input_nc, ngf, drop_out=False):
        """
        This class down samples through the network
        :param input_nc: int
        :param ngf: int
        :param batch_norm: bool
        """
        super(down_sample, self).__init__()

        if drop_out:
            self.sequence = nn.Sequential(
                nn.Conv2d(input_nc, ngf, kernel_size=4, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(ngf),
                nn.Dropout(0.2),
                nn.LeakyReLU()
            )
        else:
            self.sequence = nn.Sequential(
                nn.Conv2d(input_nc, ngf, kernel_size=4, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(ngf),
                nn.LeakyReLU()
            )

    def forward(self, x):
        return self.sequence(x)


class up_sample(nn.Module):
    def __init__(self, input_nc, ngf, drop_out=False):
        """
        This class up samples through the network
        :param input_nc: int
        :param ngf:  int
        :param drop_out: bool
        """
        super(up_sample, self).__init__()
        if drop_out:
            self.sequence = nn.Sequential(
                nn.ConvTranspose2d(input_nc, ngf, kernel_size=4, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(ngf),
                nn.Dropout(0.5),
                nn.LeakyReLU()
            )
        else:
            self.sequence = nn.Sequential(
                nn.ConvTranspose2d(input_nc, ngf, kernel_size=4, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(ngf),
                nn.LeakyReLU()
            )

    def forward(self, x):
        return self.sequence(x)


class PBR(nn.Module):
    def __init__(self):
        """
        This is a Generator architecture with skip connections.
        :param ngf: number of filters
        :param input_nc: number of input channels
        :param output_nc: number of output channels
        :param batch_norm: use batch norm
        """
        ngf = 64
        input_nc = 3
        output_nc = 3
        super(PBR, self).__init__()
        self.down_stack = nn.Sequential(
            down_sample(input_nc, ngf),
            down_sample(ngf, ngf * 2),
            down_sample(ngf * 2, ngf * 4),
            down_sample(ngf * 4, ngf * 8),
            down_sample(ngf * 8, ngf * 8),
            down_sample(ngf * 8, ngf * 8),
            down_sample(ngf * 8, ngf * 8),
            down_sample(ngf * 8, ngf * 8)
        )

        self.up_stack = nn.Sequential(
            up_sample(ngf * 8, ngf * 8, drop_out=True),
            up_sample(ngf * 16, ngf * 8, drop_out=True),
            up_sample(ngf * 16, ngf * 8, drop_out=True),
            up_sample(ngf * 16, ngf * 8, drop_out=True),
            up_sample(ngf * 16, ngf * 4),
            up_sample(ngf * 8, ngf * 2),
            up_sample(ngf * 4, ngf),
            nn.Upsample(scale_factor=2, mode='bilinear'),
        )
        self.last = nn.Sequential(
            nn.ConvTranspose2d(ngf * 2, output_nc, kernel_size=4, stride=2, padding=1),
            nn.Tanh()
        )

    def forward(self, x):
        "Down Sample Through Model"
        skips = []
        for down in self.down_stack:
            x = down(x)
            skips.append(x)  # Store each x to form skip connection to upsample

        skips = reversed(skips[:-1])

        "Upsampling Through Model"
        for up, skip in zip(self.up_stack, skips):
            x = up(x)
            x = torch.cat((x, skip), dim=1)
        x = self.last(x)
        return x


class NLayerDiscriminator(nn.Module):
    """Defines a PatchGAN discriminator, adopted from Junyaz
       Added comments and cleaned code.
       The result of a PatchGAN is a feature map which tells us if each patch is True or False
    """

    def __init__(self, input_nc, ndf=64, n_layers=3, norm_layer=nn.BatchNorm2d):
        """Construct a PatchGAN discriminator
        Parameters:
            input_nc (int)  -- the number of channels in input images
            ndf (int)       -- the number of filters in the last conv layer
            n_layers (int)  -- the number of conv layers in the discriminator
            norm_layer      -- normalization layer
        """
        super(NLayerDiscriminator, self).__init__()
        "Start a sequence with conv layer + leakyRelu"
        sequence = [nn.Conv2d(input_nc, ndf, kernel_size=4, stride=2, padding=1),
                    nn.LeakyReLU(0.2, True)]
        "Initialise constants that will control the number of filters in each layer as we progress"
        nf_mult = 1
        nf_mult_prev = 1

        "Depending on n_layers we will build a discriminator"
        for n in range(1, n_layers):
            "Update Values to have correct channel sizes"
            nf_mult_prev = nf_mult
            nf_mult = min(2 ** n, 8)  # limit max channels size to ndf * 8.

            sequence += [
                nn.Conv2d(ndf * nf_mult_prev, ndf * nf_mult, kernel_size=4, stride=2, padding=1),
                norm_layer(ndf * nf_mult),
                nn.LeakyReLU(0.2, True)
            ]

        nf_mult_prev = nf_mult
        nf_mult = min(2 ** n_layers, 8)

        "Second Last Layer"
        sequence += [
            nn.Conv2d(ndf * nf_mult_prev, ndf * nf_mult, kernel_size=4, stride=1, padding=1),
            norm_layer(ndf * nf_mult),
            nn.LeakyReLU(0.2, True)
        ]

        "Final layer"
        sequence += [nn.Conv2d(ndf * nf_mult, 1, kernel_size=4, stride=1, padding=1)]  # output 1 channel prediction map

        self.model = nn.Sequential(*sequence)

    def forward(self, input):
        """forward through discriminator"""
        return self.model(input)

def double_conv(in_channels, out_channels):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 3, padding=1),
        nn.BatchNorm2d(out_channels),
        nn.LeakyReLU(0.2, inplace=True),

        nn.Conv2d(out_channels, out_channels, 3, padding=1),
        nn.BatchNorm2d(out_channels),
        nn.LeakyReLU(0.2, inplace=True),
    )


class Unet(nn.Module):
    def __init__(self, d=64, out_channels=3):
        super(Unet, self).__init__()
        self.conv1 = nn.Conv2d(3, d, 4, 2, 1)
        self.conv2 = nn.Conv2d(d, d * 2, 4, 2, 1)
        self.conv2_bn = nn.BatchNorm2d(d * 2)
        self.conv3 = nn.Conv2d(d * 2, d * 4, 4, 2, 1)
        self.conv3_bn = nn.BatchNorm2d(d * 4)
        self.conv4 = nn.Conv2d(d * 4, d * 8, 4, 2, 1)
        self.conv4_bn = nn.BatchNorm2d(d * 8)
        self.conv5 = nn.Conv2d(d * 8, d * 8, 4, 2, 1)
        self.conv5_bn = nn.BatchNorm2d(d * 8)
        self.conv6 = nn.Conv2d(d * 8, d * 8, 4, 2, 1)
        self.conv6_bn = nn.BatchNorm2d(d * 8)
        self.conv7 = nn.Conv2d(d * 8, d * 8, 4, 2, 1)
        self.conv7_bn = nn.BatchNorm2d(d * 8)
        self.conv8 = nn.Conv2d(d * 8, d * 8, 4, 2, 1)

        self.deconv1 = nn.ConvTranspose2d(d * 8, d * 8, 4, 2, 1)
        self.deconv1_bn = nn.BatchNorm2d(d * 8)
        self.deconv2 = nn.ConvTranspose2d(d * 8 * 2, d * 8, 4, 2, 1)
        self.deconv2_bn = nn.BatchNorm2d(d * 8)
        self.deconv3 = nn.ConvTranspose2d(d * 8 * 2, d * 8, 4, 2, 1)
        self.deconv3_bn = nn.BatchNorm2d(d * 8)
        self.deconv4 = nn.ConvTranspose2d(d * 8 * 2, d * 8, 4, 2, 1)
        self.deconv4_bn = nn.BatchNorm2d(d * 8)
        self.deconv5 = nn.ConvTranspose2d(d * 8 * 2, d * 4, 4, 2, 1)
        self.deconv5_bn = nn.BatchNorm2d(d * 4)
        self.deconv6 = nn.ConvTranspose2d(d * 4 * 2, d * 2, 4, 2, 1)
        self.deconv6_bn = nn.BatchNorm2d(d * 2)
        self.deconv7 = nn.ConvTranspose2d(d * 2 * 2, d, 4, 2, 1)
        self.deconv7_bn = nn.BatchNorm2d(d)
        self.deconv8 = nn.Sequential(
            nn.ConvTranspose2d(d * 2, out_channels, 4, 2, 1),
            nn.Tanh()
            )

    def weight_init(self, mean, std):
        for m in self._modules:
            normal_init(self._modules[m], mean, std)

    def forward(self, input):
        e1 = self.conv1(input)
        e2 = self.conv2_bn(self.conv2(F.leaky_relu(e1, 0.2)))
        e3 = self.conv3_bn(self.conv3(F.leaky_relu(e2, 0.2)))
        e4 = self.conv4_bn(self.conv4(F.leaky_relu(e3, 0.2)))
        e5 = self.conv5_bn(self.conv5(F.leaky_relu(e4, 0.2)))
        e6 = self.conv6_bn(self.conv6(F.leaky_relu(e5, 0.2)))
        e7 = self.conv7_bn(self.conv7(F.leaky_relu(e6, 0.2)))
        e8 = self.conv8(F.leaky_relu(e7, 0.2))

        d1 = F.dropout(self.deconv1_bn(self.deconv1(F.relu(e8))), 0.5, training=True)
        d1 = torch.cat([d1, e7], 1)
        d2 = F.dropout(self.deconv2_bn(self.deconv2(F.relu(d1))), 0.5, training=True)
        d2 = torch.cat([d2, e6], 1)
        d3 = F.dropout(self.deconv3_bn(self.deconv3(F.relu(d2))), 0.5, training=True)
        d3 = torch.cat([d3, e5], 1)
        d4 = self.deconv4_bn(self.deconv4(F.relu(d3)))

        d4 = torch.cat([d4, e4], 1)
        d5 = self.deconv5_bn(self.deconv5(F.relu(d4)))
        d5 = torch.cat([d5, e3], 1)
        d6 = self.deconv6_bn(self.deconv6(F.relu(d5)))
        d6 = torch.cat([d6, e2], 1)
        d7 = self.deconv7_bn(self.deconv7(F.relu(d6)))
        d7 = torch.cat([d7, e1], 1)
        d8 = self.deconv8(F.relu(d7))
        
        return d8

def normal_init(m, mean, std):
    if isinstance(m, nn.ConvTranspose2d) or isinstance(m, nn.Conv2d):
        m.weight.data.normal_(mean, std)
        m.bias.data.zero_()