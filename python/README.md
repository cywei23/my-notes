### Make a path
```python
import os
if not os.path.exists("images"):
    os.mkdir("images")
```

#### Organize folders
- keep code in scripts and data in data folder under the main folder like work/program, work/data
```python
import sys,os
sys.path = ['\\'.join(os.getcwd().split('\\')[:-1])]+list(sys.path)
from optml.optml_utilities.my_functions import *

# save to month specific folder
temp.to_parquet('..\\data\\outbound-oem\\{}_{}.parq'.format(oem,date.today().strftime('%Y-%m')))
```

#### Time
```python
begin = time.time()

print(since(begin,3),'notes')
```

#### Stack all files together
```python
df = pd.concat([pd.read_parquet(outpath+f) for f in os.listdir(outpath)])
````

#### Error handling
```python
if not oem in ['nissan','bmw','subaru','toyota','mazda']:
    raise BaseException('Invalid OEM: {}'.format(oem))
```
