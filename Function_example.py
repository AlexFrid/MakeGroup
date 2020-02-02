import pandas as pd
from makegroups import makegroups

df = pd.read_json("testdata.json")

df2 = makegroups(df)

print(df2)
