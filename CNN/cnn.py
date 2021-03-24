import torch
import torchvision
import torchvision.transforms as transforms

train_set = torchvision.datasets.FashionMNIST(
    root = './data/FashionMNIST',
    train=True, # data for the training set
    download = True,
    transform = transforms.Compose([
        transforms.ToTensor() # transform the data into tensors
    ])
)

train_loader = torch.utils.data.DataLoader(train_set)


