# /home/sungho/Downloads
import csv
import pandas as pd
import numpy as np
import os

PATH = "/home/sungho/Downloads/"

from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from datetime import datetime

sparseMatrixTrain = u_u_sim_sparse = sparse.load_npz(PATH+"spareMatrixTrain.npz")
sparseMatrixTest = u_u_sim_sparse = sparse.load_npz(PATH+"sparseMatrixTest.npz")
us,mv = sparseMatrixTrain.shape
elem = sparseMatrixTrain.count_nonzero()
print("Sparsity of Training matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )
us,mv = sparseMatrixTest.shape
elem = sparseMatrixTest.count_nonzero()
print("Sparsity of Testing matrix : {} % ".format(  (1-(elem/(us*mv))) * 100) )

# Computing User-User Similarity matrix
no_of_users, _ = sparseMatrixTrain.shape
org_rows, org_cols = sparseMatrixTrain.nonzero()
org_rows = sorted(set(org_rows))
# FIXME: Compute only to 100 users (100 ~ all)
top = 100
rows, cols, data = list(), list(), list()
usr = 0
for row in org_rows[:top]:
    usr = usr + 1
    sim = cosine_similarity(sparseMatrixTrain.getrow(row), sparseMatrixTrain).ravel()
    idx = sim.argsort()[-top:]
    val = sim[idx]
    rows.extend([row] * top)
    cols.extend(idx)
    data.extend(val)
    if usr % 20 == 0:
        print("computing done for "+str(usr)+" users")

u_u_sim_sparse = sparse.csr_matrix((data, (rows, cols)), shape=(no_of_users, no_of_users))
sparse.save_npz(PATH+"UserSimilarityMatrix.npz", u_u_sim_sparse)
u_u_sim_sparse = sparse.load_npz(PATH+"UserSimilarityMatrix.npz")
print('User Similarity Matrix Shape', u_u_sim_sparse.shape)

# Computing Movie-Movie Similarity matrix
m_m_sim_sparse = cosine_similarity(sparseMatrixTrain.T, dense_output=False)
sparse.save_npz(PATH+"MovieSimilarityMatrix.npz", m_m_sim_sparse)
m_m_sim_sparse = sparse.load_npz(PATH+"MovieSimilarityMatrix.npz")
print('Movie Similarity Matrix Shape', m_m_sim_sparse.shape)

# FIXME: example predicting similar movies id =40
id = 40
movie_titles = pd.read_csv(PATH+"movie_titles.csv", sep=',', header = None,
                           names=['movie_id', 'year_of_release', 'title'], verbose=True,
                      index_col = 'movie_id', encoding = "ISO-8859-1")
print("\nMovie",movie_titles.loc[id].values[1])
print("\nIt has {} Ratings.".format(sparseMatrixTrain[:,id].getnnz()))
print("\nWe have {} movies which are similar to this movie".format(m_m_sim_sparse[:,id].getnnz()))

