### Organize folders
- keep code in scripts and data in data folder under the main folder like work/program, work/data

```python
import sys,os
sys.path = ['\\'.join(os.getcwd().split('\\')[:-1])]+list(sys.path)
from optml.optml_utilities.my_functions import *
```
