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







# import experiment data
base_path = 'H:\postgraduate\data\converted_pAe_values_'
temperature_ranges = ['1200_to_1400', '1400_to_1600', '1600_to_1800', '1800_to_2000']

dfs = {}

for temp_str1 in temperature_ranges:
    file_path = f"{base_path}{temp_str1}_K.csv"
    dfs[temp_str1] = pd.read_csv(file_path)
    print(f"\nData for {temp_str1.replace('_', ' ')} K:")
    print(dfs[temp_str1].head())








# matlab data by scipy
mat_data = loadmat('H:\postgraduate\matlab\data_first_graph.mat')

# import data from matlab
op.new()
wks_1 = op.new_sheet('w', 'first dataset')

wks_1.from_list(0, mat_data['x_data'], units='Pa', lname='Pressure', axis='X')

###
label_matrix = [1300, 1500, 1700, 1900, 500]
mat_data_map = {'y_data1': mat_data['y_data'], 'y_data2': mat_data['y_data2'], 'y_data3': mat_data['y_data3'],
                'y_data4': mat_data['y_data4'], 'y_data5': mat_data['y_data5']}
#  dynamic dictionary
# mat_data_map = {f'y_data{i+1}': mat_data[f'y_data{i+1}'] for i in range(len(label_matrix))}
for i, label in enumerate(label_matrix):
    y_data_key = f'y_data{i + 1}'
    wks_1.from_list(i + 1, mat_data_map[y_data_key], units=' ', lname=f'{label} K', axis='Y')






# import experiment data

# input scatter point
wks_1.from_list(6, mat_data['firstgraph'][:, 1], units='Pa', lname='Pressure', axis='X')
wks_1.from_list(7, mat_data['firstgraph'][:, 2], units='  ', lname='gamma', axis='Y')
wks_1.from_list(8, mat_data['firstgraph'][:, 0], units='K', lname='temperature', axis='Y')


















# create plot
graph = op.new_graph(template='pressure_dependent')  # some problems could be happened if the template is unsuitable
gl = graph[0]

# adjust axisXY
gl.set_xlim(10, 1e5, 10)  # begin end step
gl.set_ylim(1e-5, 1e-1)
gl.xscale = 'log10'
gl.yscale = 'log10'

# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:6)', type='l')  # crazy, l is L!
scatter_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,7:8)', type='s')

# group the plots and control plots setting in group
gl.group(True, 0, i)
gl.group(True, i + 1, -1)



# Save the opju to your UFF.
op.save(op.path('u') + 'plot_first_graph.opju')
