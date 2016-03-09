import SmartSprinklerModule as SSM
import math

# Initialize the position of the sprinkler to be at -90 degrees in pan, and -45 degrees in tilt
pan_angle = SSM.rotate_motor('pan', -5)
tilt_angle = SSM.rotate_motor('tilt', -math.pi / 4)

while 1:
    image = SSM.capture_image()
    flame_present, x_centroid, y_centroid = SSM.find_centroid(image)
    if flame_present:
        print 'Flame detected!'
        target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)
        if target_centered:
            while flame_present:
                SSM.spray_water()
                image = SSM.capture_image()
                flame_present = SSM.find_centroid(image)
                # If initial spray did not extinguish the fire, spray upwards in increments until it has been
                # extinguished
                if flame_present:
                    tilt_angle = SSM.rotate_motor('tilt', tilt_angle + math.pi / 6)
                else:
                    tilt_angle = SSM.rotate_motor('tilt', -math.pi / 4)
        else:
            print 'Failed to center target. Need to adjust the gains in the center_target function.'
            exit()
    else:
        # If the camera has panned across the whole 180 degrees, return to the beginning angle and start over
        if pan_angle > math.pi / 2 - .09:
            pan_angle = SSM.rotate_motor('pan', -5)
        else:
            pan_angle = SSM.rotate_motor('pan', pan_angle + .1745)
