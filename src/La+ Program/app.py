# importing library
import eel
import numpy
from math import sqrt
# initialize

def count_special_char(name: str) -> int:
	special_char: list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@']
	special_char_count: int = 0
	for c in name:
		if c in special_char:
			special_char_count += 1

	return special_char_count


eel.init("../fp_front")

@eel.expose
# below should be our model
def pred(name,fy,city,nation,industry,founder,investory,tf,ct,os,ls):
    #frame = name,fy,city,nation,industry,founder,investory,tf,ct,os,ls
    #feature truly used:
    # name_len
    # name special char
    # city
    # country
    # industry
    # investor
    # last valuation

    # length of company name
    name_length = 0
    name_length = ("".join(name)).__len__()
    # special char counts of company name
    name_sp = count_special_char("".join(name))
    #country name
    country_n = ("".join(nation)).lower()
    country_value = 0
    if country_n == "united states":
        country_value = 0
    elif country_n == "china":
        country_value = 1

    #city
    city_name = ("".join(city)).lower()
    #default
    city_value = 0
    if city_name == "san francisco":
        city_value = 0
    elif city_name == "new york":
        city_value = 1


    #this sould be button or scroll to choose
    industry_type = ("".join(industry)).lower()
    #print(industry_type)
    #default
    industry_value = 0
    #industry: dict = {'artificial intelligence': 0, 'fintech': 1, 'internet software & services': 2, 'analytics': 3, 'biotechnology': 4, 'health care': 5, 'e-commerce & direct-to-consumer': 6}
    match industry_type:
        case "artificial intelligence":
            industry_value = 0
        case "fintech":
            industry_value = 1
        case "internet software & services":
            industry_value = 2
        case "analytics":
            industry_value = 3
        case "biotechnology":
            industry_value = 4
        case "health care":
            industry_value = 5
        case "e-commerce & direct-to-consumer":
            industry_value = 6
    #test get value
    #print(industry_value)

    #this sould be button or scroll to choose
    investor_type = ("".join(investory)).lower()
    #default
    investor_value = 0

    #print(investor_type)

    investory: dict = {'andreessen horowitz': 0, 'techstars': 1, 'alumni ventures': 2, 'y combinator': 3, 'sequoia capital': 4, '500 global': 5, 'insight partners': 6}
    match investor_type:
        case "andreessen horowitz":
            investor_value = 0
        case "techstars":
            investor_value = 1
        case "alumni ventures":
            investor_value = 2
        case "y combinator":
            investor_value = 3
        case "sequoia capital":
            investor_value = 4
        case "500 global":
            investor_value = 5
        case "insight partners":
            investor_value = 6

    #test get value
    #print(investor_value)

    #last valuation
    last_valuation_value = 0
    last_valuation_value = ("".join(ls)).__len__()-1

    output = "here should be prediction"
    return output

# start
eel.start('myWebpage.html')
