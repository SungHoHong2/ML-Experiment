import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
import torch.optim as optim

torch.set_printoptions(linewidth=120)

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=5)
        self.fc1 = nn.Linear(in_features=12 * 4 * 4, out_features=120)
        self.fc2 = nn.Linear(in_features=120, out_features=60)
        self.out = nn.Linear(in_features=60, out_features=10)

    def forward(self, t):
        # (1) input layer
        t = t

        # (2) hidden conv layer
        t = self.conv1(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # (3) hidden conv layer
        t = self.conv2(t)
        t = F.relu(t)
        t = F.max_pool2d(t, kernel_size=2, stride=2)

        # (4) hidden linear layer
        t = t.reshape(-1, 12 * 4 * 4)
        t = self.fc1(t)
        t = F.relu(t)

        # (5) hidden linear layer
        t = self.fc2(t)
        t = F.relu(t)

        # (6) ouptut layer
        t = self.out(t)
        # output: [1,10]
        # t = F.softmax(t, dim=1)
        return t

train_set = torchvision.datasets.FashionMNIST(
    root = '/Users/sunghohong/Desktop/data/FashionMNIST',
    train=True, # data for the training set
    download = True,
    transform = transforms.Compose([
        transforms.ToTensor() # transform the data into tensors
    ])
)

train_loader = torch.utils.data.DataLoader(train_set, batch_size = 100, shuffle=True)
network = Network()
optimizer = optim.Adam(network.parameters(), lr=0.01)

num_of_pixels = len(train_set) * 28 * 28
total_sum = 0
for batch in train_loader:
    total_sum += batch[0].sum()

mean = total_sum / num_of_pixels
sum_of_squared_error = 0
for batch in train_loader:
    sum_of_squared_error += ((batch[0]-mean).pow(2)).sum()
std = torch.sqrt(sum_of_squared_error / num_of_pixels)
print(mean, std)

# images, labels = next(iter(train_loader))
# grid = torchvision.utils.make_grid(images)

# tb = SummaryWriter()
# tb.add_image('images', grid)
# tb.add_graph(network, images)

# for epoch in range(10):
#     total_loss = 0
#
#     for batch in train_loader:
#         images, labels = batch
#
#         preds = network(images)
#         loss = F.cross_entropy(preds, labels)
#
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#
#         total_loss += loss.item()
#
#     print('epoch:', epoch, "loss", total_loss)
#     tb.add_scalar('Loss', total_loss, epoch)
#     tb.add_histogram('conv1.bais', network.conv1.bias, epoch)
#     tb.add_histogram('conv1.weight', network.conv1.weight, epoch)
#     tb.add_histogram('conv1.weight.grad', network.conv1.weight.grad, epoch)
# tb.close()