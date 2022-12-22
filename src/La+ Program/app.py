# importing library
import eel
import numpy
import os
from math import sqrt
import json
# initialize

def count_special_char(name: str) -> int:
	special_char: list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@']
	special_char_count: int = 0
	for c in name:
		if c in special_char:
			special_char_count += 1

	return special_char_count

path = os.path.dirname(os.path.abspath(__file__))
print(path)


name_length = 0
name_sp = ""
country_value = 0


def buildJSON(name, name_length, name_sp, nation, city, industry, investory, ls, fb) :
    myDict = {
    "name": name,
    "name_len": name_length,
    "name_sp": name_sp,
    "country": country_value,
    "city": city, 
    "industry": industry,
    "investory":investory,
    "last_valuation":ls,
    "feedback":fb
    }

    with open(path + "\output.json", "w") as f:
        json.dump(myDict, f, indent = 4)
        
@eel.expose
# below should be our model
def pred(name,fy,city,nation,industry,founder,investory,tf,ct,os,ls,fb):
    #frame = name,fy,city,nation,industry,founder,investory,tf,ct,os,ls
    #feature truly used:
    # name_len
    # name special char
    # city
    # country
    # industry
    # investor
    # last valuation
    # Feedback

    # length of company name
    name_length = 0
    name_length = ("".join(name)).__len__()
    # special char counts of company name
    name_sp = count_special_char("".join(name))

    buildJSON(name, name_length, name_sp, nation, city, industry, investory, ls, fb)
    
    output = "Prediction result should be here"
    return output

eel.init(path)
# start
eel.start('myWebpage.html')


