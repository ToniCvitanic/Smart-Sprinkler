import SmartSprinklerModule as SSM
import math

# Initialize the position of the sprinkler to be at -90 degrees in pan, and -45 degrees in tilt
pan_angle = SSM.rotate_motor('pan', -1.3)
tilt_angle = SSM.rotate_motor('tilt', -1.1)

i = 1
while 1:
    image = SSM.capture_image(3,3,'image' + str(i))
    flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)
    if flame_present:
        print 'Flame detected!'
        target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        #if edge_crossing == 1:
            #ssm.rotate_motor('pan', 10 * math.pi / 180)
            #target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        #elif edge_crossing == 2:
            #ssm.rotate_motor('pan', -10 * math.pi / 180)
            #target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        #elif edge_crossing == 3:
            #ssm.rotate_motor('tilt', -10 * math.pi / 180)
            #target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        #elif edge_crossing == 4:
            #ssm.rotate_motor('tilt', 10 * math.pi / 180)
            #target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        #else:
            #target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        if target_centered:
            print 'target is centered'
        else:
            print 'Failed to center target'
            pan_angle = SSM.rotate_motor('pan', -1.3)
            tilt_angle = SSM.rotate_motor('tilt', -1.1)
    else:
        # If the camera has panned across the whole 180 degrees, return to the beginning angle and start over
        if pan_angle > math.pi / 2 - .09:
            pan_angle = SSM.rotate_motor('pan', -1.3)
        else:
            pan_angle = SSM.rotate_motor('pan', pan_angle + 10 * math.pi / 180)
    i = i+1
