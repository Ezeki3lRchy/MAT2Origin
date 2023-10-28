import pandas as pd
import originpro as op
import sys
from scipy.io import loadmat

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







# experiment data
base_path = 'H:\postgraduate\data\converted_pAe_values_'
temperature_ranges = ['1200_to_1400', '1400_to_1600', '1600_to_1800', '1800_to_2000']

dfs = {}

for temp_str1 in temperature_ranges:
    file_path = f"{base_path}{temp_str1}_K.csv"
    dfs[temp_str1] = pd.read_csv(file_path)
    print(f"\nData for {temp_str1.replace('_', ' ')} K")
    print(dfs[temp_str1].head())

# matlab data by scipy
mat_data = loadmat('H:/postgraduate/matlab/newdata_final_graph.mat')


op.new()  # create a new project

# import data
wks_1 = op.new_sheet('w', 'first dataset')  # create a new sheet
wks_1.from_list(0, mat_data['x_data'],   # import x_data
                units='Pa', lname='Pressure', axis='X')

params = mat_data['params']  # [1300, 1500, 1700, 1900] #  floating-point
#  Flatten params if it's not a 1D array
params = params.flatten()

gamma_data_struct = mat_data['gamma_data_struct']  # Note: two-dimension index

field_names = gamma_data_struct.dtype.names  # Get the names of the fields
unit = 'K'


#   loop input Y_data
for i, param in enumerate(params):  # the number of i is from 0
    param_float = float(param)
    param_value = int(param_float) if param_float.is_integer() else param_float
    y_data_key = f'{unit}{param_value}'
    # make sure it can show 1300 K , not 1300.0 K

    y_data = list(gamma_data_struct[0, 0][y_data_key][0])
    if y_data_key in field_names:
        wks_1.from_list(i + 1, y_data, units='', lname=f'{param_value}{unit} ', axis='Y')
    else:
        print(f"Key {y_data_key} not found in gamma_data_struct")






# input scatter point
index = 0
for j, temp_str2 in enumerate(temperature_ranges):
    print(f"Index: {j}, Value: {temp_str2}")
    dkey = i + 1 + 1  # 5
    xi = index + dkey
    yi = index + dkey + 1
    index += 2
    print(f"{xi}, {yi}")
    wks_1.from_list(xi, dfs[temp_str2].iloc[:, 1],
                    units='Pa', lname='Pressure', axis='X')
    wks_1.from_list(yi, dfs[temp_str2].iloc[:, 2],
                    units='  ', lname=f"{temp_str2.replace('_', ' ')} K:", axis='Y')


















# create plot
graph = op.new_graph(template='pressure_dependent')  # some problems could be happened if the template is unsuitable
gl = graph[0]

# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:{dkey})', type='l')  # crazy, l is L!
scatter_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,{dkey+1}:end)', type='s')

# group the plots and control plots setting in group
gl.group(True, 0, i)
gl.group(True, i + 1, -1)

# adjust axisXY
gl.set_xlim(100, 1e5)
gl.set_ylim(1e-5, 1e-1)
gl.xscale = 'log10'
gl.yscale = 'log10'

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_final_graph.opju')
