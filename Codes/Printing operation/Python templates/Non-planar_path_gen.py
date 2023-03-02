'''
Non-planar path printing program to project a pattern according to the z-plane 
of the target object.

Inputs (see line 20): G-codes of the plane object (created on Slic3R) and a 
2D pattern (created on Inkscape), offset coordinates and starting z position.

Output: A text file of the projected coordinates of the pattern that can be
imported to test_picture.py for printing operation.
'''

import gcodemod
import gcodemod_inkscape 
import transform_rot as transform
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D


# User-defined input
Z0 = 67 # starting z position
offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
# Import G-code of the target plane
plane_coor = gcodemod.read(r"C:\Users\Biointerface\Documents\uArmPython\examples\Iek\nose-0_1s-0_1e-100HC.txt", offset) 
# Import gcode of the pattern generated via Inkscape
inkscape_coor = gcodemod_inkscape.read(r"C:\Users\Biointerface\Documents\uArmPython\examples\Iek\pattern_on_nose_0002.txt", offset) 


# Operation
x_gcode = plane_coor[:, 0] # Import x coord from gcode file
y_gcode = plane_coor[:, 1] # Import y coord from gcode file
z_gcode = [i + 2.5 for i in plane_coor[:, 2]] # Import z coord from gcode file
e_gcode = plane_coor[:, 3]  # Import extrusion information from gcode file 

x_gcode_i = inkscape_coor[:, 0] # Import x coord from gcode file
y_gcode_i = inkscape_coor[:, 1] # Import y coord from gcode file
z_gcode_i = inkscape_coor[:, 2] # Import z coord from gcode file
e_gcode_i = inkscape_coor[:, 3] # Import extrusion information from gcode file


out = transform.map_plane(x_gcode_i, y_gcode_i, e_gcode_i, x_gcode, y_gcode, z_gcode, Z0)
out_x = [w[0] for w in out]
out_y = [w[1] for w in out]
out_z = [w[2] for w in out]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x_gcode[::5], y_gcode[::5], z_gcode[::5], alpha=0.1)
ax.scatter(out_x, out_y, out_z, color='r')
fig.show()
# Output a text file that can be imported to text_picture.py for printing
np.savetxt('nose_pattern.txt', out) 