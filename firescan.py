import SmartSprinklerModule as SSM
import math

# Initialize the position of the sprinkler to be at -90 degrees in pan, and -45 degrees in tilt
pan_angle = SSM.rotate_motor('pan', -1.3)
tilt_angle = SSM.rotate_motor('tilt', -1.5)
left_check = 0
right_check = 0
bottom_check = 0
top_check = 0

y_max = 480

tilt_ind = 0
tilt_scan_angles = [1.5, 1.5, 1, 1, .5, .5]

i = 1
while 1:
    image = SSM.capture_image(1,1,'image' + str(i))
    flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)
    if flame_present:
        print 'Flame detected!'
        for k in range(0, len(edge_crossing)):
            if edge_crossing[k] == 1:
                left_check = 1
            elif edge_crossing[k] == 2:
                right_check = 1
            elif edge_crossing[k] == 3:
                top_check = 1
            elif edge_crossing[k] == 4:
                bottom_check = 1
        y_offset = y_centroid - float(y_max) / 2.0
        if left_check == 1:
            pan_angle = SSM.rotate_motor('pan', pan_angle + (-3 if y_offset < 0 else 3) * math.pi / 180)
        elif right_check == 1:
            pan_angle = SSM.rotate_motor('pan', pan_angle + (3 if y_offset < 0 else -3) * math.pi / 180)
        if top_check == 1:
            tilt_angle = SSM.rotate_motor('tilt', tilt_angle - 3 * math.pi / 180)
        elif bottom_check == 1:
            tilt_angle = SSM.rotate_motor('tilt', tilt_angle + 3 * math.pi / 180)
        if left_check == 1 or right_check == 1 or bottom_check == 1 or top_check == 1:
            flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)

        target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)

        if target_centered:
            j = 1
            while flame_present:
                print 'Spraying water'
                SSM.spray_water()
                image = SSM.capture_image(1,1,'flameimage' + str(j))
                flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)
                 #If initial spray did not extinguish the fire, spray upwards in increments until it has been
                 #extinguished
                if flame_present:
                    y_offset = y_centroid - float(y_max) / 2.0
                    if y_offset > 0:
                        tilt_angle = SSM.rotate_motor('tilt', tilt_angle + 3 * math.pi / 180)
                    else:
                        tilt_angle = SSM.rotate_motor('tilt', tilt_angle - 3 * math.pi / 180)
                else:
                    if tilt_angle < 0:
                        tilt_angle = SSM.rotate_motor('tilt', -tilt_scan_angles[tilt_ind])
                    else:
                        tilt_angle = SSM.rotate_motor('tilt', tilt_scan_angles[tilt_ind])
                j = j+1
        else:
            print 'Failed to center target. Need to adjust the gains in the center_target function.'
            if tilt_angle < 0:
                tilt_angle = SSM.rotate_motor('tilt', -tilt_scan_angles[tilt_ind])
            else:
                tilt_angle = SSM.rotate_motor('tilt', tilt_scan_angles[tilt_ind])
    else:
        left_check = 0
        right_check = 0
        bottom_check = 0
        top_check = 0

        # If the camera has panned across the whole 180 degrees, return to the beginning angle and start over from the
        # other side
        if pan_angle > math.pi / 2 - .09:
            if tilt_angle < 0:
                tilt_angle = SSM.rotate_motor('tilt', tilt_scan_angles[tilt_ind])
            else:
                tilt_angle = SSM.rotate_motor('tilt', -tilt_scan_angles[tilt_ind])
            pan_angle = SSM.rotate_motor('pan', -1.3)
            if tilt_ind < 5:
                tilt_ind += 1
            else:
                tilt_ind = 0
        else:
            pan_angle = SSM.rotate_motor('pan', pan_angle + 10 * math.pi / 180)
    i += 1
