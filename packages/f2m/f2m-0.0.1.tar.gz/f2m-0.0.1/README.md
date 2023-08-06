# f2m: Turn user-defined functions into methods
## Pandas DataFrame example
```python
import pandas as pd
from f2m import f2m

# create a new class that inherits from pd.DataFrame
# and includes methods defined in a 'helper.py' file
F2mFrame = f2m(cls=pd.DataFrame, src='helper')

# instantiate the new class
df = F2mFrame(data=pd.read_csv('risk_factors_cervical_cancer.csv'))

# test methods added from helper file
df.say_hi()
df.say_moo()

# test method from parent class
df.head(n=1)

# confirm that df is an instance of pd.DataFrame and PydyFrame
isinstance(df, (pd.DataFrame, F2mFrame))

# confirm that F2mFrame is a subclass of pd.DataFrame
issubclass(F2mFrame, pd.DataFrame)
```