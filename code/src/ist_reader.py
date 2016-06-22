# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Set of functions to draw ist news and events slides
# ----------------------------------------------------------------------------

#Filename management
from os.path import join

#Python modules
import feedparser,re,textwrap
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#Configuration File
from MediaManager_config import *



def ist_events_handler(entry,fileout_path):
    """
    Draws the events slide
    """
    
    image = Image.open("icons/ist_frame.jpg")
    draw  =  ImageDraw.Draw (image)

    CLASS_X_OFFSET=0.30*image.size[0]
    TITLE_X_OFFSET=0.30*image.size[0]
    DESCRIPTION_X_OFFSET=0.30*image.size[0]

    CLASS_Y_OFFSET=0.25*image.size[1]
    TITLE_Y_OFFSET=0.10*image.size[1]
    DESCRIPTION_Y_OFFSET=0.08*image.size[1]
    LINE_Y_OFFSET= 0.05*image.size[1]
    
    large_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
    medium_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
    small_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

    large_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
    medium_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
    small_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

    y_offset=0
            
    y_offset+=CLASS_Y_OFFSET
    draw.text ( (CLASS_X_OFFSET,y_offset), u'Eventos', fill= CYAN,font=large_font)
    
    y_offset+=TITLE_Y_OFFSET
    lines=textwrap.wrap(entry['title'], width=45)
    for line in lines:
        y_offset+=LINE_Y_OFFSET
        draw.text ( (TITLE_X_OFFSET,y_offset), line, fill= BLACK,font=medium_font_bold)

        
    pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    description=entry['description']
    description_list=pat.findall(description[0:min(400,len(description))])
    description=''
    
    for n in range(0,len(description_list)):
        description=description + ' ' + description_list[n]
        
    y_offset+=DESCRIPTION_Y_OFFSET    
    lines=textwrap.wrap(description, width=55)   
    for line in lines:    
        y_offset+=LINE_Y_OFFSET
        draw.text ( (DESCRIPTION_X_OFFSET,y_offset), line, fill= BLACK,font=small_font_bold)        
            
    
    image.save(join(fileout_path,'ist_events_file.jpg'),quality=100) 
        

def ist_news_handler(entry,fileout_path):
    """
    Draws the news slide
    """
    
    image = Image.open("icons/ist_frame.jpg")
    draw  =  ImageDraw.Draw (image)

    CLASS_X_OFFSET=0.30*image.size[0]
    TITLE_X_OFFSET=0.30*image.size[0]
    DESCRIPTION_X_OFFSET=0.30*image.size[0]

    CLASS_Y_OFFSET=0.25*image.size[1]
    TITLE_Y_OFFSET=0.10*image.size[1]
    DESCRIPTION_Y_OFFSET=0.08*image.size[1]
    LINE_Y_OFFSET= 0.05*image.size[1]
    
    large_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
    medium_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
    small_font=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

    large_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*LARGE_FONT/1000))
    medium_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*MEDIUM_FONT/1000))
    small_font_bold=ImageFont.truetype("fonts\Ariblk.ttf",int(image.size[0]*SMALL_FONT/1000))

    y_offset=0
            
    y_offset+=CLASS_Y_OFFSET
    draw.text ( (CLASS_X_OFFSET,y_offset), u'Notícias', fill= CYAN,font=large_font)
    
    y_offset+=TITLE_Y_OFFSET
    lines=textwrap.wrap(entry['title'], width=45)
    for line in lines:
        y_offset+=LINE_Y_OFFSET
        draw.text ( (TITLE_X_OFFSET,y_offset), line, fill= BLACK,font=medium_font_bold)
   
    pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
    description=entry['description']
    description_list=pat.findall(description[0:min(400,len(description)-1)])
    description=''
    for n in range(0,len(description_list)):
        description=description + ' ' + description_list[n]
    
    y_offset+=DESCRIPTION_Y_OFFSET    
    lines=textwrap.wrap(description, width=55)   
    for line in lines:    
        y_offset+=LINE_Y_OFFSET
        draw.text ( (DESCRIPTION_X_OFFSET,y_offset), line, fill= BLACK,font=small_font_bold)        
            
            
    image.save(join(fileout_path,'ist_news_file.jpg'),quality=100) 

    
def ist_reader(fileout_path,url):
    """
    Parses the rss source
    """
    
    # try:
    feed = feedparser.parse(url)
    feed_link= feed.entries[0].link

    title=feed.entries[0].title
    description=feed.entries[0].description

    title = re.sub("<.*?>", "", title)
    description=re.sub("<.*?>", "", description)  

    entry={'title':title,'description':description}
    
    if 'Eventos' in feed.feed.title:
        ist_events_handler(entry,fileout_path)
    elif 'Noticias ' in feed.feed.title:
        ist_news_handler(entry,fileout_path)
            
    return feed_link
    
    

        