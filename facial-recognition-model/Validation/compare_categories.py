import os
import numpy as np
import pandas as pd

CATEGORIES = ['Devon', 'Declan']
NPHOTOS = 15

def diffNorm(first, second):
    return np.linalg.norm(first - second)

# For each category, take NPHOTOS embeddings and put them in a list
data = [[np.load(os.path.join('embeddings', c, path)) for path in os.listdir(os.path.join('embeddings', c))[:NPHOTOS]] for c in CATEGORIES]

# Columns for each norm comparison
cols = [
    "Average Norm Between Devon Photos",
    "Average Norm Between Declan Photos",
    "Average Norm Between Devon and Declan"
    ]

# Store the results
results = []

# Devon Photos
sum = 0
nnorms = 0
for i in range(len(data[0])):
    for j in range(i+1, len(data[0])):
        e1 = data[0][i]
        e2 = data[0][j]
        sum += diffNorm(e1, e2)
        nnorms += 1
results.append(sum / nnorms)

# Declan Photos
sum = 0
nnorms = 0
for i in range(len(data[1])):
    for j in range(i+1, len(data[1])):
        e1 = data[1][i]
        e2 = data[1][j]
        sum += diffNorm(e1, e2)
        nnorms += 1
results.append(sum / nnorms)

# Devon and Declan Photos
sum = 0
nnorms = 0
for i in range(len(data[0])):
    for j in range(len(data[1])):
        e1 = data[0][i]
        e2 = data[1][j]
        sum += diffNorm(e1, e2)
        nnorms += 1
results.append(sum / nnorms)

# Save the results
if not os.path.exists('results/'):
    os.makedirs('results/')

df = pd.DataFrame(data=[results], columns=cols)
df.to_csv('results/category_comparisons.csv')
