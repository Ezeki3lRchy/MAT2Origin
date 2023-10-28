import originpro as op
import sys
from scipy.io import loadmat
import math
import re


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
filename = 'omega_pressure_dif_flux'
mat_data = loadmat(f"H:/postgraduate/matlab/newdata_{filename}.mat")


op.new()  # create a new project
# op.open(op.path('u') + f'new_plot_{filename}.opju')  # open a project

# import data
wks_1 = op.new_sheet('w', f'{filename}')  # create a new sheet
# wks_1 = op.find_sheet('w', f'{filename}')  # find a worksheet

wks_1.from_list(0, mat_data['x_data'],   # import x_data
                units='Pa', lname='Pressure', axis='X')


#   loop input Y_data
params = ['ad', 'des', 'ER', 'LH']  # [1300, 1500, 1700, 1900] #  floating-point # 2-D matrix
#       Flatten params if it's not a 1D array

for i, param in enumerate(params):
    wks_1.from_list(i + 1, mat_data[f'omega_{param}_O_values'], units='',
                    lname=f'\g(w)\i(\-({param},O))', axis='Y')





# create plot  # some problems could be happened if the template is unsuitable
graph = op.new_graph(template='pressure_dependent', lname=f'new_plot_{filename}')
gl = graph[0]

# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:end)', type='l')  # crazy, l is L!; (?,1:end) means all

# group the plots and control plots setting in group
gl.group(True, 0, -1)


# adjust axisXY
gl.set_xlim(10, 1e5)
gl.set_ylim(1e15, 1e25)
gl.xscale = 'log10'
gl.yscale = 'log10'

# Save the opju to your UFF.
op.save(op.path('u') + f'new_plot_{filename}.opju')
print(f"new_plot_{filename}")

op.exit()
