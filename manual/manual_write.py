import numpy as np
import pandas as pd

df = pd.DataFrame(
    [
        dict(a=1, b=2),
        dict(a=3, b=np.nan),
        dict(a=np.nan, b=4),
        dict(a=999, b=999),
    ]
)
df.to_excel("/home/sr9000/Downloads/Test.xlsx")
