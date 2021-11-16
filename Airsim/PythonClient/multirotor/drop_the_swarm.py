#                                                 __      _
#  ___ __      __  __ _  _ __  _ __ ___    ___   / _|  __| | _ __   ___   _ __    ___  ___
# / __|\ \ /\ / / / _` || '__|| '_ ` _ \  / _ \ | |_  / _` || '__| / _ \ | '_ \  / _ \/ __|
# \__ \ \ V  V / | (_| || |   | | | | | || (_) ||  _|| (_| || |   | (_) || | | ||  __/\__ \
# |___/  \_/\_/   \__,_||_|   |_| |_| |_| \___/ |_|   \__,_||_|    \___/ |_| |_| \___||___/
#
#

import os
import sys
import cv2
import time
import airsim
import tempfile
import setup_path
import numpy as np
from datetime import datetime
from art import *

delay = 3
height = -0.5
speed = 2
vehicle_name = "Drone01"

def take_pictures():
    response = get_images()
    save_pictures(response)

def get_images():
    response = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis),
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False),
        airsim.ImageRequest(0, airsim.ImageType.Infrared),
        airsim.ImageRequest(1, airsim.ImageType.Segmentation, False, False),
        #success = client.simSetSegmentationObjectID("Ground", 20);
        ],vehicle_name=vehicle_name)
    print(vehicle_name, ' : Retrieved images: %d' % len(response))

    return response

def save_pictures(response_img):
    print('saving .  .   .')
    tmp_dir = 'C:\Swarm\images\persons'
    try:
        os.makedirs(tmp_dir)
    except OSError:
        if not os.path.isdir(tmp_dir):
            raise

    for idx, response in enumerate(response_img):
        filename = 'person_' + str(idx)
        path_file = os.path.join(tmp_dir, str(filename)) + str(datetime.timestamp(datetime.now()))

        # print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        # airsim.write_file(os.path.normpath(path_file + '.png'),response.image_data_uint8)
    
        if response.pixels_as_float:
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath(path_file + '.pfm'), airsim.get_pfm_array(response))
        elif response.compress: #png format
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(path_file + '.png'), response.image_data_uint8)
        else: #uncompressed array
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
            img_rgb = img1d.reshape(response.height, response.width, 3) #reshape array to 3 channel image array H X W X 3
            cv2.imwrite(os.path.normpath(path_file + '.png'), img_rgb) # write to png

tprint("swarm")
airsim.wait_key()
client = airsim.MultirotorClient()
client.confirmConnection()
print("1.- In the corner # 1")
client.enableApiControl(True,vehicle_name)
client.armDisarm(True,vehicle_name)
client.takeoffAsync().join()

client.rotateToYawAsync(225,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("2.- moving between corner 1 and 2")
client.moveToPositionAsync(-5, 0, height, speed).join()

client.rotateToYawAsync(270,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("3.- moving corner #2")
client.moveToPositionAsync(-10, 0, height, speed).join()

client.rotateToYawAsync(315,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("4.- moving between corner 2 and 3")
client.moveToPositionAsync(-10, -5, height, speed).join()

client.rotateToYawAsync(0,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("5.- moving corner #3")
client.moveToPositionAsync(-10, -10, height, speed).join()

client.rotateToYawAsync(45,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("6.- moving between corner 3 and  4")
client.moveToPositionAsync(-5, -10, height, speed).join()

client.rotateToYawAsync(90,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("7.- moving corner 4")
client.moveToPositionAsync(0, -10, height, speed).join()

client.rotateToYawAsync(135,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("8.- moving between corner 4 y 1")
client.moveToPositionAsync(0, -5, height, speed).join()

client.rotateToYawAsync(180,5,1).join()
take_pictures()
time.sleep(delay)
client.rotateToYawAsync(0,5,1).join()

client.takeoffAsync().join()
print("9.- moving home")
client.moveToPositionAsync(-3, -3, height, speed).join()

client.landAsync().join()
client.armDisarm(False)
client.enableApiControl(False)