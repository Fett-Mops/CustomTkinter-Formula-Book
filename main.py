from tkinter import *
import customtkinter as ct
from sympy import *
import CTkMessagebox
import CTkToolTip
from CTkScrollableDropdown import *
from pylatex import *

import os
import time
from datetime import datetime
#import dl_translate as dlt
#from dl_translate import *
#from translate import Translator


from PIL import Image, ImageTk
import json
import si_prefix




WIDTH, HEIGHT = 600,600
appearance = ['System', 'light', 'dark']
color_def = ['green', 'blue','dark-blue']


root = ct.CTk()
root.geometry(f'{WIDTH}'+'x'+f'{HEIGHT}')


root.title('Formelbüchlein')

# Grid configer
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

#colors
red = '#E26579'
red_b = '#D35B58'
red_h = '#C77C78'
main_col ={'green':'#00947D','blue': '#008FBE', 'dark-blue': '#5C84C3', 'orange':'#FFD382'}
menu_col = {'green': '#008180','blue': '#00B1BC', 'dark-blue': '#7764AC','orange':'#B5AA99'}
menu_h_col = {'green': '#006E7A','blue': '#0073A0', 'dark-blue': '#4E5C9F','orange':'#4F4537'}
del_col = {'green': '#FFA17A','blue': '#AF4079', 'dark-blue': '#C0697D','orange':'#FE8A7E'}
del_h_col = {'green': '#F98383','blue': '#9F5399', 'dark-blue': '#88364C','orange':'#C1554D'}
text_col = ('#1B231A','#DCE4DB')


grey=('#CCCCCC','#333333')
grey_fram = ('#DBDBDB','#2B2B2B')
d = '#2FA572'
grey_disa = '#61676C'



font1 =("None",15)

#pictures
sort_name = ['home-category',
             'add-folder',
             'add-list',
             'u_arrow',
             'd_arrow',
             'edit-formula',
             'edit-info',
             'home-category',
             'home',
             'icon-infoo',
             'reload',
             'remove-formula',
             'settings',
             'speaker_off',
             'speaker_on',
             'createdate',
             'abc']
pngs = {}
for i in sort_name:
    pngs[i] =ct.CTkImage(dark_image=Image.open("pictures/white/"+i+'.png'),
                   light_image=Image.open("pictures/black/"+i+'.png'),
                   size=(30, 30))

frame = ct.CTkFrame(root, width=25)
frame.grid(row = 0,rowspan=2, column=0, sticky='nws', pady=(4,5), padx=(5,5))
frame.grid_rowconfigure(3,weight=1)



class Gui:
    def __init__(self):
        self.cal_bool = False
        self.h_page =  ct.CTkFrame(root, fg_color='transparent')
        self.c_page =  ct.CTkFrame(root, fg_color='transparent')
        self.s_page =  ct.CTkFrame(root, fg_color='transparent')
        self.a_page =  ct.CTkFrame(root, fg_color='transparent')
        self.c1_page =  ct.CTkFrame(root, fg_color='transparent')
        self.si_index = []
        self.si_str = si_prefix.SI_PREFIX_UNITS
        self.cal_rad_var = ct.IntVar(value=0)
        self.cal_rad2_var = ct.StringVar(value='T')
        self.cal_rad_first = False
        self.info_str_var = ct.StringVar(value='sdfadf')
        self.auto_th_var = ct.Variable()
        self.man_th_var = ct.Variable()
        self.popup_var = ct.Variable()
        self.sound_slider_var = ct.Variable()
        self.sound_slider_boo = ct.BooleanVar()
        self.lan_menu_var = ct.Variable()
        self.toplevell = False
        self.toplevel = None
        self.user_json_cp = ''
        self.sorting_var = 0
        #need to translate this
        self.sort_tip_var ='alphabetical'
        self.sort_but_img = [pngs['abc'],pngs['createdate'],pngs['home-category']]
        self.rm_box = ct.BooleanVar(value=1)
        self.new_frm_name = ct.StringVar()
        self.old_frm_name = ct.StringVar()
        self.languages =  ['English', 'Deutsch', 'Français']
        self.translater = {}
        self.color_lang = {'English':['green', 'blue', 'dark-blue', 'orange'],
                           'Deutsch':['Grün', 'Blau','Dunkel-Blau', 'Orange'],
                           'Français':['vert', 'blue', 'dark-blue', 'orange']}
        self.var_inps = []
        self.search_inp = ct.StringVar()
        self.inp_formula_var = ct.StringVar()
        self.cat_inp = ct.StringVar()
        self.edit_bool = False
  
    def translate(self, text):
        help = 'help'
        if self.lan_menu_var.get()== 'English':
            return text
        else:
            try:
                help =self.translater[text]
            except:
                # ? only print with excuse
                
                print(text)
            return help
    
    def write_json(self, path:str, inp:any)->any:
        with open (path, 'w') as f:
            json.dump(inp, f, indent=4)
            
    def read_json(self, path:str)->any:
        with open (path) as f:
            return json.load(f)

    def open_file(self, file:str)->None:
        os.system('start '+file)
         
    def add_formula(self, new_frm_name:str, first_var:int):
        # TODO if added not sorted pls change
        global scr_frame, boxes, information,info_index, coc
        
        
        for kid in frame.winfo_children():
            kid.configure(state='disabled') 
            kid.configure(fg_color=self.colorscale(col_th, .5))
            
        self.a_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.a_page.grid_columnconfigure([0,1,2], weight=1)
 
           
        self.a_page.grid_rowconfigure(2, weight=1)  
        self.a_page.tkraise()
        
        name_formula = ct.CTkEntry(master=self.a_page,
                                placeholder_text=self.translate('formula name'),
                                fg_color=col_th,border_width=0,
                                placeholder_text_color=text_col,
                                text_color=text_col,justify='center',
                                textvariable=self.new_frm_name,
                                )

        name_formula.grid(row=0, column=0,columnspan=4, sticky='nswe', pady=(0,5))
        
        inp_formula = ct.CTkEntry(master=self.a_page,width=50, height=35,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text=self.translate('formula'),
                                        placeholder_text_color=text_col,
                                        textvariable=self.inp_formula_var)
        inp_formula.grid(row=1, column=0,columnspan=3, sticky='nswe', pady=(0,5))
        
        helpful_frame = ct.CTkFrame(master=self.a_page, fg_color='transparent')
        helpful_frame.grid(row=1, column=3, padx=(5,0),pady=(0,5))
        
        pngs['icon-infoo'].configure(size=(30,30))
        info_format_but = ct.CTkButton(master= helpful_frame, height=35, text = '',
                                                  image=pngs['icon-infoo'],
                                                  width=10, command=lambda:(self.open_file()))
        info_format_but.grid(row=0, column=2, padx=(5,0))
        
        
        edit_info_but = ct.CTkButton(master= helpful_frame, height=35, text = '',
                                                  image=pngs['edit-info'],
                                                  width=10, command=lambda:(self.edit_info(new_frm_name,None)))
        edit_info_but.grid(row=0, column=1, padx=(5,0))
        

        reload_scr_frame = ct.CTkButton(master=helpful_frame, image=pngs['reload'],width=60, height=35, text = '',
                                        command=lambda:(self.read_formula(inp_formula)))
        reload_scr_frame.grid(row=0, column=0)
        
        
        #scrolable fram
        scr_frame = ct.CTkScrollableFrame(master=self.a_page, fg_color=grey_fram)
        scr_frame.grid(row=2, column=0, columnspan=4, sticky='nswe')
        scr_frame.grid_columnconfigure(0, weight=1)
        scr_frame.grid_rowconfigure(0, weight=1)   
        
        labl_frame = ct.CTkFrame(scr_frame,fg_color=grey)
        labl_frame.grid(row=0,column=0,sticky='nswe',padx=5, pady=5)
        labl_frame.grid_columnconfigure([0,1,2,3,4,5], weight=1)
        labl_frame.grid_rowconfigure(0, weight=1)
        
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('con value'), font=font1)
        cal_label.grid(row=0, column=0, padx=5)
        
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('Unit'), font=font1)
        cal_label.grid(row=0, column=1, sticky='nswe', padx=5)
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('Unit name'), font=font1)
        cal_label.grid(row=0, column=2, sticky='nswe', padx=5)
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('symbol'), font=font1)
        cal_label.grid(row=0, column=3, sticky='nswe', padx=5)
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('symbol name'), font=font1)
        cal_label.grid(row=0, column=4, sticky='nswe', padx=5)
        cal_label = ct.CTkLabel(master=labl_frame,
                                text=self.translate('info'), font=font1)
        cal_label.grid(row=0, column=5, padx=5)
        
            
        
        
        boxes,  info_index = [], []
        information = [[inp_formula],]   
        
        coc =[]     #TODO: rm name thks
        number = 3
        
        self.edit_var(new_frm_name,number, first_var)
        
        inp_category = ct.CTkEntry(master=self.a_page,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text=self.translate('category'),height=35,
                                        placeholder_text_color=text_col,
                                        textvariable=self.cat_inp)
        inp_category.grid(row=3, column=0,columnspan=4, sticky='we', pady=5)
        
        information.append(inp_category)

        save_but = ct.CTkButton(master=self.a_page, text=self.translate('save'), height=35,text_color= text_col,
                                           command= lambda:(self.get_formula(name_formula.get(),information,'not pp')))
        save_but.grid(row = 4, column=2,columnspan= 2, sticky='nwse') 
        
        
        cancle_but = ct.CTkButton(master=self.a_page, text=self.translate('cancle'),text_color= text_col,
                                             height=35, fg_color=del_col[def_col],hover_color=del_h_col[def_col],
                                             command=lambda:(self.get_formula(new_frm_name,information,'pp')))
        
        cancle_but.grid(row = 4, column=0, columnspan= 2,sticky='nwse',padx=(0,5)) 
        try:
            self.new_frm_name.set(new_frm_name)
            self.inp_formula_var.set(r_formula_json['formula'][new_frm_name]['formula'][0])
            self.cat_inp.set(r_formula_json['formula'][new_frm_name]['category'])
        except:
            pass
    
    def read_formula(self, l_formula):
        pass
         #\frac = /
         #\frac{\frac{1}{x}+\frac{1}{y}}{y-z}
    
    def edit_var(self, formula:str, number:int, first_var : int):
        self.var_inps = [ct.StringVar() for _ in range(number)]
        self.unit_inps = [ct.StringVar() for _ in range(number)]
        self.unit_n_inps = [ct.StringVar() for _ in range(number)]
        self.symb_n_inps = [ct.StringVar() for _ in range(number)]
        self.boxes = [ct.Variable() for _ in range(number)]
        
        for i in range(number):            
            inp_frame = ct.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i+1, column=0, columnspan=4,sticky='nswe', pady=5, padx=5)
            inp_frame.grid_columnconfigure([1,2,3,4,5], weight=2)
            
                

            inp_frame.grid_rowconfigure( [j for j in range(number)], weight=1)  
            
            box_x = ct.CTkCheckBox(master=inp_frame,text='', width=5,
                                                corner_radius=5,
                                                variable=self.boxes[i],
                                                command=lambda i = i: (self.add_con(i, coc)))
            boxes.append(box_x)
            box_x.grid(row=0, column=0, pady=5, padx=(10,0))    
                 
            var_inp = ct.CTkEntry(master=inp_frame,textvariable=self.var_inps[i],
                                    width=50, height=35,  fg_color=grey, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,text_color=text_col, state='disabled')
            
            var_inp.grid(row = 0, column=1, pady= 5, sticky='nwes')
            

                                          
            unit_inp = ct.CTkEntry(master=inp_frame,textvariable=self.unit_inps[i]
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,text_color=text_col)
            unit_inp.grid(row = 0, column=2,  pady= 5, padx=(5,0), sticky='nwes')
            
            unit_n_inp = ct.CTkEntry(master=inp_frame,textvariable=self.unit_n_inps[i]
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,text_color=text_col)
            unit_n_inp.grid(row = 0, column=3, pady= 5,padx=(5,0), sticky='nwes')
        
        #change to listU
            symb_label = ct.CTkLabel(master = inp_frame  ,text=self.translate('formula'), font=font1, 
                                           fg_color=grey,text_color=text_col,)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
            
            symb_n_inp = ct.CTkEntry(master=inp_frame,textvariable=self.symb_n_inps[i]
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,text_color=text_col)
            symb_n_inp.grid(row = 0, column=5, pady= 5, sticky='nwes')
            
            
            #info   
     
            info_index.append(first_var + i)
            r_formula_json['formula'][formula]['values'].append(var)
            r_char_json[info_index[i]] ={
                            "symbol": 'change Thies',
                            "s_name": "",
                            "value": None,
                            "unit": '',
                            "u_name": '',
                            "category": '',
                            "information": "cock " +f'{info_index[i]}'}
       
            #Help
            pngs['icon-infoo'].configure(size=(30,30))
            edit_var_info_but = ct.CTkButton(master=inp_frame,
                                           text='' ,
                                           image=pngs['edit-info'],width=30,height= 35, 
                                           command=lambda i = i:(self.edit_info(formula,info_index[i])) )
            edit_var_info_but.grid(row = 0, column=6, sticky='nwe', pady = 5, padx=5) 
            
            coc.append(var_inp)
            try:
                short = r_char_json[f"{r_formula_json['formula'][formula]['values'][i]}"]
                
                self.symb_n_inps[i].set(value=short['s_name'])
                self.unit_inps[i].set(value=short['unit'])
                self.unit_n_inps[i].set(value=short['u_name'])
                #TODO: Val if cancle not pop but leafe idk
                if short['value'] != None:
                    self.var_inps[i].set(value=short['value'])
                    self.boxes[i].set(value=1)
                    var_inp.configure(fg_color=col_th, state='normal')
                    

            except:
                pass
          
    def add_con(self, index:int, var_inp: Widget):
        if var_inp[index].cget('fg_color') == grey:
            var_inp[index].configure(fg_color=col_th, state='normal')
        else:
            var_inp[index].configure(fg_color=grey, state='disabled')
            self.var_inps[index].set(value='')
    
    def get_formula(self, new_frm_name : str, information:list[str,list[str],str], *args):
        
        if  args[0] == 'pp':
            
            
            self.idk_dont_look(self.translate("don't save changes"),
                               None,[self.translate("don't save")],
                               'center', False,self.translate('leaf'),
                               new_frm_name)  
        elif self.edit_bool:
            self.edit_for_var(new_frm_name , information)
        else:
            
            
            self.add_for_var(new_frm_name, information)
        
    def edit_for_var(self,new_frm_name , information):
        
        
        r_char_json_cp = r_char_json.copy()
        r_formula_json_cp = r_formula_json.copy()
        
        r_formula_json_cp['formula'][new_frm_name] = r_formula_json_cp['formula'].pop(self.old_frm_name.get())
  
        
        r_formula_json_cp['formula'][new_frm_name]['formula'][0] = self.inp_formula_var.get()
        
        r_formula_json_cp['formula'][new_frm_name]['category'] = self.cat_inp.get()    
       
        
        
        for  i, var in enumerate(r_formula_json_cp['formula'][new_frm_name]['values']):
              
            if self.var_inps[i].get() == '':
                r_char_json_cp[f'{var}']['value'] = None
            else:
                r_char_json_cp[f'{var}']['value'] = self.var_inps[i].get()
            r_char_json_cp[f'{var}']['u_name'] = self.unit_n_inps[i].get()
            r_char_json_cp[f'{var}']['s_name'] = self.symb_n_inps[i].get()
            #r_char_json[char_len+i]['information'] = information[1][3][i].get()
        
    
        
        
        self.idk_dont_look(self.translate('save chages'), None,[self.translate('save')],
                           'center', False,self.translate('save'),new_frm_name)
    
    def add_for_var(self,new_frm_name, information):
        
        r_formula_json['formula'][new_frm_name] = r_formula_json['formula'].pop(self.old_frm_name.get())
        #information = [[inp_formula,edit_info_box],
        #print(self.var_inps)
        #self.unit_inps
        #self.unit_n_inps
        #self.symb_n_inps
        #self.symb_inps
        # category] 
       
        r_formula_json['formula'][new_frm_name]['formula'][0] = self.inp_formula_var.get()
        #information[0][0].get()
        #r_formula_json['formula'][new_frm_name]['information'] = information[0][1].get() 
        r_formula_json['formula'][new_frm_name]['category'] = self.cat_inp.get()     
            
        char_len = len(r_char_json)
        # char exept symbol is working

            
        for  i, var in enumerate(self.var_inps):
            r_char_json[char_len+i]['u_name'] = self.unit_n_inps[i].get()
            r_char_json[char_len+i]['s_name'] = self.symb_n_inps[i].get()
            r_char_json[char_len+i]['category'] = self.cat_inp.get()
            #r_char_json[char_len+i]['information'] = information[1][3][i].get()
            if self.var_inps[i].get() == '':
                r_char_json[char_len+i]['value'] = None
            
            
        self.idk_dont_look(self.translate('save chages'), None,[self.translate('save')],
                           'center', False,self.translate('save'),new_frm_name)

    def idk_dont_look(self, message, icon, options, justify, sound, title, new_frm_name):
        
        global r_formula_json, r_char_json
    
        if self.popup_var.get() or self.messagebox(message,icon, options, justify, sound, title):
           
            if title ==  self.translate('save'):
                r_formula_json['formula'][new_frm_name]['creationdate'] = datetime.now().strftime("%d.%m.%Y %H:%M")
                self.write_json('json_files/formula.json',r_formula_json)
                self.write_json('json_files/formula_char.json',r_char_json)
                r_formula_json = self.read_json('json_files/formula.json')
                r_char_json = self.read_json('json_files/formula_char.json')
                
                
                
                self.user_settings()
                
            elif title == self.translate('leaf'):
                if self.edit_bool:

                    self.edit_bool = False
                else:
                    
                    r_formula_json['formula'].pop(new_frm_name)
             
                    
                
 

            for kid in frame.winfo_children():
                    kid.configure(state='normal') 
                    kid.configure(fg_color=col_th)
            self.sorting(r_formula_json, False)
                                 
    def clamp(self, val, minimum=0, maximum=255):
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    def colorscale(self,hexstr, scalefactor):
        hexstr = hexstr.strip('#')

        if scalefactor < 0 or len(hexstr) != 6:
            return hexstr

        r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

        r = int(self.clamp(r * scalefactor))
        g = int(self.clamp(g * scalefactor))
        b = int(self.clamp(b * scalefactor))
        
        

        return "#%02x%02x%02x" % (r, g, b)
    
    
    
    def edit_info(self, formula, var):
        
        
        if self.toplevell :
            self.toplevell = False
            
        if not self.toplevell:
            self.toplevel = ct.CTkToplevel()
            self.toplevel.geometry("400x500")
            self.toplevel.rowconfigure(1, weight=2)
            self.toplevel.rowconfigure(0, weight=1)            
            self.toplevel.columnconfigure(0, weight=1)
            self.toplevel.attributes("-topmost", True)
            self.toplevell = True
            
        edit_info_win = ct.CTkTextbox(self.toplevel,fg_color=grey)
        #independent
        edit_info_win.grid(row=1,column=0, sticky='nswe', pady=5, padx=5)
        
        if var != None:
            var_sym = ct.CTkTextbox(self.toplevel,fg_color=grey)
            var_sym.grid(row=0,column=0, sticky='nswe', pady=(5,0), padx=5)
            edit_info_win.insert('end',r_char_json[var]['information'])
        else:
            formula_la = ct.CTkTextbox(self.toplevel,fg_color=grey)
            formula_la.grid(row=0,column=0, sticky='nswe', pady=(5,0), padx=5)

            terms_inp = ct.CTkTextbox(self.toplevel,fg_color=grey)
            terms_inp.grid(row=0,column=1, rowspan=2, sticky='nswe', pady=(5,0), padx=5)
            terms_inp.insert('end', r_formula_json['formula'][formula]['search_terms'])
            
            edit_info_win.insert('end',r_formula_json['formula'][formula]['information'])

        save_edit = ct.CTkButton(self.toplevel, text=self.translate('save'))
        save_edit.grid(row=3,column=0, sticky='nswe', padx=5,pady=(0,5))
          
          
                
    def add_formula_name(self):
        frm_name = ct.CTkInputDialog(title=self.translate('name formula'), button_text_color= text_col,
                                     text=self.translate('naming the formula'))
        frm_var = frm_name.get_input()
        frm_safe = self.translate('unnamed formula')
        # TODO if delt and new errors possible
        if  frm_var!= None:
            if frm_var != '':
                frm_safe = frm_var
            else:
                for i in range(len(r_formula_json['formula'])):
                    if i >=1:
                        try: 
                            r_formula_json['formula'][frm_safe +f' {i}' ]
                            
                        except:                      
                            frm_safe = frm_safe +f' {i}' 
                            
            self.new_frm_name.set(frm_safe)
            self.old_frm_name.set(frm_safe)
            r_formula_json['formula'][frm_safe] = {'search_terms':[],
                                                   'formula':['2=1*1',[1,1,1]],
                                                   'values':[],
                                                   'information': 'insert info',
                                                   'category' : '',
                                                   'creationdate':''}
            frm_safe = self.translate('unnamed formula')
            
            self.add_formula(self.new_frm_name.get(), len(r_char_json))
                
    def remove_formula(self,formula):
        
        
        rm_message = CTkMessagebox.CTkMessagebox(master= root,
                        message=self.translate("Bist du sicher das du die Formel: {}{}{} löschen willst?").format("'",formula,"'"),
                        justify='right', icon=False,
                        title=self.translate('delete formula'), option_1=self.translate('delete')) 
        rm_comp = ct.CTkCheckBox(master = rm_message, text=self.translate('also delete components'), variable=self.rm_box)
        rm_comp.place(x=10,y=160)
        
        if rm_message.get() == self.translate('delete'):
            if rm_comp.get():
                for var in r_formula_json['formula']:
                        if formula == var:
                            break
                        #TODO: Understand and fix
                        
                        for i in range(len(r_formula_json['formula'][formula]['values'])):
                            current_value = r_formula_json['formula'][formula]['values'][i]

                            if current_value not in r_formula_json['formula'][var]['values']:
                                try:
                                    r_char_json.pop(current_value)
                                    
                                except KeyError:
                                    pass
                                self.write_json('json_files/formula_char.json', r_char_json)
  
                                    
                
            r_formula_json['formula'].pop(formula)
            self.write_json('json_files/formula.json', r_formula_json)  
            self.rm_box.set(value= 1)

    
            self.home()

    def search_formula(self,Shit:any, Search_Term:str)-> any:
        search= {'formula': [formula for formula in r_formula_json['formula']],
                 'variables': [r_char_json[variable]['s_name'] for variable in r_char_json],
                 'search_terms': [r_formula_json['formula'][term]['search_terms'] for term in r_formula_json['formula']],
                 'category': [r_formula_json['formula'][category]['category'] for category in r_formula_json['formula']]}
        cat_fr = ''
        searched_formula = []
        
        for cat in search:
            if cat != 'search_terms':
                if Search_Term in search[cat]:
                        cat_fr = cat
                        
            else:
                for term in range(len(search[cat])):
                    if Search_Term in search[cat][term]:
                        cat_fr = cat
                        
               
            if cat_fr == 'formula':
                searched_formula.append(Search_Term)
                   
            elif cat_fr == 'variables':
                for variable in r_char_json:
                    if Search_Term == r_char_json[variable]:
                        searched_formula.append(variable)            
            else:
                for formula in r_formula_json['formula']:
                    if cat_fr == 'category':
                        if Search_Term == r_formula_json['formula'][formula][cat_fr]:
                            searched_formula.append(formula)
                   
                    else: 
                        if Search_Term in r_formula_json['formula'][formula]['search_terms']:
                            searched_formula.append(formula)
        if cat_fr != '':
            
            r_formula_json_cp = r_formula_json.copy()
            r_formula_json_cp = {'formula':{key: value for key, value in r_formula_json["formula"].items() if key in searched_formula}}
            self.show_formulas(r_formula_json_cp)
        else:
            self.show_formulas({'formula':{}})       
   
    def edit_formula(self, formula:str):
        self.edit_bool = True
        self.old_frm_name.set(value=formula)
        self.add_formula(formula,len(r_char_json))
   
    def set_values(self, formula):

        global unit_label, Buttons, Units, edit_formula_but, del_formula_but, cal_inp_var
        
        add_formula_but.grid_forget()
        pngs['edit-formula'].configure(size=(40,40))
        edit_formula_but = ct.CTkButton(master=frame, image=pngs['edit-formula'],
                                        text='', width=60, height=60,fg_color=menu_col[def_col],
                                        hover_color=menu_h_col[def_col], 
                                        command=lambda: self.edit_formula(formula))
        edit_formula_but.grid(row=1 ,column=0,pady=10, padx=10)
        
        
        #remove formula
        pngs['remove-formula'].configure(size=(40,40))
        del_formula_but = ct.CTkButton(master=frame, image=pngs['remove-formula'],
                                       text='', width=60, height=60, fg_color=del_col[def_col],
                                       hover_color=del_h_col[def_col],
                                       command=lambda formula= formula :self.remove_formula(formula))
        del_formula_but.grid(row = 2, column=0,pady=10, padx=10)     
        self.cal_bool = True
            

        self.c_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.c_page.tkraise()
        self.c_page.grid_columnconfigure([0,1,2], weight=1)        
        self.c_page.grid_rowconfigure(2, weight=1)     
        #label
        label_frame= ct.CTkFrame(master=self.c_page)
        label_frame.grid(row=0, column=0, columnspan=4, sticky='nswe',pady=(0,10))
        
        cal_label = ct.CTkLabel(master=label_frame,
                                text=self.translate('help'), font=font1)
        cal_label.grid(row=1, column=0, sticky='nswe', padx=5)
        cal_label.grid_columnconfigure(0, weight=1)
        cal_label.grid_rowconfigure(0, weight=1)
        
        
        #scrolable fram
        scr_frame = ct.CTkScrollableFrame(master=self.c_page)
        scr_frame.grid(row=2, column=0, columnspan=4, sticky='nswe')
        scr_frame.grid_columnconfigure(0, weight=1)
        scr_frame.grid_rowconfigure(0, weight=1)   
        

        cal_inp_var = [ct.StringVar(value='') for _ in range(len(r_formula_json['formula'][formula]['formula'][1]))]
        ryd_loop =r_formula_json['formula'][f'{formula}']['formula'][0].replace('*', '').replace('+', '').replace('-', '').replace('=', '').replace('/', '')
        Units, Buttons, inp = [], [[],[]], []
        cover = True
        self.si_index[8 for _ in range(ryd_loop)]
        for i, var in enumerate(ryd_loop)  :            
            inp_frame = ct.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i, column=0, sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([0,1,2,4], weight=2)
           
            inp_frame.grid_rowconfigure([0,1,2,4,5], weight=1)  
     
            box_x = ct.CTkRadioButton(master=inp_frame,text='', width=5,
                                                 corner_radius=5,
                                                 value=i, variable=self.cal_rad_var,
                                                 command=lambda inp = inp: self.disable_inp(inp, formula))
            box_x.grid(row=0, column=0, pady=5, padx=(5,0))     
            var_inp = ct.CTkEntry(master=inp_frame
                                ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                placeholder_text_color=text_col,
                                textvariable=cal_inp_var[i]
                                )
            unit_label = ct.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                            text= r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][i]}"]['unit'])
            if r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][i]}"]['value'] != None:
                cal_inp_var[i].set(r_char_json[f"{r_formula_json['formula'][formula]['values'][i]}"]['value'])
                box_x.configure(border_color=grey_disa,state='disabled')
               
                var_inp.configure(fg_color=self.colorscale(col_th, 0.5), 
                                    placeholder_text_color=grey_disa,
                                    textvariable=cal_inp_var[i],
                                    state='disabled'
                                    )
                                   
                unit_label = ct.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                                text= r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][i]}"]['unit'])
            
                    
                    
                    # ! not functional for more var than three
            
            if r_char_json[f"{r_formula_json['formula'][formula]['values'][i]}"]['value'] == None:
                if cover:
                    
                    var_inp.configure(state='disabled')
                    var_inp.configure(fg_color=self.colorscale(col_th,.5))
                    self.cal_rad_var.set(i)
                    cover = False

            var_inp.grid(row = 0, column=1, pady= 5, padx=(5,0), sticky='nwes')
            inp.append(var_inp)

            ud_frame = ct.CTkFrame(master =inp_frame,bg_color='transparent', fg_color=grey)
            ud_frame.grid(column=2, row=0)
            

            pngs['u_arrow'].configure(size=(20,20))
            up_but = ct.CTkButton(master=ud_frame, image=pngs['u_arrow'],
                                  text='',  width=0, height=0, hover=False, fg_color=grey,
                                  command=lambda i = i, f = formula: (self.add(self.si_index,f,i)))
            up_but.grid(row = 0, column=0, sticky='nswe')
            Buttons[0].append(up_but)
        
            pngs['d_arrow'].configure(size=(20,20))
            down_but = ct.CTkButton(master=ud_frame, image=pngs['d_arrow'], text='', width=0, height=0,
                                               hover=False, fg_color=grey,
                                               command=lambda i = i, f = formula: (self.sub(self.si_index,f,i)))
            down_but.grid(row = 1, column=0, sticky='nswe')                
            Buttons[1].append(down_but)
                                           
            Units.append(unit_label)
            unit_label.grid(row = 0, column=3, pady= (8,5), padx=10, sticky='nwes')
        
        #change to listU
            symb_label = ct.CTkLabel(master = inp_frame  ,text=var, font=font1, 
                                           fg_color=grey)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
            
            
            #info png        
            pngs['icon-infoo'].configure(size=(40,40))
            info_but = ct.CTkButton(master=inp_frame, text='',
                                    image=pngs['icon-infoo'],
                                    width=30,height= 35 )
            info_but.grid(row = 0, column=5, sticky='nwe', pady = 5, padx=5) 
            

                        
        t_radio =ct.CTkRadioButton(master=self.c_page, text=self.translate('text'),corner_radius=5,
                                              value='T', variable=self.cal_rad2_var)
                                              
        t_radio.grid(row=3, column=0, sticky='nswe', pady=10,padx=10 )
        p_radio =ct.CTkRadioButton(master=self.c_page, text=self.translate('picture'),corner_radius=5,
                                              value='P', variable=self.cal_rad2_var)
        p_radio.grid(row=3, column=1, sticky='nswe', pady=10,padx=10)
        v_radio =ct.CTkRadioButton(master=self.c_page, text=self.translate('video'), corner_radius=5,
                                              value='V', variable=self.cal_rad2_var)
        v_radio.grid(row=3, column=2, sticky='nswe', pady=10,padx=10)

              
        cal_but = ct.CTkButton(master=self.c_page, text=self.translate('calculate'), height=35,
                    command= lambda val =inp, chosen = self.cal_rad_var, 
                    format = self.cal_rad2_var , formula = formula:(self.set_values_check(val,chosen,format, formula)) )
        cal_but.grid(row = 3, column=3, sticky='nwse', pady = 15) 
       
    def set_values_check(self, val, chosen, format, formula):
        format.get()
        values = []
        message = self.translate('are you sure all inputs are right?')
        sound = False
        icon = 'check'
        title = self.translate('save inputs')
        option1 = self.translate('calculate')
        for i in range(len(val)):
            
                if i != chosen.get():
                    try:
                    
                        float(val[i].get())
                        values.append(val[i].get())
                    except:
                        message = self.translate('There is a mistake somewehre')
                        sound = True
                        option1 = None
                        title = self.translate('Misake')
                        icon =  "cancel"                 
                        
                        
                else:
                   values.append(None) 
        

        
        if title == 'save inputs' and self.popup_var.get() ==1:
            self.calculate(val, chosen, format, formula)
        else:
            if self.messagebox(message, icon, [option1], 'center', sound, title):
                self.calculate(val, chosen, format, formula)
                
    def calculate(self, val, chosen, format, formula):
        si_units = []
        if format.get() == 'T':
            self.c1_page.tkraise()
            self.c1_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
            self.c1_page.grid_columnconfigure(0, weight=1)
            self.c1_page.grid_rowconfigure(0, weight=1)
            
            scr_cal = ct.CTkScrollableFrame(master=self.c1_page)
            scr_cal.grid(row=0, column=0, sticky='nswe')
            
            for i in range(len(Units)):
                    if r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'] == Units[i].cget('text'):
                        si_units.append(' ')
                    else:
                        si_units.append(Units[i].cget('text')[0])
                        
            
            labels = [r_formula_json['formula'][f'{formula}']['formula'][0],self.sypmy_solve(formula, chosen)]
            #labels = [ chosen.get(),format.get(),si_units, val[0].get(),val[1].get(),val[2].get()]
            #labels = [ formula,umgestellte fomell ,umgestellete formel mit zahlen, Lösung]
            
            for i, data in enumerate(labels):
                Cal_label = ct.CTkLabel(master=scr_cal, text=data)
                Cal_label.grid(row=i,column=0)
   
            
            #self.algebra?

        elif format.get() == 'F':
            pass
        else :
            pass
    
    def disable_inp(self, inp, formula):
        for i , var in enumerate(inp):
            if int(self.cal_rad_var.get()) == i:
                var.configure(state='disabled')
                var.configure(fg_color=self.colorscale(col_th, .5))
                cal_inp_var[i].set('')
                
            elif r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][i]}"]['value'] == None:
                var.configure(state=NORMAL)
                var.configure(fg_color=col_th)

    def sub(self, si_index, f, i):
        
        if si_index[i] != 0:
            self.si_index[i] -=1

        Unit = r_char_json[f"{r_formula_json['formula'][f'{f}']['values'][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index[i]] + f'{Unit}')
                
    def add(self, si_index, f, i):
           
        if si_index[i]  != 16:
           self.si_index[i]  +=1         

        Unit = r_char_json[f"{r_formula_json['formula'][f'{f}']['values'][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index[i] ] + f'{Unit}')

    def sypmy_solve(self, formula, chosen):
        pass
    
    def messagebox(self, message, icon, options, justify, sound, title):
        mis_win = CTkMessagebox.CTkMessagebox(master= root,message=message, 
                                              icon=icon, 
                                              text_color= ('#1B231A','#DCE4DB'),
                                              button_text_color= ('#1B231A','#DCE4DB'),
                                              cancel_button_color= (red_b),
                                              options=options,
                                              option_1= None,
                                              justify=justify,sound=sound,
                                              title=title,
                                              cancel_button='circle') 

        if mis_win.get() == options[0] and options[0] != None:
            return True
        
    def home(self):
        global sort_but, frame_list
        
        self.user_settings()
        self.Sound_effects('Home')
       
        for child in frame.winfo_children():      
            child.configure(fg_color=menu_col[def_col])
            child.configure(hover_color= menu_h_col[def_col])
        if self.cal_bool:
            del_formula_but.grid_forget()
        
            edit_formula_but.grid_forget()
            add_formula_but.grid(row=0, column=0,pady=10, padx=10)

        self.h_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.h_page.grid_columnconfigure(1, weight=1)
        self.h_page.grid_rowconfigure(1, weight=1)
        self.h_page.tkraise()
        
        
        

        
        sort_but = ct.CTkButton(master=self.h_page, text='',image=self.sort_but_img[self.sorting_var],
                                command=lambda: (self.sorting(r_formula_json,True)),height=40,width=35)
        sort_but.grid(row = 0, column=0, pady =  5, padx=(0,5), sticky='nwe')
        CTkToolTip.CTkToolTip(sort_but,message=self.sort_tip_var)
        
        search_inp = ct.CTkEntry(master=self.h_page, placeholder_text=self.translate('formula'), 
                                    width=100, height=40,  fg_color=col_th, 
                                    placeholder_text_color=text_col, border_width=0,
                                    textvariable=self.search_inp)
        search_inp.grid(row = 0, column=1, pady= 5, columnspan=1, sticky='nwe')
        
        search_inp.bind('<Return>', lambda Event:self.search_formula( Event,self.search_inp.get()))
    
        
        search_but = ct.CTkButton(master=self.h_page, text=self.translate('search'), command=
                                  lambda:(self.search_formula('shit',self.search_inp.get())),
                                        width=100, height=40,text_color= text_col)
        search_but.grid(row = 0, column=2, pady =  5, padx=5, sticky='nwe')
        

        
        self.show_formulas(r_formula_json) 
    
    def show_formulas(self, Formulas:dict):
        
        frame_list = ct.CTkScrollableFrame(self.h_page,fg_color=grey_fram)
        frame_list.grid(row=1,column=0,columnspan=3, sticky='nwes')
        frame_list.grid_columnconfigure(0, weight=1)

        for i, formula in enumerate(Formulas['formula']):
           
            frame_formula = ct.CTkFrame(frame_list,width=250, height=75,fg_color=grey)
            frame_formula.grid(row=i,column=0,pady=5, padx=5, sticky='nswe')
            frame_formula.grid_columnconfigure((0,1), weight=(1))
            frame_formula.grid_columnconfigure(2, weight=(2))

            ct.CTkButton(frame_formula,text=formula,width=85, text_color=text_col,
                         command=lambda k = formula: (self.set_values(k))
                                    ).grid(row=0, column=0, pady = 5, padx=5,sticky='w')
            ct.CTkLabel(frame_formula, text=Formulas['formula'][formula]['formula'][0], 
                                 font=font1).grid(row=0, column=1, pady =8, padx=5,sticky='we')
            
            ct.CTkLabel(frame_formula, text=Formulas['formula'][formula]["category"], 
                                   font=font1).grid(row=0, column=2, pady =8, padx=10,sticky='e')
            ct.CTkLabel(frame_formula, text=Formulas['formula'][formula]["creationdate"], 
                                   font=font1).grid(row=0, column=3, pady =8, padx=10,sticky='e')
    
    def sorting(self, dictionary:dict, bool: bool)-> dict:   
        global r_formula_json, sort_but
        if bool:
            self.sorting_var +=1
        
        if self.sorting_var == 3:
           self.sorting_var = 0
            
        if self.sorting_var == 0:
            #alphabetical
            sorted_data = dict(sorted(dictionary["formula"].items(), key=lambda x: (x[0].lower(), x[0])))
            r_formula_json = {"formula": sorted_data}
            self.sort_tip_var = self.translate('alphabetical')

        elif self.sorting_var == 1:
            #erscheinungsdatum
            sorted_data = dict(sorted(dictionary["formula"].items(), key=lambda x: datetime.strptime(x[1]["creationdate"], "%d.%m.%Y %H:%M")))
            r_formula_json = {"formula": sorted_data}           
            self.sort_tip_var = self.translate('creation date')
            
        elif self.sorting_var == 2:
            #category
            sorted_data = dict(sorted(dictionary["formula"].items(), key=lambda x: x[1]['category'].lower()))
            r_formula_json = {"formula": sorted_data}   
            self.sort_tip_var = self.translate('category')
            
        self.home()
          
    def settings(self):
       
        
        global sound_but,   manuell_th_swi, col_them_menu
        if self.cal_bool:
            del_formula_but.grid_forget()
        
            edit_formula_but.grid_forget()
            add_formula_but.grid(row=0, column=0,pady=10, padx=10)

        self.s_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.s_page.tkraise()
        self.s_page.columnconfigure(1, weight=1)
        
        pngs['speaker_on'].configure(size=(50,50))
        pngs['speaker_off'].configure(size=(50,50))
        
        #border doesent change color for some reason


        sound_slider = ct.CTkSlider(master=self.s_page, command=self.sound_slider,
                                    variable=self.sound_slider_var,from_=0, to=100, number_of_steps=100)
        sound_slider.grid(row = 0, column=1,pady=30, padx=5 ,sticky='nwe')
        
        sound_but = ct.CTkButton(master=self.s_page, text='', width=60, height=60,
                                      fg_color='transparent', hover=True, hover_color=menu_h_col[def_col],
                                      image=pngs['speaker_on'], border_width=2,border_color=menu_col[def_col],
                                      command=lambda bool = self.sound_slider_boo, text_color= text_col,
                                      int = self.sound_slider_var: self.sound_slider((int, bool)))
        sound_but.grid(row = 0, column=0,pady=5, padx=5, sticky='nswe')
        
        if self.sound_slider_var.get() ==0:
            sound_but.configure(image=pngs['speaker_off'])
            sound_but.configure(border_color=del_col[def_col])
        

        #TODO make look better
        #TODO disabled and not better seeable
        
        manuell_th_swi = ct.CTkSwitch(self.s_page,text='Light/Dark-Mode',
                                      text_color= ('#1B231A','#DCE4DB'), variable=self.man_th_var,
                                      command=lambda:(self.mode(self.man_th_var)))
        manuell_th_swi.grid(row = 1, column=1,pady=30, padx=5 ,sticky='nwe')
        if self.auto_th_var.get():
            manuell_th_swi.configure(state='disabled')        
                
        auto_th_swi = ct.CTkSwitch(self.s_page, text=self.translate('get system mode'), 
                                              variable=self.auto_th_var,
                                              text_color=('#1B231A','#DCE4DB'),
                                              command=lambda:(self.auto_thm(self.auto_th_var)))
        auto_th_swi.grid(row = 1, column=0,pady=30, padx=5 ,sticky='nwe')
        
        col_thms = self.color_lang[self.lan_menu_var.get()]
        col_thms[ self.color_lang['English'].index(def_col)]
        col_them_menu = ct.CTkOptionMenu(self.s_page, values=[col_thms[ self.color_lang['English'].index(def_col)]], text_color= text_col)
        
        col_them_menu.grid(row = 2, column=1,pady=30, padx=5 ,sticky='nwe')
       
        CTkScrollableDropdown(col_them_menu, values=col_thms, command=self.update_col,
                              scrollbar=False)

        
        lang_them_menu = ct.CTkOptionMenu(self.s_page,values=['t_l'],variable=self.lan_menu_var,text_color= text_col)
     
        CTkScrollableDropdown(lang_them_menu,values=self.languages)
        lang_them_menu.grid(row = 2, column=0,pady=30, padx=5 ,sticky='nwe')
        
        
        less_popu_box = ct.CTkCheckBox(self.s_page, text=self.translate('Less safty popups'),
                                                   variable=self.popup_var, 
                                                   command=lambda:(self.popup(self.popup_var)))
        less_popu_box.grid(row = 3, column=0,pady=30, padx=5 ,sticky='nwe')
        
        
        
        save_but = ct.CTkButton(self.s_page, text=self.translate('save'), command=self.save_settings,text_color= text_col)
        save_but.grid(row = 5, column=1, sticky='nesw', pady=(4,5), padx=(5,5))

    def auto_thm (self,bool):
        if bool.get() == 1:

            #manuell_th_swi.configure(state='disabled',button_color =grey_disa, fg_color=self.colorscale( col_th, .25) )
            ct.set_appearance_mode('System')
            self.user_json_cp['auto_app'] = True
            
        else:
            #manuell_th_swi.configure(state='Normal',button_color =grey_disa, fg_color=self.colorscale( col_th, .25))
            self.user_json_cp['auto_app'] = False
            if self.man_th_var.get() == 1:
                ct.set_appearance_mode('dark')
            else:
                ct.set_appearance_mode('light')
                                       
    def mode(self, bool):
        if bool.get() ==1:
            ct.set_appearance_mode('dark')
            self.user_json_cp['var_app'] = 'dark'
        else:
            ct.set_appearance_mode('light')
            self.user_json_cp['var_app'] = 'ligth'
    
    def popup(self,bool):
        self.user_json_cp['less_popup'] = bool.get()
        
    def update_col(self, col_change):
        ind = self.color_lang[self.lan_menu_var.get()].index(col_change)
        
        col_change = self.color_lang['English'][ind]
        self.user_json_cp['def_col'] = col_change
        ct.set_default_color_theme(col_change)
        for child in frame.winfo_children():      
            child.configure(fg_color=menu_col[col_change])
            child.configure(hover_color= menu_h_col[col_change])
            
        
        self.settings()
        col_them_menu.set(self.color_lang[self.lan_menu_var.get()][ind])
       
    def sound_slider(self, value):
        
        if type(value) == tuple:
            
            self.sound_slider_boo.set(value= True)

            self.sound_slider_var.set(value=0)
            
            self.user_json_cp['volume'] = (self.sound_slider_boo.get(),int(value[0].get()))

        else:
            self.user_json_cp['volume'] = (self.sound_slider_boo.get(),int(self.sound_slider_var.get()))
           
        
        if self.sound_slider_var.get() <=0 or self.sound_slider_boo.get():
            self.sound_slider_boo.set(value=False)
            sound_but.configure(image=pngs['speaker_off'])
            sound_but.configure(border_color=del_col[def_col])
            sound_but.configure(hover_color=del_h_col[def_col])
        else:
            sound_but.configure(image=pngs['speaker_on'])
            sound_but.configure(border_color=menu_col[def_col])
            sound_but.configure(hover_color=menu_h_col[def_col])
    
    def save_settings(self):

      
        self.user_json_cp['language'] = self.lan_menu_var.get()
        user_json = self.user_json_cp
        
        self.write_json('json_files/user_data.json', user_json)
        self.user_settings()
        self.settings()

    def user_settings(self):
        global less_popu, lang, col_th, def_col,  t_lang,tr_lan, auto_app, var_app, user_json, text_col
        user_json = self.read_json('json_files/user_data.json')
            
        self.user_json_cp = user_json.copy()
        def_col = user_json['def_col']
        if def_col == 'orange':
            text_col = '#2B2B2B'
        else:
            text_col = ('#1B231A','#DCE4DB')
       

        #language_mapping = {
        #'german': dlt.lang.GERMAN,
        #'English': dlt.lang.English,
        #}
        #user_language = user_json.get('language')
        #t_lang = language_mapping.get(user_language.lower())
        t_lang = user_json.get('language')
        self.lan_menu_var.set(t_lang)
        if t_lang != 'English':
            tr_lan = self.read_json('json_files/languages/'+ t_lang +'.json') 
        else:
            tr_lan = []
        for tr in tr_lan:
            self.translater[tr[0]] = tr[1]

                
        self.sound_slider_var.set(value= user_json['volume'][1])
        self.popup_var.set(value= user_json['less_popup'])
        self.auto_th_var.set(value=user_json['auto_app'])
        if user_json['var_app'] == 'dark':
            self.man_th_var.set(value=1)
        else:
            self.man_th_var.set(value=0)
   
            
      
        #
        col_th = main_col[def_col]
        
        if self.auto_th_var.get():
            ct.set_appearance_mode('System')
        else:
            if self.man_th_var.get() == 1:
                ct.set_appearance_mode('dark')
            else:
                ct.set_appearance_mode('light')
                            
        ct.set_default_color_theme(def_col)
    
    def menue_buts(self):
        global  add_formula_but
        #makes formula
        pngs['add-list'].configure(size=(40,40))
        add_formula_but = ct.CTkButton(master=frame, image=pngs['add-list'],
                                       text='', width=60,
                                       height=60, command=self.add_formula_name,
                                       fg_color=menu_col[def_col],hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(add_formula_but, message=self.translate('new formula'))   
        add_formula_but.grid(row=0, column=0,pady=10, padx=10)

        #settings
        pngs['settings'].configure(size=(40,40))
        setting_but = ct.CTkButton(master=frame, image=pngs['settings'],
                                   text='', width=60, height=60,
                                       command= self.settings, fg_color=menu_col[def_col],
                                       hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(setting_but, message=self.translate('settings'))
        setting_but.grid(row=4, column=0,pady=10, padx=10, sticky='nwe')
    
        #home
        pngs['home'].configure(size=(40,40))
        home_but = ct.CTkButton(master=frame, image=pngs['home'],text='', width=60, height=60,
                                   command=lambda: (self.home()), fg_color=menu_col[def_col], hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(home_but, message=self.translate('home'))
        home_but.grid(row=5,column=0,pady=10, sticky='nwe', padx=10)
    
    def zoomed(self):
        pass
          #root.state('zoomed')
    
    def Sound_effects(self, Soundtype:str)->None:
        """"possible Values: Button, Home, Save, Cancle, calc"""
        pass
    
    def run(self):
        
        global r_formula_json, r_char_json, user_json
        r_formula_json = self.read_json('json_files/formula.json')
        r_char_json = self.read_json('json_files/formula_char.json')
                   
        
        self.home()
        
        self.sorting(r_formula_json, False)
        self.menue_buts()
        self.zoomed()
        
        
            
        root.mainloop()

if __name__ == '__main__':
    app = Gui()
    app.run()
