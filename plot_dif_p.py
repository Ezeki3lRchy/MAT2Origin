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
mat_data = loadmat('H:\postgraduate\matlab\data_dif_p.mat')

# set worksheet variable
op.new()
wks_1 = op.new_sheet('w', 'first dataset')

# import data
wks_1.from_list(0, mat_data['x_data'], units='K', lname='1000/T', axis='X')
wks_1.from_list(1, mat_data['y_data_p10'], units='', lname=' 10Pa')
wks_1.from_list(2, mat_data['y_data_p100'], units='', lname=' 100Pa')
wks_1.from_list(3, mat_data['y_data_p500'], units='', lname=' 500Pa')
wks_1.from_list(4, mat_data['y_data_p1000'], units='', lname=' 1000Pa')
wks_1.from_list(5, mat_data['y_data_p2000'], units='', lname=' 2000Pa')
wks_1.from_list(6, mat_data['y_data_p3500'], units='', lname=' 3500Pa')

# create plot
graph = op.new_graph(template='gamma_invT')
gl = graph[0]


# plot sheet as XY plot and scatter
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:end)', type='l')  # crazy, l is L!

#  group the plots and control plots setting in group
gl.group()


# other way, axis limit
gl.xlim = (0.3, 1, 8)
gl.ylim = (1e-5, 1e-1)

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_dif_p.opju')

op.exit()