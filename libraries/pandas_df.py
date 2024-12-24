import numpy_arr as npa
import pandas as pd

# creating an array from numpy_arr module
print(f"creating array from numpy_arr module")
arr = npa.crt_arr()
print(f"the array created with shape {arr.shape} :\n{arr}")

# creating datafram from arr created
df = pd.DataFrame(arr)
print(f"Datafram created is :\n{df}")

# 