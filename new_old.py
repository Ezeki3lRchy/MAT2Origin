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
mat_data = loadmat('H:\postgraduate\matlab\data_invT_new_old.mat')

# import data
op.new()

wks_1 = op.new_sheet('w', 'first dataset')
wks_1.from_list(0, mat_data['x_data'], units='K', lname='1000/T', axis='X')
wks_1.from_list(1, mat_data['y_data'], lname='new')
wks_1.from_list(2, mat_data['y_data2'], units=' ', lname='old')


wks_1.from_list(3, mat_data['gamma_Scott_1983'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(4, mat_data['gamma_Scott_1983'][:, 1], units=' ', lname='Scott')

wks_1.from_list(5, mat_data['gamma_Stewart_1996'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(6, mat_data['gamma_Stewart_1996'][:, 1], units=' ', lname='Stewart')

wks_1.from_list(7, mat_data['gamma_greaves_1959'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(8, mat_data['gamma_greaves_1959'][:, 1], units=' ', lname='Greaves')

wks_1.from_list(9, mat_data['gamma_kolodziej_1987'][:, 0], units=' ', lname='', axis='X')
wks_1.from_list(10, mat_data['gamma_kolodziej_1987'][:, 1], units=' ', lname='Kolodziej')


# create plot
graph = op.new_graph(template='gamma_invT')
gl = graph[0]

# semi-logy
gl.xscale = 1
gl.yscale = 2

# other way, axis limit
gl.xlim = (0.3, 2.7)
gl.ylim = (1e-5, 1e-1, 5)

# plot whole sheet as XY plot
line_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:3)', type='l')  # crazy, l is L!

scatter_plot = gl.add_plot(f'{wks_1.lt_range()}!(?,4:end)', type='s')

# group the plots and control plots setting in group
gl.group(True, 0, 1)
gl.group(True, 2, -1)


# Now, get the list of all plots in the graph layer
plots = gl.plot_list()


line_plot.colormap = 'Candy'
line_plot.shapelist = [3, 2, 1]

scatter_plot.colormap = 'Candy'
scatter_plot.shapelist = [3, 2, 1]





# \f:Times New Roman(\p127( ? )) from JH
# axis title
ax = gl.axis('x')
ax.title = ' \ f:Times New Roman(\p127(%(1@W,1,L)[%(1@W,1,U)]))'  # can't be \f, I have tested.
ay = gl.axis('y')
ay.title = '\ f:Times New Roman(\p127(   \g(g)  ))'

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_invT_new_old.opju')