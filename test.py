from thefuzz import fuzz, process
import time
from datetime import datetime
list = [['Elecktrotechnick', 'Mechanick', 'Physik', 'mathe','banana'], ['Mechanick', 'Physik', 'mathe','banana']]
#print(process.extract("bandna", list[0], scorer=fuzz.token_set_ratio))

import time
from datetime import datetime
import random
import json

# Create a list of datetime objects
time_objects = []


    
import time
from datetime import datetime
import json


with open ('json_files/formula.json') as f:
            r_formula_json = json.load(f)
            
with open ('json_files/formula_char.json') as f:
            r_char_json = json.load(f)
                   

print()
print(r_char_json.pop(f"{r_formula_json['formula']['unnamed formula 1']['values'][1]}"))

