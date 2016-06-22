# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# MediaManager class

# ----------------------------------------------------------------------------

#Always consider real division
from __future__ import division 

#Filename management
from os.path import isfile, isdir, join, splitext

#Python modules
import pyglet, sys , random, bisect, win32com.client, threading

#Configuration File
from MediaManager_config import *

#Auxiliary classes
from update_media import UpdateMedia


class MediaManager(pyglet.window.Window):   
    """
    Main class. Superclasses Pyglet Window. Controls Input and Media Management.
    """
    
    def __init__(self,screen,script_dir):
        """
        Initializes a MediaManager instance
        """
        
        super(MediaManager, self).__init__(fullscreen=True, visible=True,screen=screen, resizable=True)
        
        #Clear Color
        pyglet.gl.glClearColor(1,1,1,1)
        
        #Reindex Pyglet
        pyglet.resource.path.append('../icons')
        pyglet.resource.path.append('../fonts')
        pyglet.resource.reindex()
        
        #Set Mouse Invisible
        self.set_mouse_visible(False)
        
        #Media folder path
        self.media_path = script_dir + '\media'
        
        #Initialize Sidebar
        self.update_media=UpdateMedia(self.media_path)
        
        #Initialize Player, push Player handlers into MediaManager
        self.player=pyglet.media.Player()
        self.player.push_handlers(self)
        self.player.eos_action = self.player.EOS_PAUSE 
        
        #Current media
        self.media={'source':None,'aspect_ratio':None,'timeout':None,'media_x':None,'media_y':None,'width':None,'height':None,'format':None,'playing':None}
        self.next_media=self.media
        
        #Next State
        self.state={'categories':None,'source':None}

        #DEEC and QUIZ slides counter (to show in sequence)
        self.deec_counter=0
        self.quiz_counter=0
        
        
    def collision_detection(self,x,y,obj):
        """
        Detects collision between coordinates x,y and obj
        obj needs to have attributes position (int,int) [left bottom corner], width and height
        """
        
        return x>obj.position[0]-COLLISION_PRECISION*obj.width and x<obj.position[0]+obj.width+COLLISION_PRECISION*obj.width and \
               y>obj.position[1]-COLLISION_PRECISION*obj.height and y<obj.position[1]+obj.height+COLLISION_PRECISION*obj.height
               
    
    def eos(self, dt=0):
        """
        Actions to perform in the end of a source stream. 
        """
        
        pyglet.clock.unschedule(self.eos)
        #Unschedule manager
        if self.media['format']=='video':
            self.player.pause()
            self.player.next()
        self.media['playing']=False
        #Reschedule manager
        pyglet.clock.schedule_once(self.manager,0)
            
                    
    def manager(self,dt=0):
        """
        Manages transition between media sources
        """

        if self.next_media['source'] is not None:
            #Feed window  
            self.media_handler()
            #Compute next state     
            self.state_machine()
        else:
            #Compute next state     
            self.state_machine()
            #Launch Manager
            pyglet.clock.schedule_once(self.manager,0)
    

    def media_handler(self):
        """
        Feeds the window with the next source
        """

        if self.next_media['format']=='video':
            self.player.play()
        
        self.media=self.next_media
        self.resize_media()
        self.media['playing']=True
        
        self.next_media={'source':None,'aspect_ratio':None,'timeout':None,'media_x':None,'media_y':None,'width':None,'height':None,'format':None,'playing':None}
        pyglet.clock.schedule_once(self.eos,self.media['timeout'])
    
    
    def on_draw(self):
        """
        On draw events
        """
        
        self.clear()
        try:
            self.media['source'].get_texture().blit(self.media['media_x'],self.media['media_y'],width=self.media['width'], height=self.media['height'])
        except AttributeError:
            pass 

       
    def on_key_press(self,symbol,modifiers): 
        """
        Control keyboard inputs
        """
        
        #Terminate and close - Esc
        if symbol == pyglet.window.key.ESCAPE:
            self.terminate()         
        elif modifiers & pyglet.window.key.MOD_CTRL:   
            #Toggle Fullscreen ON/OFF - Ctrl + F
            if symbol == pyglet.window.key.F:
                if self.fullscreen==True:
                    self.set_fullscreen(False)
                else:
                    self.set_fullscreen(True)
            #Jump to next state - Ctrl + N
            elif symbol == pyglet.window.key.N: 
                self.eos()
                
        return True
    
    
    def on_resize(self, width, height):
        """
        On window resize events
        """
        
        super(MediaManager, self).on_resize(width, height)

        self.resize_media()

                 
    def picture_handler(self):
        """
        Loads a picture source
        """
        
        try:
            image=pyglet.image.load(self.state['source'])
            if self.state['timeout']:
                timeout=self.state['timeout']
            else:
                timeout=PIC_DEFAULT_TIMEOUT
            self.next_media={'source':image,'aspect_ratio':image.width/image.height,'timeout':timeout,'media_x':None,'media_y':None,'width':None,'height':None,'format':'picture'}
            
            return True
        except:
            return False
            
            
    def resize_media(self):
        """
        Resize window and media
        """
        
        if self.height>0:
            display_aspect_ratio=self.width/self.height

            if self.media['source']:
                
                #Fullwidth
                if display_aspect_ratio<self.media['aspect_ratio']:
                    width=self.width
                    height=self.width/self.media['aspect_ratio']
                    media_x=0
                    media_y=(self.height-height)/2
                #Fullheight
                else:
                    width=self.height*self.media['aspect_ratio']
                    height=self.height
                    media_x=(self.width-width)/2
                    media_y=0
                self.media['media_x']=media_x;self.media['media_y']=media_y
                self.media['width']=width;self.media['height']=height
            
            
    def run(self):
        """
        Launches Media_Manager
        """
        
        self.update_media.run()
        
        #Launch Manager 
        pyglet.clock.schedule_once(self.manager,0)
        
        
    def state_machine(self):
        """
        Chooses next media source based on a set of probabilities
        """
        
        # from DEEC -> choose other state 
        if self.state['categories']=='deec' or self.state['categories'] is None:
            weights=PROB_DEEC.values()
            keys=PROB_DEEC.keys()
            cumdist=[sum(weights[0:k+1]) for k in range(0,len(weights))]
            x = random.random() * cumdist[-1]
            category=keys[bisect.bisect(cumdist, x)]
            if len(self.update_media.media_files[category])>0:
                if category=='quiz':
                    self.quiz_counter=(self.quiz_counter)%len(self.update_media.media_files['quiz'].keys())+1
                    file='Slide' + str(self.quiz_counter) 
                    if file in self.update_media.media_files['quiz']:
                        self.state={'categories':'quiz','source':self.update_media.media_files['quiz'][file][1],'timeout':self.update_media.media_files['quiz'][file][0]}
                    else:  
                        return
                else:
                    file=random.choice(self.update_media.media_files[category].keys())
                self.state={'categories':category,'source':self.update_media.media_files[category][file][1],'timeout':self.update_media.media_files[category][file][0]}
            else:
                self.state={'categories':None,'source':None,'timeout':None}
                return

        # from QUIZ question -> QUIZ answer 
        elif self.state['categories']=='quiz' and self.quiz_counter%2==1:
            self.quiz_counter=(self.quiz_counter)%len(self.update_media.media_files['quiz'].keys())+1
            file='Slide' + str(self.quiz_counter) 
            if file in self.update_media.media_files['quiz']:
                self.state={'categories':'quiz','source':self.update_media.media_files['quiz'][file][1],'timeout':self.update_media.media_files['quiz'][file][0]}
            else:  
                self.state={'categories':None,'source':None,'timeout':None}
                return
        
        elif self.state['categories']=='CoW':
            category='AoW'
            file=random.choice(self.update_media.media_files[category].keys())
            self.state={'categories':category,'source':self.update_media.media_files[category][file][1],'timeout':self.update_media.media_files[category][file][0]}
            
        else:
            # From any other state -> DEEC 
            if len(self.update_media.media_files['deec'])>0:
                self.deec_counter=(self.deec_counter)%len(self.update_media.media_files['deec'].keys())+1
                file='Slide' + str(self.deec_counter)   
                if file in self.update_media.media_files['deec']:
                    self.state={'categories':'deec','source':self.update_media.media_files['deec'][file][1],'timeout':self.update_media.media_files['deec'][file][0]}
                else: 
                    self.state={'categories':None,'source':None,'timeout':None}
                    return
            else: 
                self.state={'categories':None,'source':None,'timeout':None}
                return
        
        fileName, fileExtension = splitext(self.state['source'])
        
        #File handling
        if fileExtension in VIDEO_FORMATS:
            self.video_handler()
        elif fileExtension in PIC_FORMATS:
            self.picture_handler()         
    

    def terminate(self):
        """
        Gracefully terminates Media_Manager
        """
        self.player.pause()
        pyglet.clock.unschedule(self.eos)
        self.update_media.terminate()
        pyglet.app.exit()
        self.close()   
        sys.exit()
        

    def video_handler(self):
        """
        Loads a video source
        """
        
        try: 
            video=pyglet.media.load(self.state['source'])
            self.player.queue(video)
            if hasattr(self.state,'timeout'):
                timeout=self.state['timeout']
            else:
                timeout=video.duration
            self.next_media={'source':self.player,'aspect_ratio':video.video_format.width/float(video.video_format.height),'timeout':timeout,'media_x':None,'media_y':None,'width':None,'height':None,'format':'video'}
            return True
        except:
            return False

        
    
