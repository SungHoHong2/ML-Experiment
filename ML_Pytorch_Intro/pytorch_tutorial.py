import torch
# create a 3d dimensions
torch.empty(2,2,3)
# create 2d random values
torch.rand(2,3)
# create 2d zero values
x = torch.zeros(2,3)
# check the type of the matrix
print(x.dtype)
# set up 2d zero matrix with int values
x = torch.zeros(2,3, dtype=torch.int)
x = torch.zeros(2,3, dtype=torch.float16)
x = torch.zeros(2,3, dtype=torch.double)
print(x.dtype)
print(x.size())
x = torch.tensor([2.5,0.1])

# adding the tensor
x = torch.rand(2,2)
y = torch.rand(2,2)
print(x)
print(y)







