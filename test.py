from thefuzz import fuzz, process
import time
from datetime import datetime
list = [['Elecktrotechnick', 'Mechanick', 'Physik', 'mathe','banana'], ['Mechanick', 'Physik', 'mathe','banana']]
#print(process.extract("bandna", list[0], scorer=fuzz.token_set_ratio))
from CTkScrollableDropdown import *
import customtkinter
import json



def read_json(path:str)->any:
        with open (path) as f:
            return json.load(f)


r_formula_json = read_json('json_files/formula.json')
r_char_json = read_json('json_files/formula_char.json')


        
def fuzz_search_formula( Search_Term:str,Shit='idk')-> any:
        search= {'formula': [formula for formula in r_formula_json['formula']],
                 'variables': [r_char_json[variable]['s_name'] for variable in r_char_json],
                 'search_terms': [r_formula_json['formula'][term]['search_terms'] for term in r_formula_json['formula']],
                 'category': [r_formula_json['formula'][category]['category'] for category in r_formula_json['formula']]}
        
        cat_fr = ''
        searched_formula = []
        proxil = []
        
        for cat in search:
            
           
            if cat != 'search_terms':
                
                for tp in process.extractBests(Search_Term,search[cat], scorer=fuzz.partial_ratio):
                    if tp[1] == 100:
                        tp3 = tp + (cat,)
                        
                        proxil.append(tp3)
                        
            else:
                
                for term in range(len(search[cat])):
                    for tp in process.extractBests(Search_Term,search[cat][term], scorer=fuzz.partial_ratio):
                        if tp[1] == 100:
                            tp3 = tp + (cat,)
                            proxil.append(tp3)
                            
        for tr in proxil:     
            
            if tr[2] == 'formula':
                searched_formula.append(tr[0])
                   
            elif tr[2]== 'variables':
                pass
                          
            else:
                
                    if tr[2] == 'category':
                        for formula in r_formula_json['formula']:
                            pass
                        
                    else: 
                        for formula in r_formula_json['formula']:
                            pass
                        
        #if cat_fr != '':
            
        #    r_formula_json_cp = r_formula_json.copy()
        #    r_formula_json_cp = {'formula':{key: value for key, value in r_formula_json["formula"].items() if key in searched_formula}}
        #    print('sorting output')
        #else:
        #    print('srting everything')   
q = True       
while q:
    l = input('nach formel suchen: ')
    if l == 'q':
        q = False
    fuzz_search_formula(Search_Term=l)