# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# MediaManager

#Interactive media manager for the IST/DEEC institucional screens

#Description:
#-Choice of the media source based on a state machine         
#-User interaction based on Kinect gesture recognition  
#-Possibility to check the cafeteria's menu            
# ----------------------------------------------------------------------------

import pyglet, sys

from MediaManager_config import *
from media_manager import MediaManager
from os.path import dirname, abspath
        
def main(argv): 
   
    SCRIPT_DIR=argv[0]
    
    #Screen
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screens = display.get_screens()

    #Initialize Media Manager
    media_manager=MediaManager(screens[0],SCRIPT_DIR)
    media_manager.run()

    #Pyglet run
    pyglet.app.run()

if __name__=='__main__':
    main(sys.argv[1:])  
        