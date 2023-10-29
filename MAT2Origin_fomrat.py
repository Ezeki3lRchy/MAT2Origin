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

# open GUI
if op.oext:
    op.set_show(True)

# environment variable
filename = 'gammaEROOfraction_T_dif_v0_Diff'
mat_data = loadmat(f"H:/postgraduate/matlab/newdata_{filename}.mat")



# create a new project
op.new()
wks_1 = op.new_sheet('w', f'{filename}')  # create a new sheet
# or we also can find a worksheet:
# wks_1 = op.find_sheet('w', f'{filename}')  # find a worksheet

wks_1.from_list(0, mat_data['x_data'],   # import x_data
                units='K', lname='Temperature', axis='X')

# input Y_data
params = mat_data['params']  # [1300, 1500, 1700, 1900] #  floating-point # 2-D matrix
#       Flatten params if it's not a 1D array
params = params.flatten()
gamma_data_struct = mat_data['gamma_data_struct']  # Note: two-dimension index
field_names = gamma_data_struct.dtype.names  # Get the names of the fields

#       extract_char
extracted_string = field_names[0]
match = re.match(r'[a-zA-Z]+', extracted_string)
prefix = ''
if match:
    prefix = match.group(0)
    print(prefix)
#       add Y_data
front_label = prefix
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
        longname_front = f'\i(v\-(0,{front_label}) =)'
        longname_exponent_term = f'10\+({exponent_number})'
        longname_unit = "s\+(-1)"
        longname_number = f'{mantissa}\g(´){longname_exponent_term}'  # eg:10^3
        # if  just need T = 1300 K, we can:
        # longname_number = f'{para_value}'
        wks_1.from_list(i + 1, y_data, units='',
                        lname=f'{longname_front} {longname_number} {longname_unit}', axis='Y')
        print(f'{longname_front} {longname_number} {longname_unit}')
    else:
        print(f"Key {y_data_key} not found in gamma_data_struct")

# create plot
# some problems could be happened if the template is unsuitable
graph = op.new_graph(template='gamma_T', lname=f'new_plot_{filename}')
gl = graph[0]  # set graphic layer, index is from 0

# plot sheet as XY plot
# NOTE: l's capital is L!; (?,1:end) means all
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:end)', type='l')

# group the plots and control plots setting in group, -1 =all
gl.group(True, 0, -1)

# adjust axis X and Y
gl.set_xlim(10, 1e5)
gl.set_ylim(1e-4, 1e-1)

gl.xscale = 'log10'
gl.yscale = 'log10'

# axis title
ax = gl.axis('x')
ax.title = ' \ f:Times New Roman(\p127(%(1@W,1,L)[%(1@W,1,U)]))'  # \f is prohibited
ay = gl.axis('y')
ay.title = '\ f:Times New Roman(\p127(   \g(g)  ))'

# Save the opju to your UFF.
op.save(op.path('u') + f'new_plot_{filename}.opju')
print(f"new_plot_{filename}")

# exit
op.exit()
