import os
import ansys.fluent.core as pyfluent

os.chdir('E:\ICEM\Validation4mesh_independence')

solver_session = pyfluent.launch_fluent(show_gui=True,
                                        mode='solver',
                                        precision='double',
                                        processor_count=1,
                                        version="2d")

solver_session.file.read_case_data(file_name=
                                   "0710_23_testgeometryV3.3_shock250_48mm_normal_80_standard.cas.h5")

solver_session.tui.display.objects.create(
    "xy-plot",#Object types: (contour mesh particle-tracks pathlines vector xy-plot scene volume)
    "plot-1", #new object name
    # Choose setting to change[help-mode]>
    # axes                    options                 x-axis-function
    # curves                  plot-direction          y-axis-function
    # name                    surfaces-list
    "options",
    "node-values",
    "yes",
    "position-on-x-axis",
    "#t",
    "q",

    "y-axis-function",
    "heat-flux",
    "x-axis-function",
    '"Curve Length"',  #very improtant
    "surface-list",
    "fsi",
    "()",
    "q",
)
solver_session.tui.display.objects.display("plot-1")

































































































































































