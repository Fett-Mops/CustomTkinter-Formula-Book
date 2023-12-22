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


        
def fuzz_search_formula( Shit:any, Search_Term:str)-> any:
        search= {'formula': [formula for formula in r_formula_json['formula']],
                 'variables': [r_char_json[variable]['s_name'] for variable in r_char_json],
                 'search_terms': [r_formula_json['formula'][term]['search_terms'] for term in r_formula_json['formula']],
                 'category': [r_formula_json['formula'][category]['category'] for category in r_formula_json['formula']]}
        
        proxil, searched_formula = [], []
        
      
        if Search_Term != '':
            for cat in search:
                
           
                if cat != 'search_terms':
                
                    for tp in process.extractBests(Search_Term,search[cat], scorer=fuzz.partial_ratio,limit=100):
                        if tp[1] == 100:
                            if cat == 'variables':
                                for key, var in r_char_json.items():
                                    if var["s_name"] == tp[0]:
                                        tp3 = (key, cat)
                            else:
                                tp3 = (tp[0] ,cat)
                            proxil.append(tp3)
                else:
                    for term in range(len(search[cat])):
                        for tp in process.extractBests(Search_Term,search[cat][term], scorer=fuzz.partial_ratio, limit=100):
                            if tp[1] == 100:
                                tp3 = (tp[0] ,cat)
                                proxil.append(tp3)
            for tp in proxil:      
                    if tp[1] == 'formula':
                        searched_formula.append(tp[0])  
                    else:
                        for formula in r_formula_json['formula']:
                            if tp[1] == 'category':
                                if r_formula_json['formula'][formula][tp[1]] == tp[0]:
                                    searched_formula.append(formula) 
                            elif tp[1] == 'variables':
                                    if int(tp[0]) in r_formula_json['formula'][formula]['values']:
                                        if formula not in searched_formula:
                                            searched_formula.append(formula)
                            else: 
                                if tp[0] in   r_formula_json['formula'][formula]['search_terms']:
                                    searched_formula.append(formula)       
            r_formula_json_cp = r_formula_json.copy()
            r_formula_json_cp = {'formula':{key: value for key, value in r_formula_json["formula"].items() if key in searched_formula}}
            print(searched_formula)
        
            print((r_formula_json_cp).keys())
        else:
            print({'formula':{}})
q = True       
while q:
    l = input('nach formel suchen: ')
    if l == 'q':
        q = False
    fuzz_search_formula(Search_Term=l,Shit='d')