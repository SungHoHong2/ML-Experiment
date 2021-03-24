import torch
t = torch.Tensor([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# shape of 3 rows and 3 columns
# print(t.shape)

# shape of 1 row with 9 columns
# print(t.reshape(1,9))

# Create tensors without data
# print(torch.eye(2))
# print(torch.zeros(2,2))
# print(torch.ones(2,2))
# print(torch.rand(2,2))

# flatten function
def flatten(t):
    t = t.reshape(1,-1)
    t = t.squeeze()
    return t
# print(flatten(t))


# combine multiple tensors as a batch
t1 = torch.Tensor([[1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1]
                   ])
t2 = torch.Tensor([[2, 2, 2, 2],
                   [2, 2, 2, 2],
                   [2, 2, 2, 2],
                   [2, 2, 2, 2]
                   ])
t3 = torch.Tensor([[3, 3, 3, 3],
                   [3, 3, 3, 3],
                   [3, 3, 3, 3],
                   [3, 3, 3, 3]
                   ])

t = torch.stack((t1,t2,t3))
# print(t)
# [ batch size, height, width ]
# print(t.shape)


# reshape into [batch size, color channel, height, width]
t = t.reshape(3,1,4,4)
# print("first item in the batch", t[0])
# print('first color channel',t[0][0])
# print('first row',t[0][0][0])
# print('first column',t[0][0][0][0])

print(t.flatten(), t.shape)



