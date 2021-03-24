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

# allows to shuffle, and provie batch-size of the data
train_loader = torch.utils.data.DataLoader(train_set, batch_size = 10)








