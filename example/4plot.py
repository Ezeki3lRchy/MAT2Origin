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

# open file
# src_opju = op.path('u') + r'plot_pressure_dependent.opju'  # u = user , e = install
# op.open(file=src_opju, readonly=False)

# get data
mat_data = loadmat('H:\postgraduate\matlab\data_pressure_dependent_ref.mat')

# import data
op.new()
wks_1 = op.new_sheet('w', 'first dataset')
wks_1.from_list(0, mat_data['x_data'], units='Pa', lname='Pressure', axis='X')
wks_1.from_list(1, mat_data['y_data'], units=' ', lname='500 K')  # \g(?)
wks_1.from_list(2, mat_data['y_data2'], units=' ', lname='1700 K')
wks_1.from_list(3, mat_data['y_data3'], units=' ', lname='1179 K')

# Save the opju to your UFF.
# op.save(op.path('u')+ 'Ext Python Example 1.opju')

# find sheet
#  wks_1 = find_sheet

# create plot
graph = op.new_graph(template='gamma_invT')  # some problems could be happened about the template
gl = graph[0]

# plot whole sheet as XY plot
plot = gl.add_plot(f'{wks_1.lt_range()}!(?,1:end)')  # it's good

# group the plots and control plots setting in group
gl.group()
plot.colormap = 'Candy'
plot.shapelist = [3, 2, 1]
gl.rescale()

# loglog
gl.xscale = 'log10'
gl.yscale = 'log10'

# gl.rescale()

# Sets axis scale begin(From), end(To) and step(Increment)
gl.set_xlim(1e1, 1e5)
gl.set_ylim(1e-4, 1)
gl.rescale()  # update limits to show all the data, including color scale range is colormap is used

# other way, axis limit
gl.xlim = (1e1, 1e5)
gl.ylim = (1e-4, 1)

# \f:Times New Roman(\p127( ? )) from JH
# axis title
ax = gl.axis('x')
ax.title = ' \ f:Times New Roman(\p127(%(1@W,1,L)[%(1@W,1,U)]))'  # can't be \f, I have tested.
ay = gl.axis('y')
ay.title = '\ f:Times New Roman(\p127(   \g(g\-(OO))  ))'

# Save the opju to your UFF.
op.save(op.path('u') + 'plot_pressure_dependent_ref.opju')

op.exit()
