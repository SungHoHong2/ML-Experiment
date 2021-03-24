import torch
import torchvision
import torchvision.transforms as transforms

import numpy as np
import matplotlib.pyplot as plt
torch.set_printoptions(linewidth=120)

train_set = torchvision.datasets.FashionMNIST(
    root = './data/FashionMNIST',
    train=True, # data for the training set
    download = True,
    transform = transforms.Compose([
        transforms.ToTensor() # transform the data into tensors
    ])
)

# allows to shuffle, and provie batch-size of the data
train_loader = torch.utils.data.DataLoader(train_set, batch_size = 10)

"""
reading the training set 
"""
# print(len(train_set))
# print(train_set.train_labels)
# give use the frequency distribution of the labels
# print(train_set.train_labels.bincount())

"""
reading a training sample 
"""
sample = next(iter(train_set))
# sample = train_set[0]
print(len(sample))
# return a 2D array with a label
image, label = sample
print(image, label)

"""
reading from a batch sample 
"""
batch = next(iter(train_loader))
print(len(batch))
images, labels = batch
print(len(images), len(labels))
# 10 batches, 1 color, y=28, x=28
print(images.shape)
# 10 batches
print(labels.shape)

grid = torch

# http://localhost:8888/lab?token=33923aa70f01c416fcaaca14dde2cc9e0c0e6b7d5b43486c
# http://192.168.0.15:8004/lab?token=33923aa70f01c416fcaaca14dde2cc9e0c0e6b7d5b43486c

