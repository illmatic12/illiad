from xml_read_functions import check_connections,open_tagplc,check_items
#pip install bs4
#or try pip install BeautifulSoup4
from bs4 import BeautifulSoup
#pip install lxml
import lxml
import os#this one is to get the file of the name from the path
#pip install pandas
import pandas as pd
#pip install pathlib(if u dont alreayd ahve it)
import re

from pathlib import Path
#place the path to the directory here, i used a file but just put in the directory
path="C:/Users/faysa/Desktop/xml_files"

#the path to the file you want to place ur final excel(use .csv) file info 
path2='C:/Users/faysa/Desktop/practice2.csv'

#the path to the plc tag file(put ur own and make sure to replace the \ with /)
plc_tag_path="C:/Users/faysa/Downloads/fresca.xlsx"




#get all of the xml files from the directory
xml_folder = Path(path).rglob('*.xml')
files = [x for x in xml_folder]



#For loop to iterate through all of the files

acceptable_items=["maintainedbutton","momentarybutton","text","connections","connection","group","momentarybutton"]

csv_f=pd.DataFrame(columns=["screen","object","general descriptor","connection tag","tag in plc","gotoscreen"])


for name in files:

    with open(name,"r") as xml_file:
        

        fname=os.path.basename(xml_file.name)
        bs_file=BeautifulSoup(xml_file,features="lxml")
        b_unique=bs_file.find('gfx')
        b_unique_list=list(b_unique.children)
        newlist=b_unique_list[1:40:2]
        del(b_unique)
        del(b_unique_list)
        del(bs_file)
        for items in newlist:
            csv_f=check_items(items,csv_f,fname)
        plc_tags=open_tagplc(plc_tag_path)
        plc_tags=plc_tags[1:]
        csv_f=csv_f.apply(check_connections,o_csv=plc_tags,axis=1)
        print(name,"done")   
        xml_file.close()

csv_f.to_csv(path2,index=False)




    