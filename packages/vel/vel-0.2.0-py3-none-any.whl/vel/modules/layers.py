"""
Code based on:
https://github.com/fastai/fastai/blob/master/fastai/layers.py
"""
import torch
import torch.nn as nn


class AdaptiveConcatPool2d(nn.Module):
    """ Concat pooling - combined average pool and max pool """
    def __init__(self, sz=None):
        super().__init__()
        sz = sz or (1, 1)
        self.ap = nn.AdaptiveAvgPool2d(sz)
        self.mp = nn.AdaptiveMaxPool2d(sz)

    def forward(self, x):
        return torch.cat([self.mp(x), self.ap(x)], 1)


class Lambda(nn.Module):
    """ Simple torch lambda layer """
    def __init__(self, f):
        super().__init__()
        self.f = f

    def forward(self, x):
        return self.f(x)


class Flatten(nn.Module):
    """ Flatten input vector """
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.view(x.size(0), -1)

