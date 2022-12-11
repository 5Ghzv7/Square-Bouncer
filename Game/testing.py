#import pygame
import sys
sys.dont_write_bytecode = True
import os
block_detector_location = os.getcwd()+"\block_detector"
sys.path.insert(1, fr"{os.getcwd()}\block_detector")

import test
test.test()