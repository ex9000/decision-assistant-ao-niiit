import uuid

import numpy as np

print(uuid.uuid4())

for k in range(2, 10):
    data = np.array(list(reversed([1 / (1 + x) for x in range(k)])))
    data = data.cumsum() / k
    print(data.round(2))
