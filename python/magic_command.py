# Magic command for Jupyter Notebook

%%time     #Show run time
%%timeit   #Show average run time

%%bash     #Show run time, average run time

%matplotlib inline     #Show plot

%load_ext autoreload   #Auto reload code
%autoreload 2

%who_ls    #show used name
%who_ls function

%load_ext line_profiler
%lprun
