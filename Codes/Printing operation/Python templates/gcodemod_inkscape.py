import numpy as np

def read(filepath, offset):
    """
    Read a Gcode file into Python array
    
    Input:
        filepath: path to Gcode file
        offset: (X0, Y0, Z0) offset the centre point
        
    Return:
        An array in format of [(x1, y1, z1, e1), (x2, y2, z2, e2), ...]
    """
    X0, Y0, Z0 = offset
    
    raw = []  # raw file, read directly from file
    xyzraw = []  # raw format with lines contains either X, Y or Z
    output = []  

    with open(filepath) as inputfile:
        for line in inputfile:
            raw.append(line.strip().split(' '))

    # Remove lines that don't start with 'G01'
    g1raw = [r for r in raw if 'G01' == r[0] or 'G02' == r[0] or 'G03'== r[0]]
    
    # Remove lines without 'X','Y', or 'Z'
    for r in g1raw:
        isappend = False
        for item in r:
            if 'X' in item or 'Y' in item or 'Z' in item:
                isappend = True
        if isappend:
            xyzraw.append(r)

    z = None
    for r in xyzraw:
        if r[1][0] == 'Z':
            try:
                #z = float(r[1][1:])  # expecting 'Z123.456'
                z = 0.5 #Starting layer position user default
            except:
                raise RuntimeError('Unexpected format: cannot convert line' \
                        + ' %s with %s to float' % (raw.index(r), r[1][1:]))
        
        elif (r[1][0] == 'X') and (r[2][0] == 'Y'):
            if z is None:
                raise RuntimeError('Unexpected format: z position is not' \
                        + ' declared before x, y')
                
            try:
                x = float(r[1] [1:])  # expecting 'X123.456'
                y = float(r[2] [1:])  # expecting 'Y123.456'
            except:
                raise RuntimeError('Unexpected format: cannot convert line' \
                        + ' %s with %s and/or %s to float' % (raw.index(r), \
                        r[1][1:], r[2][1:]))
            
            o = [x, y, z]
            
            e = 0
            for item in r:
                if 'I' in item:
                    e = 1
            output.append(o + [e])

        else:
            raise RuntimeError('Unexpected format: line %s' % raw.index(r) \
                    + ' does not contain (X, Y) or Z coordinates')

    output = np.asarray(output, dtype='float64')
    output[:, 0] = np.around(output[:, 0] + X0 - np.mean(output[:, 0]),
                             decimals=1)
    output[:, 1] = np.around(output[:, 1] + Y0 - np.mean(output[:, 1]),
                             decimals=1)
    output[:, 2] = np.around(Z0 - output[:, 2], decimals=1)
    return output


if __name__ == '__main__':
    p = "/home/ieklei/Documents/uArmPython/examples/api/single/v3-printer/gcode-transform/hand.txt"
    bigCoor = read(p , (0, 0, 70))
    x_gcode = bigCoor[:, 0]
    y_gcode = bigCoor[:, 1]
    z_gcode = bigCoor[:, 2]
    e_gcode = bigCoor[:, 3]
   
    # Also try transform!
    import transform
    a_gcode = 282.5  # mm
    b_gcode = 1.5 # mm
    xyarm_gcode = transform.coordinateTransfer(x_gcode, y_gcode, a_gcode, b_gcode).T
    zarm_gcode = np.copy(z_gcode)
    
    print('Gcode coordinates: ')
    for i in range(xyarm_gcode.shape[0]):
        print(np.append(xyarm_gcode[i], zarm_gcode[i]))
    print('')
    