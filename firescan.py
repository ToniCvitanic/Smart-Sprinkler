import SmartSprinklerModule as SSM
import math
import os
import RPi.GPIO as GPIO
import sys
import time

# This script is the main script to run the Smart Sprinkler. It continuously scans for, targets, and squirts water at
# fires as long as the device is turned on

# Setup the shutdown pin switch to be high with the internal pullup resistor
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(19, GPIO.FALLING, callback = SSM.shutdown, bouncetime = 2000)

# Initialize the position of the sprinkler position
pan_angle = SSM.rotate_motor('pan', -1.3)
tilt_angle = SSM.rotate_motor('tilt', -1.5)
left_check = 0
right_check = 0
bottom_check = 0
top_check = 0

# Define the height of the image (used later)
y_max = 480

# Define the different tilt angles to run through. They are repeated because of the way the code is written in
# incrementing them.
tilt_ind = 0
tilt_scan_angles = [1.5, 1.5, 1, 1, .5, .5]

i = 1
while 1:
	try:
		# Capture an image

		#image = SSM.capture_image(1,1,'image' + str(i))
		image = SSM.capture_image()
		# Check for a flame, and find its centroid in the image
		flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)
		if flame_present:
			print 'Flame detected!'
			# Check if the flame centroid touches any edges of the image
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
			# Move to get centroid of the flame away from the edges of the image
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

			# Bring the centroid of the fire to the center of the image
			target_centered = SSM.center_target(pan_angle, tilt_angle, x_centroid, y_centroid)

			if target_centered:
				j = 1
				# Spray water until the flame is no longer present
				while flame_present:
					print 'Spraying water'
					SSM.spray_water(tilt_angle)
					image = SSM.capture_image()
					#image = SSM.capture_image(1,1,'flameimage' + str(j))
					flame_present, x_centroid, y_centroid, edge_crossing = SSM.find_centroid(image)
					# If initial spray did not extinguish the fire, spray at slightly different tilts until it is
					# extinguished
					if not flame_present:
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
				if tilt_ind < 5:
					tilt_ind += 1
				else:
					tilt_ind = 0
					
				if tilt_angle < 0:
					tilt_angle = SSM.rotate_motor('tilt', tilt_scan_angles[tilt_ind])
				else:
					tilt_angle = SSM.rotate_motor('tilt', -tilt_scan_angles[tilt_ind])
				pan_angle = SSM.rotate_motor('pan', -1.3)

			else:
				pan_angle = SSM.rotate_motor('pan', pan_angle + 10 * math.pi / 180)
		i += 1
	except:
                sysinfo = sys.exc_info()
		print "Unexpected error:",sysinfo[1]
		with open("Error_Log.txt", "a") as text_file:
			text_file.write("\n Error: {0}".format(sys.exc_info()[0]))
			text_file.write("\n Error: {0}".format(sys.exc_info()[1]))
			text_file.write("\n Error: {0}".format(sys.exc_info()[2]))
		break
while 1:
        time.sleep(1)


		


