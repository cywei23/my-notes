# Magic command for Jupyter Notebook

%%time     #Show run time
%%timeit   #Show average run time

%%bash     #Show run time, average run time

%matplotlib inline     #Show plot

%load_ext autoreload   #Auto reload code
%autoreload 2

%who_ls    #show used name
%who
%who_ls function

%load_ext line_profiler
%lprun

%run file.py           #run external python file

!ls -l     #use ! to access command line call


# Setup for display
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
