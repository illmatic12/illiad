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


#pip install xlrd 
#pip install openpyxl 
#install both just in case to read excel files


#opens the xml file
def open_tagplc(path):
    dataframe=pd.read_excel(path)
    return dataframe


#it's is used to see if the address tag in the csv file we made is in the excel file with the plc code and put the plc tag in our csv file
def check_connections(x,o_csv):
    if x["connection tag"]:
        if o_csv.isin([x["connection tag"]]).any().any():
            x["tag in plc"]=o_csv[o_csv["Tag Name"]==x["connection tag"]].iloc[0,1]
    return x
    

#this is for general description where we check to see if all of the text is alpha numeric and if it is we return true else we return false for the clean_tag function
def check_descriptor(text):
    text=text.replace(" ","")
    if (text.isalnum()):
        return True
    else:
        return False

#more cleaning the tags and texts, if the text tags contain non alnum we split them apart to get rid of the all the other excess and just get the address
def clean_tag(text):
    text=re.sub("[{}]","",text)
    count_t=0
    if "*N:" in text:
        x=text.split(" ")
        for count,value in enumerate(x):
            if "*N:" in value:
                count_t=count+1
                break 
        return x[count_t]
    else:
        return text


#this is for text tags, checks if the text tag caption contains only alnum values or not and puts them in their respective places
def text_info(text,csv_f,fname):
    if text["caption"] != None:
        if  not check_descriptor(text["caption"]):
            text_insert=clean_tag(text["caption"])
            csv_f=csv_f.append({"screen":fname,"object":text["name"],"connection tag":text_insert},ignore_index=True)
        else:
            csv_f=csv_f.append({"screen":fname,"object":text["name"],"general descriptor":text["caption"]},ignore_index=True)

    return csv_f

#for the multistateindicator, numericinputenable, and maintainedbutton, and momentary button connection attribute values 
def connection_tag_check(items,csv_f,fname):
    item_exp=re.sub("[{}]","",items["expression"])
    csv_f=csv_f.append({"screen":fname,"object":items.parent.parent["name"],"connection tag":item_exp},ignore_index=True)
    return csv_f


#for the multistateindicator, numericinputenable, and maintainedbutton, and momentary button connection attributes where we look for the values in the proper places

def connection_diffs(items,csv_f,fname):
    if items.name=="numericinputenable":
        for tags in items.connections.children:
            if tags.name=="connection":
                if tags["name"]=="Value":
                    csv_f=connection_tag_check(tags,csv_f,fname)
    elif items.name=="multistateindicator" or items.name =="maintainedbutton" or items.name=="momentarybutton":
        for tags in items.connections.children:
            if tags.name=="connection" :
                if tags["name"]=="Indicator":
                    csv_f=connection_tag_check(tags,csv_f,fname)
    return csv_f

#for gotobuttons
def gotobutton_add(items,csv_f,fname):
    csv_f=csv_f.append({"screen":fname,"object":items["name"],"gotoscreen":items.caption["caption"]},ignore_index=True)
    return csv_f

#for groups, where if it is a group u send it to check_items until all groups adn inner groups are represented in the csv file
def group_check(items,csv_f,fname):
    if items.children:
        for tags in items.children:
            csv_f=check_items(tags,csv_f,fname)
    return csv_f


#checks the xml file for all the tags we need values for
def check_items(items,csv_f,fname):
    four_connections=["numericinputenable","multistateindicator","maintainedbutton","momentarybutton"]
    if items.name == "text":
            csv_f=text_info(items,csv_f,fname)
    if items.name in four_connections:
        csv_f=connection_diffs(items,csv_f,fname)
    if items.name=="gotobutton":
        csv_f=gotobutton_add(items,csv_f,fname)

    if items.name=="group":
        if items.parent.name == "gfx":
            csv_f=csv_f.append({"object":""},ignore_index=True)
        csv_f=csv_f.append({"object":items["name"]},ignore_index=True)
        csv_f=group_check(items,csv_f,fname)
        csv_f=csv_f.append({"object":items["name"]},ignore_index=True)
        if items.parent.name =="gfx":
            csv_f=csv_f.append({"object":""},ignore_index=True)

    return csv_f