import numpy as np

class MyAngle():
    def __init__(self,theta_val,phi_val):
        self.theta = theta_val
        self.phi = phi_val
class MyCentroid():
    def __init__(self,x_val,y_val):
        self.x = x_val
        self.y = y_val
class MyMove():
    def __init__(self,theta_val,theta_sign_val,phi_val,phi_sign_val):
        self.theta = theta_val
        self.theta_sign = theta_sign_val
        self.phi = phi_val
        self.phi_sign = phi_sign_val

# Function to calculate the range of the camera from the flame based on the centroid location and camera angles
def range_finder(angle,centroid,i_angle=20):    # Initial default move angle of 20 degrees

    move = find_direction(angle,centroid,i_angle)

    def iter_move_angle(move,counter=0):
        counter += 1
        move_motor('theta',move.theta,move.theta_sign)
        move_motor('phi',move.phi,move.phi_sign)
        FLAME,centroid = get_centroid()
        test_angle = get_angle()

        if(FLAME!=1 & counter>=10):
            print 'Well, crap.'
            # Lost Flame for 10 iterations! Restart scan
        elif(FLAME!=1):
            # Temporarily lost flame. Lower move magnitude and try to refind it
            move.theta = move.theta/2
            move.phi = move.phi/2
            if(counter == 1):
                # If this is our second iteration, change directions.
                move.theta_sign = move.theta_sign*-1
                move.phi_sign = move.phi_sign*-1
                return iter_move_angle(move,counter)
            elif(counter > 1):
                # If this is not our first or second iteration, maintain direction
                return iter_move_angle(move,counter)
        elif(FLAME==1):
            # If the flame is detected return our new centroid and angle
            return angle,centroid

    angle2,centroid2 = iter_move_angle(move,0)

    return angle2,centroid2
    



# Function to calculate which direction to move in based on centroid location and camera angles
def find_direction(angle,centroid,i_angle):
    return MyMove(10,1,5,-1)
def get_centroid():
    return(1,MyCentroid(50,50))
def move_motor(blah, blah2, blah3):
    return()
def get_angle():
    return MyAngle(75,115)
        
