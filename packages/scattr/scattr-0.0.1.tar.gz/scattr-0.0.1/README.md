# The `scattr` Python package

The `scattr` package has one function, `scattr`,
that provides an easy way to
**S**et **C**lass **ATTR**ibutes of classes derived
from pre-existing Python classes.

The `scattr` function takes 
- a class object and
- the name of a helper script
and returns a subclass called `SubClassAttributes`
that contains the methods defined in the helper script.

Essentially, this is an easy way to
add user-defined functions to classes.

Class variables, method and classes can be added dynamically:
```python
import pandas as pd
import math
# add pi to a pandas DataFrame
pd.DataFrame.pi = math.pi
```

The `scattr` package provides a cleaner way to 
add new attributes, because it creates a new subclass and
uses method and class defined in a separate helper script. 

The `scattr` function only adds
callable objects(methods and classes), not variables.

## Pandas DataFrame example
```python
import pandas as pd
from scattr import scattr

# create a new class that inherits from pd.DataFrame
# and includes methods defined in a 'helper.py' file
ScattrFrame = scattr(cls=pd.DataFrame, src='helper')

# instantiate the new class
df = ScattrFrame(data=pd.read_csv('risk_factors_cervical_cancer.csv'))

# test methods added from helper file
df.say_hi()

# test CowClass added from helper file
df.CowClass.say_moo()

# test method from parent class
df.head(n=1)

# confirm that df is an instance of pd.DataFrame and PydyFrame
isinstance(df, (pd.DataFrame, ScattrFrame))

# confirm that ScattrFrame is a subclass of pd.DataFrame
issubclass(ScattrFrame, pd.DataFrame)
```