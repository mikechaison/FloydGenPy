import json
import time
from multiprocessing import Pool

with open('matrix1.json', 'r') as f:
    matrix = json.load(f)

dist=matrix.copy()
n=len(dist)

start = time.time()
for k in range(n):
    for i in range(n):
        for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

end = time.time()
print(f"Execution time: {end - start}")

print(dist[0][n-1])