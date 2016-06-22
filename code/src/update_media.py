# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# UpdateMedia Class
# ----------------------------------------------------------------------------

#Filename management
from os import listdir, remove
from os.path import isfile, isdir, join, splitext

#Python modules
import pyglet, threading, csv, feedparser, time,sys, win32com.client, time, subprocess

#Configuration File
from MediaManager_config import *
      
#Auxiliary classes      
from myhtmlparser import MyHTMLParser_SASUL
from fb_reader import fb_reader
from ist_reader import ist_reader, ist_news_handler, ist_events_handler
from menu_handler import menu_handler
      
      
class UpdateMedia:
    """
    Periodically checks the Media folder and updates the list of available media sources.
    Converts the files to the required formats. 
    
    """
    
    def __init__(self,media_path):
        """
        Initializes an UpdateMedia instance
    
        """
        
        #Path to media directory
        self.media_path=media_path
        
        #SAS RSS url
        self.url_sas=URL_sas
        #DEEC FB url
        self.url_fbdeec=URL_fbdeec
        #IST events url
        self.url_events=URL_ist_events
        #IST news url
        self.url_news=URL_ist_news
        
        #List of available media sources
        self.media_files=dict.fromkeys(MEDIA_EXTENSIONS.keys(),{})

        #Cafeteria Menu
        self.menu=None
        
        #Open media organizer
        self.notebookFile=open(join(self.media_path,'notebook.csv'),'ab+')
        
        #Flags to lock/unlock Update Media, RSS SAS Reader and RSS DEEC FB reader
        self.update_media_flag=True
        self.rss_sas_reader_flag=True
        self.rss_fbdeec_reader_flag=True
        self.rss_ist_reader_flag=True
        
        #Last link
        self.last_ist_events_link=None
        self.last_ist_news_link=None
        
        #Text to display
        self.menu_labels=[]
        
        
    def check_timeout(self,fileName):
        """
        Check media file timeout
        
        """
        self.notebookFile.seek(0)
        cvsreader = csv.reader(self.notebookFile, delimiter=';')
        
        for row in cvsreader:
            if len(row)==2:
                if row[0]==fileName:
                    if int(row[1]):
                        return int(row[1])
                    else:
                        #Default: 0 seconds
                        return 0
        else:
            cvswriter = csv.writer(self.notebookFile, delimiter=';')
            cvswriter.writerow([fileName,'0'])
            return 0    
            
            
    def convert_ppt2(self,filename_in,filename_out,format):
        """
        Handles communication with a Powerpoint instance
        
        """
        
        SaveAs={'ppSaveAsMP4':39,'ppSaveAsJPG':17}

        ppMediaTaskStatusInProgress = 1
        ppMediaTaskStatusDone = 3
        ppMediaTaskStatusFailed = 4
        
        if format in SaveAs:
        
            try:
                powerpoint = win32com.client.Dispatch("PowerPoint.Application")
                powerpoint.DisplayAlerts = False
                deck = powerpoint.Presentations.Open(filename_in)
                deck.SaveAs(filename_out, SaveAs[format])
                #Wait for the convertion to finish
                while deck.CreateVideoStatus==ppMediaTaskStatusInProgress:
                    time.sleep(5)
                if deck.CreateVideoStatus==ppMediaTaskStatusFailed:
                    remove(filename_out)
                deck.Close()
                powerpoint.Quit()    
            except:
                try:
                    powerpoint.Quit()
                except:
                    pass
    

    def fbdeec_reader(self):
        """
        Reads last note or post on DEEC FB page
        """
    
        self.rss_fbdeec_reader_flag=False
        file_path_raw=join(self.media_path,'fbdeec','Raw')
        fileout_path=join(self.media_path,'fbdeec','Converted')
        
        feed_link=URL_fbdeec
        fb_reader(file_path_raw,fileout_path,feed_link)
     
        self.rss_fbdeec_reader_flag=True
    
    
    def fbdeec_reader_thread(self,dt=0):  
        """
        Lauches rss_fbdeec_reader in a thread
        """
        #If update_media is not running
        if self.rss_fbdeec_reader_flag:
            #By using threads, the process runs in the background
            update_t=threading.Thread(target=self.fbdeec_reader)
            update_t.start()

            
    def movie2mp4(self,folder_list):
        """
        Converts to a video source to mp4 using ffmpeg
        
        """
        
        for folder in folder_list:    
            folder_path_in=join(self.media_path,folder,'Raw')
            folder_path_out=join(self.media_path,folder,'Converted')        
            for file in listdir(folder_path_in): 
                file_path=join(folder_path_in,file)
                if isfile(file_path):
                    fileName, fileExtension = splitext(file) 
                    fileout=fileName+VIDEO_EXTENSION_OUT
                    if fileout not in listdir(folder_path_out) and fileExtension in VIDEO_EXTENSIONS_IN: 
                        #Calls ffmpeg with a subprocess (runs in the background)
                        p =subprocess.Popen(['start', '/MIN', '/WAIT', '/affinity', '1','./external/ffmpeg/bin/ffmpeg', '-i',file_path, '-c:v', 'libx264', '-preset', 'ultrafast', '-s', 'hd1080', '-acodec', 'mp3','-y', join(folder_path_out,fileout)],shell=True)
                        p.communicate()
                        remove(file_path) 
                        return

                        
    def ppt_sniffer(self,folder_dict):
        """
        Checks for new presentions that have not been converted yet
        
        """
        
        for folder in folder_dict.keys(): 
            folder_path_in=join(self.media_path,folder,'Raw')
            format=folder_dict[folder]
            
            if format=='ppSaveAsJPG':
                folder_path_out=join(self.media_path,folder,'Converted') 
                file_out_extension=''
            elif format=='ppSaveAsMP4':
                folder_path_out=folder_path_in
                file_out_extension=VIDEO_EXTENSION_OUT
            else:
                continue
                    
            for obj in listdir(folder_path_in):  
                obj_path=join(folder_path_in,obj)
                if isdir(obj_path):
                    for file in listdir(obj_path):  
                        file_path=join(obj_path,file)
                        if isfile(file_path):
                            fileName, fileExtension = splitext(file)
                            fileout=fileName+file_out_extension
                            if fileout not in listdir(folder_path_out) and fileExtension in SLIDESHOW_EXTENSIONS_IN:
                                self.convert_ppt2(file_path,join(folder_path_out,fileout),format)
                                remove(file_path)    
                elif isfile(obj_path):
                    fileName, fileExtension = splitext(obj)
                    fileout=fileName+file_out_extension
                    if fileout not in listdir(folder_path_out) and fileExtension in SLIDESHOW_EXTENSIONS_IN:
                                self.convert_ppt2(obj_path,join(folder_path_out,fileout),format)
                                remove(obj_path)    
  

    def rss_ist_events_reader_thread(self,dt=0):  
        """
        Lauches rss_ist_reader in a thread (events)
        """
        
        #If update_media is not running
        if self.rss_ist_reader_flag:
            #By using threads, the process runs in the background
            fileout_path=join(self.media_path,'ist_events','Converted')
            update_t=threading.Thread(target=self.rss_ist_reader,args=[fileout_path,self.url_events])
            update_t.start()
            

    def rss_ist_news_reader_thread(self,dt=0):  
        """
        Lauches rss_ist_reader in a thread (news)
        """
        
        #If update_media is not running
        if self.rss_ist_reader_flag:
            #By using threads, the process runs in the background
            fileout_path=join(self.media_path,'ist_news','Converted')
            update_t=threading.Thread(target=self.rss_ist_reader,args=[fileout_path,self.url_news])
            update_t.start()             
   
   
    def rss_ist_reader(self,fileout_path,url):
        """
        Reads IST rss (events and news)
        """
        
        self.rss_ist_reader_flag=False
        
        try:
            feed = feedparser.parse(url)
            feed_link= feed.entries[0].link
            if url==self.url_news:
                if self.last_ist_news_link!=feed_link:
                    self.last_ist_news_link=feed_link
                    ist_reader(fileout_path,url)
            elif url==self.url_events:
                if self.last_ist_events_link!=feed_link:
                    self.last_ist_events_link=feed_link
                    ist_reader(fileout_path,url)
        except:
            pass
        self.rss_ist_reader_flag=True
        
    
    def rss_sas_reader(self):
        """
        Reads SAS UL RSS 
        """
        
        self.rss_sas_reader_flag=False
        try:
            
            date=time.strftime("%x")
            tdy_mon=date[0:2]
            tdy_day=date[3:5]
            rss_entries = feedparser.parse(self.url_sas).entries
            parser = MyHTMLParser_SASUL()
            for entry in rss_entries:
                menu_date=entry.title.split()
                menu_day=menu_date[1]
                menu_month=MONTHS[menu_date[3]]
                if tdy_mon==menu_month and tdy_day==menu_day:
                    menu=parser.feed(entry.description)
                    self.menu=menu
                    break
        except:
            self.menu=None
            
        fileout_path=join(self.media_path,'menu','Converted')        
        menu_handler(self.menu,fileout_path)
        
        self.rss_sas_reader_flag=True
    
    
    def rss_sas_reader_thread(self,dt=0):  
        """
        Lauches rss_sas_reader in a thread
        """
        
        #If update_media is not running
        if self.rss_sas_reader_flag:
            #By using threads, the process runs in the background
            update_t=threading.Thread(target=self.rss_sas_reader)
            update_t.start()

            
    def run(self):
        """
        Launches UpdateMedia
        """
        
        #Scheduled routines
        pyglet.clock.schedule_interval_soft(self.update_media_thread, LOAD_MEDIA_PERIOD)
        pyglet.clock.schedule_interval_soft(self.rss_sas_reader_thread, RSS_FEED_SAS_PERIOD)
        pyglet.clock.schedule_interval_soft(self.fbdeec_reader_thread, FEED_FBDEEC_PERIOD)
        pyglet.clock.schedule_interval_soft(self.rss_ist_news_reader_thread, RSS_FEED_IST_NOTICIAS_PERIOD)
        pyglet.clock.schedule_interval_soft(self.rss_ist_events_reader_thread, RSS_FEED_IST_EVENTOS_PERIOD)
    
    
    def terminate(self):
        """
        Gracefully terminates UpdateMedia
        """
        
        pyglet.clock.unschedule(self.update_media_thread,)
        pyglet.clock.unschedule(self.rss_sas_reader_thread)
        pyglet.clock.unschedule(self.fbdeec_reader_thread)
        pyglet.clock.unschedule(self.rss_ist_news_reader_thread)
        pyglet.clock.unschedule(self.rss_ist_events_reader_thread)
        
        while not (self.update_media_flag and self.rss_sas_reader_flag and self.rss_fbdeec_reader_flag and self.rss_ist_reader_flag):
            pass
            
            
    def update_media_thread(self,dt=0): 
        """
        Lauches update_media in a thread
        """
        
        #If update_media is not running
        if self.update_media_flag:
            
            #By using threads, the process runs in the background
            update_t=threading.Thread(target=self.update_media)
            update_t.start()
     
     
    def update_media(self):
        """
        Updates the available files in the media folder
        """

        self.update_media_flag=False

        #Check converted media        
        keys=MEDIA_EXTENSIONS.keys()
        media_files=dict(zip(keys,[{} for _ in xrange(len(keys))]))
        for folder in keys:   
            folder_path=join(self.media_path,folder,'Converted')
            for obj in listdir(folder_path):
                    obj_path=join(folder_path,obj)
                    if isfile(obj_path):
                        fileName, fileExtension = splitext(obj)
                        if fileExtension in MEDIA_EXTENSIONS[folder]:
                            timeout=self.check_timeout(fileName)
                            media_files[folder][fileName]=(timeout,obj_path)
                    elif isdir(obj_path):
                        for file in listdir(obj_path):
                            file_path=join(obj_path,file)
                            if isfile(file_path):
                                fileName, fileExtension = splitext(file)
                                if fileExtension in MEDIA_EXTENSIONS[folder]:
                                    timeout=self.check_timeout(fileName)
                                    media_files[folder][fileName]=(timeout,file_path)
                        break   

        #Updates the database  
        self.media_files=media_files
        
        #Convert PPT 2 MP4
        self.ppt_sniffer({'teasers':'ppSaveAsMP4','daily_specials':'ppSaveAsMP4','deec':'ppSaveAsJPG','quiz':'ppSaveAsJPG','AoW':'ppSaveAsJPG','CoW':'ppSaveAsJPG'})
        self.movie2mp4(['teasers','video','daily_specials'])    

        self.update_media_flag=True

        
    
        
        
        
        
        
        
        