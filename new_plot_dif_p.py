import pandas as pd
import originpro as op
import sys
from scipy.io import loadmat
import numpy as np

# Very useful, especially during development, when you are
# liable to have a few uncaught exceptions.
# Ensures that the Origin instance gets shut down properly.
# Note: only applicable to external Python.
# Ensures that the Origin instance gets shut down properly.
def origin_shutdown_exception_hook(exctype, value, traceback):
    op.exit()
    sys.__excepthook__(exctype, value, traceback)


if op and op.oext:
    sys.excepthook = origin_shutdown_exception_hook

# Set Origin instance visibility.
# Important for only external Python.
# Should not be used with embedded Python.
if op.oext:
    op.set_show(True)




# matlab data by scipy
mat_data = loadmat("H:/postgraduate/matlab/newdata_gamma_invT_dif_p.mat")




op.new()  # create a project

# import data
wks_1 = op.new_sheet('w', 'first dataset')
wks_1.from_list(0, mat_data['x_data'], units=' ', lname='1000/T', axis='X')

params = np.logspace(1, 5, 5)  # floating-point
y_data_key = [None] * len(params)
gamma_data_struct = mat_data['gamma_data_struct']  # two-dimension index
field_names = gamma_data_struct.dtype.names  # Get the names of the fields
#   loop input data
for i, param in enumerate(params):  # the number of i is from 0
    param_int = int(param)
    y_data_key = f'Pa{param_int if param.is_integer() else param}'  # make sure it can show Pa10
    if y_data_key in field_names:
        wks_1.from_list(i + 1, list(gamma_data_struct[0, 0][y_data_key]), units='', lname=f'{param_int}Pa ', axis='Y')
    else:
        print(f"Key {y_data_key} not found in gamma_data_struct")


# create plot
graph = op.new_graph(template='gamma_invT')  # some problems could be happened if the template is unsuitable
gl = graph[0]

# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:end)', type='l')  # crazy, l is L!; (?,1:end) means all

# group the plots and control plots setting in group
gl.group(True, 0, -1)


# adjust axisXY
gl.set_xlim(10, 1e5)
gl.set_ylim(1e-4, 1e-1)
gl.xscale = 'log10'
gl.yscale = 'log10'

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_first_graph.opju')
