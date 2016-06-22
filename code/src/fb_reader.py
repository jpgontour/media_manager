# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# fb_reader function
# ----------------------------------------------------------------------------

#Filename management
from os.path import dirname, abspath,join

#Python modules
import feedparser, os
from selenium import webdriver
from PIL import Image


def fb_reader(file_path_raw, fileout_path, feed_link):
    """
    Prints the screen on the latest FB note. 
    """
    
    try:
        driver = webdriver.PhantomJS(service_log_path='src/ghostdriver.log')
        driver.implicitly_wait(10)
        driver.maximize_window()

        driver.get(feed_link)
        
        driver.find_element_by_id("js_1").click()
        
        content = driver.find_element_by_class_name("_1dwg")
        
        location = content.location
        size = content.size

        img = driver.get_screenshot_as_png()
        
        path=join(file_path_raw,'fbdeec.png')
        driver.save_screenshot(path) # saves screenshot of entire page

        img = Image.open(path) # uses PIL library to open image in memory

        left = int(location['x'])
        top = int(location['y'])
        right = min(int(location['x'] + size['width']),img.size[0])
        bottom = min(int(location['y'])+size['height'],img.size[1])

        img = img.crop((left, top, right, bottom)) # defines crop points
        path=join(fileout_path,'fbdeec_file.png')
        
        img.save(path) # saves new cropped image
        
        driver.quit()
        return True
    except:
        try:
            driver.quit()
        except:
            pass
        return False
    
    
    
