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

# get data
mat_data = loadmat('H:\postgraduate\matlab\data_parameterization_Pa_calibration.mat')

# import data
op.new()

wks_1 = op.new_sheet('w', 'first dataset')
wks_1.from_list(0, mat_data['x_data'], units='K', lname='1000/T', axis='X')
wks_1.from_list(1, mat_data['y_data'], units='Pa', lname=' 50 ')
wks_1.from_list(2, mat_data['y_data2'], units='Pa', lname='500')
wks_1.from_list(3, mat_data['y_data3'], units='Pa', lname='3000')

i = 4
wks_1.from_list(i, mat_data['gamma_Scott_1983'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(i + 1, mat_data['gamma_Scott_1983'][:, 1], units=' ', lname='Scott')

wks_1.from_list(i + 2, mat_data['gamma_Stewart_1996'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(i + 3, mat_data['gamma_Stewart_1996'][:, 1], units=' ', lname='Stewart')

wks_1.from_list(i + 4, mat_data['gamma_greaves_1959'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(i + 5, mat_data['gamma_greaves_1959'][:, 1], units=' ', lname='Greaves')

wks_1.from_list(i + 6, mat_data['gamma_kolodziej_1987'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(i + 7, mat_data['gamma_kolodziej_1987'][:, 1], units=' ', lname='Kolodziej')

# create plot
graph = op.new_graph(template='gamma_invT')
gl = graph[0]

# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:4)', type='l')  # crazy, l is L!
scatter_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,5:end)', type='s')

# group the plots and control plots setting in group
gl.group(True, 0, 2)
gl.group(True, 3, -1)

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_parameterization_Pa_calibration.opju')
