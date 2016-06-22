# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# MyHTMLParser_SASUL class

# ----------------------------------------------------------------------------

#Python modules
import re
from HTMLParser import HTMLParser


     
class MyHTMLParser_SASUL(HTMLParser):
    """
    Child class from HTMLParser (https://docs.python.org/2/library/htmlparser.html)
    Parses the XML in https://www.sas.ulisboa.pt/_archive/_rss/PT_19.xml

    """
    dataList=[]
    startTag=[]
    
    Menu={}
    mealCurrent=''
    menuCurrent=''

    def feed(self, data):
        self.rawdata = self.rawdata + data
        self.goahead(0)
        return self.Menu
    

    def handle_data(self, data):
        if len(self.startTag)>0: 
            if len(self.dataList)>0:
                self.dataList[-1]=self.dataList[-1]+data
            else:
                self.dataList.append(data)
    
    
    def handle_endtag(self, tag):
        n=-1
        while tag!=self.startTag[n]:
            n=n-1
        DataList=''.join(self.dataList[n:])
        
        #Meal tag
        if tag=='b':
            self.mealCurrent=DataList
            self.Menu[self.mealCurrent]={}
        #Menu tag
        elif tag=='em':
            self.menuCurrent=DataList
            if self.menuCurrent in self.Menu[self.mealCurrent]:
                pass
            else:
                self.Menu[self.mealCurrent][self.menuCurrent]=[]
        #Dish tag
        elif tag=='br':
            if self.menuCurrent in self.Menu[self.mealCurrent]:
                #Remove the ()
                DataList=re.sub('[()]', '', DataList)  
                #Append Dish
                self.Menu[self.mealCurrent][self.menuCurrent].append(DataList)

        del self.dataList[n:],self.startTag[n:]

    
    def handle_startendtag(self, tag, attrs):
        if tag in self.startTag:
            self.handle_endtag(tag)
            self.handle_starttag(tag, attrs) 
        else:
            self.handle_starttag(tag, attrs) 
          
          
    def handle_starttag(self, tag, attrs):
        self.startTag.append(tag)
        self.dataList.append('')
    
    
    


            
            
            