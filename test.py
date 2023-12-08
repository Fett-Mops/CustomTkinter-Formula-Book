from thefuzz import fuzz, process
import time
from datetime import datetime
list = [['Elecktrotechnick', 'Mechanick', 'Physik', 'mathe','banana'], ['Mechanick', 'Physik', 'mathe','banana']]
#print(process.extract("bandna", list[0], scorer=fuzz.token_set_ratio))
from CTkScrollableDropdown import *
import customtkinter
import json

def name_handler( name:str)->str:
        return name
def translate(text:str)->str:
    return text

def read_json( path:str)->any:
    with open (path) as f:
        return json.load(f)
    
def name_handler(name:str)->str:
    reserve_name = 'unnamed'
    if name == '':
        name = reserve_name
    

    for key in r['formula'].keys():
        
        try:
            int(key[-1])
            print('int')
        except:
            pass
    if name in r['formula'].keys():
        pass
    return name
r = read_json('json_files/formula.json')

while True:
    
    l=input('input name: ')
    name_handler(l)     