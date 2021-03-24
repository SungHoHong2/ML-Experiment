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






