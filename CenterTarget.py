import math


def center_target(r, x, y, h_fov, v_fov):
    # r refers to the distance from the camera to the fire
    # x and y refer to the image coordinates of the fire centroid
    # x_max and y_max refer to the dimensions of the image
    # h_fov and v_fov are the horizontal and vertical fields of view of the camera

    # This function assumes that the image origin is at the top left of the image
    # and that x increases going down, and y increases going to the right

    x_max  = 640
    y_max = 480

    x_offset = float(x_max) / 2.0 - x
    y_offset = float(y_max) / 2.0 - y

    x_offset = x_offset * 2 * r * math.tan(v_fov / 2) / x_max
    y_offset = y_offset * 2 * r * math.tan(h_fov / 2) / y_max

    x_rotate = math.asin(x_offset / r)
    y_rotate = math.asin(y_offset / r)

    print "x_rotate = %f" % x_rotate
    print "y_rotate = %f" % y_rotate

    test = math.asin(.5)
    print "test = %f" % test

    return x_rotate, y_rotate
