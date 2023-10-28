import originpro as op
import sys
from scipy.io import loadmat
import math


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
filename = 'gamma_T_dif_D_Diff'
mat_data = loadmat(f"H:/postgraduate/matlab/newdata_{filename}.mat")




op.new()  # create a new project

# import data
wks_1 = op.new_sheet('w', f'{filename}')  # create a new sheet
wks_1.from_list(0, mat_data['x_data'],   # import x_data
                units='K', lname='Temperature', axis='X')

params = mat_data['params']  # [1300, 1500, 1700, 1900] #  floating-point # 2-D matrix
#  Flatten params if it's not a 1D array
params = params.flatten()

gamma_data_struct = mat_data['gamma_data_struct']  # Note: two-dimension index

field_names = gamma_data_struct.dtype.names  # Get the names of the fields
front_label = 'Diff'


#   loop input Y_data
for i, param in enumerate(params):  # the number of i is from 0
    param_float = float(param)
    param_value = int(param_float) if param_float.is_integer() else param_float
    print(param_value)
    y_data_key = f'{front_label}{param_value}'
    # make sure it can show 1300 K , not 1300.0 K

    y_data = list(gamma_data_struct[0, 0][y_data_key][0])
    if y_data_key in field_names:
        exponent_number = math.floor(math.log10(param_value))
        mantissa = int(param_value / 10 ** exponent_number)
        longname_front = f'\i(D\-({front_label})=)'
        longname_exponent_term = f'10\+({exponent_number})'
        longname_unit = 'J/mol'
        wks_1.from_list(i + 1, y_data, units='',
                        lname=f'{longname_front} {mantissa}\g(´){longname_exponent_term}{longname_unit}', axis='Y')
    else:
        print(f"Key {y_data_key} not found in gamma_data_struct")





# create plot  # some problems could be happened if the template is unsuitable
graph = op.new_graph(template='gamma_T', lname=f'new_plot_{filename}')
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
op.save(op.path('u') + f'new_plot_{filename}.opju')
print(f"new_plot_{filename}")

op.exit()
