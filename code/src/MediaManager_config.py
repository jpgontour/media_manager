# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# MediaManager configuration parameters
# ----------------------------------------------------------------------------

#Always consider real division
from __future__ import division 


#MEDIA DIRECTORY
MEDIA_DIR='\media'


#SIDEPANEL
SIDEBAR_OFF_OFFSET=0.3  #Visible sidepanel width when not selected
SIDEBAR_OPACITY=0.8     #Sidepanel opacity
SIDEBAR_MENU_Y=0.5      #Menu icon vertical position

#HOVERING PRECISION
COLLISION_PRECISION=0.1

#FONT SIZE
HUGE_FONT=45   #not in pts
LARGE_FONT=35   #not in pts
MEDIUM_FONT=25    #not in pts
SMALL_FONT=20   #not in pts

#COLORS (rgb)
BLUE=(0,38,255)

#COLORS (rgba)
CYAN=(0, 160, 228, 255)
BLACK=(0, 0, 0, 255)


MONTHS={'janeiro': '01', 'Janeiro': '01',                                              \
                'fevereiro': '02', 'Fevereiro': '02',                                  \
                u'março': '03', u'Março': '03', 'marco':'03', 'Marco': '03',             \
                'abril': '04', 'Abril': '04',                                          \
                'maio': '05', 'Maio': '05',                                            \
                'junho': '06', 'Junho': '06',                                          \
                'julho': '07', 'Julho': '07',                                          \
                'agosto': '08', 'Agosto': '08',                                        \
                'setembro': '09', 'Setembro': '09',                                    \
                'outubro': '10', 'Outubro': '10',                                      \
                'novembro': '11', 'Novembro': '11',                                    \
                'dezembro': '12', 'Dezembro': '12',                                    \
                }

                
                
#SAS MENU UPDATE PERIOD
RSS_FEED_SAS_PERIOD=60 #seconds
#DEEC FACEBOOK PAGE UPDATE PERIOD
FEED_FBDEEC_PERIOD=60 #seconds
#IST EVENTS FEED UPDATE PERIOD
RSS_FEED_IST_EVENTOS_PERIOD=60 #seconds
#IST NEWS FEED UPDATE PERIOD
RSS_FEED_IST_NOTICIAS_PERIOD=60 #seconds
#AVAILABLE MEDIA SOURCES UPDATE PERIOD
LOAD_MEDIA_PERIOD=5 #seconds
              
#RSS LINKS              
URL_sas="https://www.sas.ulisboa.pt/_archive/_rss/PT_19.xml"                
URL_fbdeec="https://www.facebook.com/deec.ist"
URL_ist_events="http://tecnico.ulisboa.pt/pt/eventos/rss"
URL_ist_news="http://tecnico.ulisboa.pt/pt/noticias/rss"   


PIC_FORMATS=['.jpg','.JPG','.png','.PNG','.gif','.bmp']
VIDEO_FORMATS=['.mp4']


MEDIA_EXTENSIONS={'video':VIDEO_FORMATS,'teasers':VIDEO_FORMATS,'quiz':PIC_FORMATS,\
                  'AoW':PIC_FORMATS,'CoW':PIC_FORMATS,'fbdeec':PIC_FORMATS,\
                  'menu':PIC_FORMATS,'ist_news':PIC_FORMATS,'ist_events':PIC_FORMATS,\
                  'daily_specials':VIDEO_FORMATS,'deec':PIC_FORMATS}
                  
SLIDESHOW_EXTENSIONS_IN=['.ppt','.pptx']
VIDEO_EXTENSIONS_IN=['.avi','.mpeg','.mpg','.wmv','.avi','.mp4']
VIDEO_EXTENSION_OUT='.mp4'
PIC_EXTENSION_OUT='.JPG'


#MENU AND PICTURES EXHIBITION INTERVAL
MENU_TIMEOUT=10
PIC_DEFAULT_TIMEOUT=10

#KINECT PARAMETERS
KINECT_PRESS_TIMEOUT=1
KINECT_FORGET_TIMEOUT=1
KINECT_X_PREC=0.15
KINECT_Y_PREC=0.20
KINECT_X_RIGHT_OFFSET=-1
KINECT_X_LEFT_OFFSET=2.5
KINECT_Y_OFFSET=0.7
#SMOOTHING PARAMETER
SMOOTH_PAR=8/10
MOUSE_ICON_SIZE=1/4

#STATE MACHINE PROBABILITY 
PROB_DEEC={'video':0.07,'teasers':0.07,'quiz':0.07,'AoW':0.06,'CoW':0.06,'fbdeec':0.07,'menu':0,'ist_news':0.05,'ist_events':0.05,'daily_specials':0.5,'deec':0}



