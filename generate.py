import numpy as np
import json

def generate_floyd_matrix(size=100, edge_probability=0.3, max_weight=50):
    inf = 1000000007
    matrix = np.full((size, size), inf)

    np.fill_diagonal(matrix, 0)
    
    for i in range(size):
        for j in range(size):
            if i != j:
                if np.random.rand() < edge_probability:
                    matrix[i][j] = np.random.randint(1, max_weight)
    
    matrix = matrix.tolist()
    return matrix

matrix = generate_floyd_matrix(200)
with open("matrix1.json", 'w') as f:
    json.dump(matrix, f, indent=4)