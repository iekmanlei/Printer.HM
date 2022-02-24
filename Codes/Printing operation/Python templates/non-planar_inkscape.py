# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:17:36 2021

@author: Iek Man Lei
"""

import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
# Import my modules
import transform_rot as transform
import gcodemod
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import gcodemod_inkscape as gcodemod_inkscape
get_ipython().run_line_magic('matplotlib', 'qt5')

def map_plane(x_print, y_print, x_plane, y_plane, z_plane, Z0):
    eps = 0.2
    output = []
    for x, y in zip(x_print, y_print):
        out = []
        has_value = False
        for i, (x_base, y_base, z_base) in enumerate(zip(x_gcode, y_gcode, z_gcode)):
            
            if x_base - eps <= x <= x_base + eps:
                if y_base - eps <= y <= y_base + eps:
                    out.append([x, y, z_base])
                    has_value = True

        if has_value == True:
            z = [w[2] for w in out]
            min_index = z.index(np.nanmin(z))
            output.append(out[min_index])
    
        else: 
            output.append([x,y,Z0])
    return output

plt.close('all')

# User-defined input
Z0 = 67
offset = [0, 0, Z0]
# Import G-code of the target object
bigCoor = gcodemod.read('nose-0_5e-0_5s-100HC_noshell.txt', offset) 
# Import gcode of the pattern generated via Inkscape
bigCoor_i = gcodemod_inkscape.read('pattern_on_nose_0002.txt', offset) 


# Operation
x_gcode = bigCoor[:, 0] # Import x coord from gcode file
y_gcode = bigCoor[:, 1] # Import y coord from gcode file
z_gcode = [i + 2.5 for i in bigCoor[:, 2]] # Import z coord from gcode file
e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 

x_gcode_i = bigCoor_i[:, 0] # Import x coord from gcode file
y_gcode_i = bigCoor_i[:, 1] # Import y coord from gcode file
z_gcode_i = bigCoor_i[:, 2] # Import z coord from gcode file
e_gcode_i = bigCoor_i[:, 3] # Import extrusion information from gcode file 
output = map_plane(x_gcode_i, y_gcode_i, x_gcode, y_gcode, z_gcode, Z0)


# Plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(x_gcode[::5], y_gcode[::5], z_gcode[::5], alpha=0.1)

x = [w[0] for w in output]
y = [w[1] for w in output]
z = [w[2] for w in output]
ax.scatter(x, y, z, color='r')
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.view_init(azim=0, elev=270)

plt.show()

