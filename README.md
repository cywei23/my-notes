# Environment Setup / Frequently Used Commands

### Change Jupyter Notebook Starting Directory
`jupyter notebook --notebook-dir=//detasprod01/as/ford/cwei/`

### Jupyter Notebook Extension
- `conda install -c conda-forge jupyter_contrib_nbextensions`
- Put the setup folder in the path: C:\Users\cwei\AppData\Local\Continuum\anaconda3\Lib\site-packages\jupyter_contrib_nbextensions\nbextensions
- `jupyter contrib nbextensions install`

#### Useful Extensions
- Collapsible Headings
- ExecuteTime
- Scratchpad
- Setup
- Snippets
- spellchecker
- Variable inspecor

### Set up virtual environment & scrapy
- `python -V` use python 3.6.5
- `pip install virtualenv`
- `virtualenv virtual_workspace`
- `cd virtual_workspace`
- `Scripts\activate`
- `pip install scrapy==1.5.1`
- `scrapy startproject demo_project`
- `cd demo_project`
- `code .`
- Go to code and settings.json and type in "python.pythonPath": "C:\\Users\\CW\\virtual_workspace\\Scripts\\python.exe" then use python: create terminal
- `pip install pylint`
- Open Windows Powershell as administrator and type in `Set-ExecutionPolicy Unrestricted`
- `pip install pypiwin32`
- Use python: select interpreter and use the python.exe correct path one
- Run spider: `scrapy crawl goodreads -o ouputdata.json`

### Set up MongoDB
- Download community server edition from MongoDB.com
- Environment variables - system variables - path - new "C:\Program Files\MongoDb\Server\4.0\bin"
- Install Azure Cosmo DB extension to VS code
- `md "\data\db" "\data\log"`
- `mongod --dbpath="C:\data\db"`

### Set up scrapy-splash
- Download docker windows destop
- Go to the virtual workspace and `pip install scrapy-splash`
- `docker run -p 8050:8050 scrapinghub/splash`
- Go to browser and typ localhost:8050 and go the site want to do Lau script and render
- Go to the new project's settings.py and add `SPLAH_URL = 'http://localhost:8050'`, DOWNLOAD_MIDDLEWARES, SPIDER_MIDDLEWARES to the file
- `scrapy genspider -t basic usproxy us-proxy.org`

### Set up for Azure ML
- [Quickstart: Use the Python SDK to get started with Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-create-workspace-with-python?toc=%2Fen-us%2Fpython%2Fapi%2Foverview%2Fazure%2Fml%2Ftoc.json%3Fview%3Dazure-ml-py&bc=%2Fen-us%2Fpython%2Fazureml_py_breadcrumb%2Ftoc.json%3Fview%3Dazure-ml-py&view=azure-ml-py)
