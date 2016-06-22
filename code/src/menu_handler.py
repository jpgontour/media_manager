# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# menu_handler function
# ----------------------------------------------------------------------------

#Filename managemen
from os.path import join

#Python modules
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#Configuration File
from MediaManager_config import *


def menu_handler(menu,fileout_path):
    """
    Generates background and labels for the Cafeteria Menu 
    
    """
    
    image = Image.open("icons/menu_template.jpg")
    draw  =  ImageDraw.Draw (image)
    
    if menu is None:  
    
        TITLE_X_OFFSET=0.05*image.size[0]
        TITLE_Y_OFFSET=0.25*image.size[1]
        
        huge_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*HUGE_FONT/1000)) 

        draw.text ( (TITLE_X_OFFSET,TITLE_Y_OFFSET), u'Ementa não disponível', fill=BLACK,font=huge_font)
        
    else:

        TITLE_X_OFFSET=0.05*image.size[0]
        MEAL_X_OFFSET=0.07*image.size[0]
        MENU_X_OFFSET=0.10*image.size[0]
        DISH_X_OFFSET=0.15*image.size[0]

        TITLE_Y_OFFSET=0.12*image.size[1]
        MEAL_Y_OFFSET=0.10*image.size[1]
        MENU_Y_OFFSET=0.08*image.size[1]
        DISH_Y_OFFSET=0.06*image.size[1]
        
        
        large_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
        medium_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
        small_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

        large_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
        medium_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
        small_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

        y_offset=0
        
        y_offset+=TITLE_Y_OFFSET
        draw.text ( (TITLE_X_OFFSET,y_offset), u'Ementa', fill=BLACK,font=large_font)
        
        if menu.has_key(u'Almoço'):
            y_offset+=MEAL_Y_OFFSET
            draw.text ( (MEAL_X_OFFSET,y_offset), u'Almoço', fill=BLACK,font=medium_font_bold)
            

            if menu[u'Almoço'].has_key(u'Menú Tradicional'):  
                y_offset+=MENU_Y_OFFSET 
                draw.text ( (MENU_X_OFFSET,y_offset), u'- Menú Tradicional', fill= BLACK,font=small_font)                                                       
                
                for elem in menu[u'Almoço'][u'Menú Tradicional']:
                    y_offset+=DISH_Y_OFFSET
                    draw.text ( (DISH_X_OFFSET,y_offset), u'\u2022 ' + elem, fill= BLACK,font=small_font)                           
                    
                
            if menu[u'Almoço'].has_key(u'Menú Macrobiótica'):  
                y_offset+=MENU_Y_OFFSET  
                draw.text ( (MENU_X_OFFSET,y_offset), u'- Menú Macrobiótica', fill= BLACK,font=small_font)                                                                 
                
                for elem in menu[u'Almoço'][u'Menú Macrobiótica']:
                    y_offset+=DISH_Y_OFFSET
                    draw.text ( (DISH_X_OFFSET,y_offset), u'\u2022 ' + elem, fill= BLACK,font=small_font)                                                           
                    
        if menu.has_key(u'Jantar'): 
            y_offset+=MEAL_Y_OFFSET
            draw.text ( (MEAL_X_OFFSET,y_offset), 'Jantar', fill= BLACK,font=medium_font_bold) 
            
            if menu[u'Jantar'].has_key(u'Menú Tradicional'): 
                y_offset+=MENU_Y_OFFSET 
                draw.text ( (MENU_X_OFFSET,y_offset), u'- Menú Tradicional', fill= BLACK,font=small_font)   
                
                for elem in menu[u'Jantar'][u'Menú Tradicional']:
                    y_offset+=DISH_Y_OFFSET
                    draw.text ( (DISH_X_OFFSET,y_offset), u'\u2022 ' + elem, fill= BLACK,font=small_font)                                                                
                    
                    
    image.save(join(fileout_path,'menu_file.jpg')) 
