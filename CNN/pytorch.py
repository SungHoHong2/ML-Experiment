import torch
t = torch.Tensor([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# shape of 3 rows and 3 columns
print(t.shape)

# shape of 1 row with 9 columns
print(t.reshape(1,9))











