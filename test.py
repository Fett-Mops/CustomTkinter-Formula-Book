from thefuzz import fuzz, process
import time
from datetime import datetime
list = [['Elecktrotechnick', 'Mechanick', 'Physik', 'mathe','banana'], ['Mechanick', 'Physik', 'mathe','banana']]
#print(process.extract("bandna", list[0], scorer=fuzz.token_set_ratio))
from CTkScrollableDropdown import *
import customtkinter
import json
d = True





r = read_json('json_files/formula.json')

# Example usage:
existing_names_list = r['formula'].keys()





while d is True:
    
    l=input('input name: ')
    if l == 'q':
        d = False
    print(r['formula'].keys())
    print(generate_unique_name(existing_names_list,l))