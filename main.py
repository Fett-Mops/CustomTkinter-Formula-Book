from tkinter import *
import customtkinter as ct
from sympy import *
import CTkMessagebox
import CTkToolTip
from CTkScrollableDropdown import *

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
#root.state('zoomed')

root.title('Formelbüchlein')

# Grid configer
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

#colors
red = '#E26579'
red_b = '#D35B58'
red_h = '#C77C78'
main_col ={'green':'#00947D','blue': '#008FBE', 'dark-blue': '#5C84C3', 'orange':'#88364C'}
menu_col = {'green': '#008180','blue': '#00B1BC', 'dark-blue': '#7764AC','orange':'#88364C'}
menu_h_col = {'green': '#006E7A','blue': '#0073A0', 'dark-blue': '#4E5C9F','orange':'#88364C'}
del_col = {'green': '#FFA17A','blue': '#AF4079', 'dark-blue': '#C0697D','orange':'#88364C'}
del_h_col = {'green': '#F98383','blue': '#9F5399', 'dark-blue': '#88364C','orange':'#88364C'}
text_col = '#DCE4DB'
grey='#333333'
grey_fram = '#2B2B2B'
d = '#2FA572'
grey_disa = '#61676C'



font1 =("None",13)

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
        self.si_index = [8 for _ in range(3)]
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
        self.sorting_var = -1
        self.sort_tip_var =self.translate('alphabetical')
        self.sort_but_img = [pngs['abc'],pngs['createdate'],pngs['home-category']]
  
    def translate(self, text):
        # ? source=dlt.lang.GERMAN
        # ? tred =mt.translate(text,source, t_lang)
        # ? Create a Translator instance with the desired engine ('mymemory', 'microsoft', etc.)
        # ? translator = Translator(to_lang=t_lang, from_lang='en', provider='mymemory')

        # ? translation = translator.translate(text)
        return text 
    
    def write_json(self, path:str, inp:any)->any:
        with open (path, 'w') as f:
            json.dump(inp, f, indent=4)
    
    def add_formula(self, new_frm_name, first_var):
        # TODO if added not sorted pls change
        for kid in frame.winfo_children():
            kid.configure(state='disabled') 
            kid.configure(fg_color=self.colorscale(col_th, .5))
            
        self.a_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.a_page.grid_columnconfigure([0,1,2], weight=1)
 
           
        self.a_page.grid_rowconfigure(2, weight=1)  
        self.a_page.tkraise()
        
        boxes,  info_index = [], []
        name_formula = ct.CTkEntry(master=self.a_page,
                                placeholder_text=self.translate('formula name'),
                                fg_color=col_th,border_width=0,
                                placeholder_text_color=text_col,justify='center'
                                )
        name_formula.insert('end',new_frm_name)
        name_formula.grid(row=0, column=0,columnspan=4, sticky='nswe', pady=(0,5))
        
        inp_formula = ct.CTkEntry(master=self.a_page,width=50, height=35,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text=self.translate('formula'),
                                        placeholder_text_color=text_col)
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
        

        reload_scr_frame = ct.CTkButton(master=helpful_frame, image=pngs['reload'],width=60, height=35, text = '')
        reload_scr_frame.grid(row=0, column=0)
        
        #scrolable fram
        scr_frame = ct.CTkScrollableFrame(master=self.a_page)
        scr_frame.grid(row=2, column=0, columnspan=4, sticky='nswe')
        scr_frame.grid_columnconfigure(0, weight=1)
        scr_frame.grid_rowconfigure(0, weight=1)   
        
        cal_label = ct.CTkLabel(master=scr_frame,
                                text=self.translate('d'), font=font1)
        cal_label.grid(row=0, column=0, sticky='nswe', padx=5)
        cal_label.grid_columnconfigure(0, weight=1)
        cal_label.grid_rowconfigure(0, weight=1)
        
        information = [[inp_formula],[[],[],[],[]]]        
        number = 3
        for i in range(number):            
            inp_frame = ct.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i+1, column=0, columnspan=4,sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([1,2,3,4,5], weight=2)

            inp_frame.grid_rowconfigure( [j for j in range(number)], weight=1)  
            add_check_var = [ct.Variable() for _ in range(number)]
            box_x = ct.CTkCheckBox(master=inp_frame,text='', width=5,
                                                corner_radius=5,
                                                variable=add_check_var[i])
            boxes.append(box_x)
            box_x.grid(row=0, column=0, pady=5, padx=(10,0))    
                 
            var_inp = ct.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col)
            #var_inp.grid(row = 0, column=1, pady= 5, sticky='nwes')
            

                                          
            unit_inp = ct.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,)
            unit_inp.grid(row = 0, column=2,  pady= 5, padx=(10,0), sticky='nwes')
            
            unit_n_inp = ct.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col)
            unit_n_inp.grid(row = 0, column=3, pady= 5,padx=(5,0), sticky='nwes')
        
        #change to listU
            symb_label = ct.CTkLabel(master = inp_frame  ,text=self.translate('formula'), font=font1, 
                                           fg_color=grey)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
            
            symb_n_inp = ct.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col)
            symb_n_inp.grid(row = 0, column=5, pady= 5, sticky='nwes')
            
            
            #info   
     
            info_index.append(first_var + i)
       
            #Help
            pngs['icon-infoo'].configure(size=(30,30))
            edit_var_info_but = ct.CTkButton(master=inp_frame,
                                           text='' ,
                                           image=pngs['icon-infoo'],width=30,height= 35, 
                                           command=lambda:(self.edit_info(new_frm_name,info_index[i],i)) )
            edit_var_info_but.grid(row = 0, column=6, sticky='nwe', pady = 5, padx=5) 
            information[1][0].append(unit_inp)
            information[1][1].append(unit_n_inp)
            information[1][2].append(symb_n_inp)
            #info box
            information[1][3].append(var_inp)

                
        
        inp_category = ct.CTkEntry(master=self.a_page,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text=self.translate('category'),height=35,
                                        placeholder_text_color=text_col)
        inp_category.grid(row=3, column=0,columnspan=4, sticky='we', pady=5)
        
        information.append(inp_category)

        save_but = ct.CTkButton(master=self.a_page, text=self.translate('save'), height=35,
                                           command= lambda:(self.get_formula(new_frm_name,information)))
        save_but.grid(row = 4, column=2,columnspan= 2, sticky='nwse') 
        
        
        cancle_but = ct.CTkButton(master=self.a_page, text=self.translate('cancle'),
                                             height=35, fg_color=del_col[def_col],hover_color=del_h_col[def_col],
                                             command=lambda:(self.idk_dont_look(self.translate("don't save changes"),
                                                                                None,[self.translate("don't save")],'center', False,self.translate('leaf'), new_frm_name)))
        
        cancle_but.grid(row = 4, column=0, columnspan= 2,sticky='nwse',padx=(0,5)) 
    
    def get_formula(self, new_frm_name, information):
        print( r_formula_json['formula'][new_frm_name])

        #information = [[inp_formula,edit_info_box],[[unit_inp],[unit_n_inp],[symb_n_inp][info_box]],category] 
        print(information[0][0].get())
        print(information[2].get())
        r_formula_json['formula'][new_frm_name]['formula'][0] = information[0][0].get()
        #r_formula_json['formula'][new_frm_name]['information'] = information[0][1].get() 
        r_formula_json['formula'][new_frm_name]['category'] = information[2].get()    
            
        char_len = len(r_char_json)
        # char exept symbol is working
        for  i, var in enumerate(information[1][0]):
            r_formula_json['formula'][new_frm_name]['values'][0].append(char_len+i)
            r_char_json[char_len+i] ={
                            "symbol": 'change Thies',
                            "s_name": "",
                            "value": 0,
                            "unit": var.get(),
                            "u_name": '',
                            "category": information[2].get(),
                            "information": "insert information"}
            r_char_json[char_len+i]['u_name'] = information[1][1][i].get()
            r_char_json[char_len+i]['s_name'] = information[1][2][i].get()
            #r_char_json[char_len+i]['information'] = information[1][3][i].get()

            
        print(r_char_json[char_len])
        print(r_char_json[char_len+1])
        print(r_char_json[char_len+2])
        #print(char_len)
        print(r_formula_json['formula'][new_frm_name])
     

            
            
                
        self.idk_dont_look(self.translate('save chages'), None,[self.translate('save')],
                           'center', False,self.translate('save'),new_frm_name)
    
    def idk_dont_look(self, message, icon, options, justify, sound, title, new_frm_name):
        
        if self.messagebox(message,icon, options, justify, sound, title):
            if title == self.translate('leaf'):
                r_formula_json['formula'].pop(new_frm_name)

            elif title ==  self.translate('save'):
                r_formula_json['formula'][new_frm_name]['creationdate'] = datetime.now().strftime("%d.%m.%Y %H:%M")
                self.write_json('json_files/formula.json',r_formula_json)
                self.write_json('json_files/formula_char.json',r_char_json)
                self.write_json('json_files/formula_con.json',r_con_json)  

            for kid in frame.winfo_children():
                    kid.configure(state='normal') 
                    kid.configure(fg_color=col_th)
            self.home()    
                    
    def open_file(self):
        os.system('start formula_syntax.pdf')
        
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
    
    def edit_info(self, formula, var, i):
        print(i)
        
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
            r_formula_json['formula'][formula]['values'][0].append(var)
            r_char_json[var] ={
                            "symbol": 'change Thies',
                            "s_name": "",
                            "value": 0,
                            "unit": '',
                            "u_name": '',
                            "category": '',
                            "information": "cock " +f'{var}'}
            
            edit_info_win.insert('end',r_char_json[var]['information'])
        else:
            edit_info_win.insert('end',r_formula_json['formula'][formula]['information'])
        save_edit = ct.CTkButton(self.toplevel, text=self.translate('save'))
        save_edit.grid(row=3,column=0, sticky='nswe', padx=5,pady=(0,5))
                
    def add_formula_name(self):
        frm_name = ct.CTkInputDialog(title=self.translate('name formula'), text=self.translate('naming the formula'))
        frm_var = frm_name.get_input()
        frm_safe = self.translate('unnamed formula')
        if  frm_var!= None:
            if frm_var != '':
                frm_safe = frm_var
            else:
                for i in range(len(r_formula_json['formula'])):
                    if i >=1:
                        try: 
                            r_formula_json['formula'][frm_safe +f' {i}' ]
                            print(i)
                        except:                      
                            frm_safe = frm_safe +f' {i}' 
                            print(i)
                
            r_formula_json['formula'][frm_safe] = {'search_terms':[],
                                                   'formula':['',[]],
                                                   'values':[[],[]],
                                                   'information': 'insert info',
                                                   'category' : ''}
            
            self.add_formula(frm_safe, len(r_char_json))
                
    def remove_formula(self,formula):
        
        
        rm_message = CTkMessagebox.CTkMessagebox(master= root,
                        message=self.translate("Bist du sicher das du die Formel: {}{}{} löschen willst?").format("'",formula,"'"),
                        justify='right', icon=False,
                        title=self.translate('delete formula'), option_1=self.translate('delete')) 
        rm_comp = ct.CTkCheckBox(master = rm_message, text=self.translate('also delet components'))
        rm_comp.place(x=10,y=160)
        
        if rm_message.get() == self.translate('delete'):
            if rm_comp.get():
                
                # TODO better way to storey than rewrite the hole thing
                for i, var in enumerate(r_formula_json['formula']):
                    for i in range(len(r_formula_json['formula'][f'{formula}']['values'][0])):
                            if formula != var:
                                if r_formula_json['formula'][f'{formula}']['values'][0][i] in r_formula_json['formula'][var]['values'][0]:
                                    if r_formula_json['formula'][f'{formula}']['values'][1][i] != r_formula_json['formula'][var]['values'][1][i]:
                                        if r_formula_json['formula'][f'{formula}']['values'][1][i] == 0:
                                            print('var rm1',i)

                                            r_char_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                            self.write_json('json_files/formula_char.json',r_char_json)  
                                           
                                        else:
                                            
                                            r_con_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                            self.write_json('json_files/formula_con.json',r_con_json)  
                                            print('con rm1',i)
                                    
                                else:
                                    print('var rm2',i)
                                    if r_formula_json['formula'][f'{formula}']['values'][1][i] == 0:

                                        r_char_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                        self.write_json('json_files/formula_char.json',r_char_json)  
                                    else:
                                        print('con rm2',i)
                                        r_con_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                        self.write_json('json_files/formula_con.json',r_con_json)  
                                    
                
            r_formula_json['formula'].pop(formula)
            self.write_json('json_files/formula.json', r_formula_json)  
            

    
            self.home()

    def search_formula(self):
        pass
   
    def edit_formula(self):
        pass
   
    def set_values(self, formula):

        global unit_label, Buttons, Units, edit_formula_but, del_formula_but
        
        add_formula_but.grid_forget()
        pngs['edit-formula'].configure(size=(40,40))
        edit_formula_but = ct.CTkButton(master=frame, image=pngs['edit-formula'],
                                        text='', width=60, height=60,fg_color=menu_col[def_col],
                                        hover_color=menu_h_col[def_col])
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
        for i, var in enumerate(ryd_loop)  :            
            inp_frame = ct.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i, column=0, sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([0,1,2,4], weight=2)
           
            inp_frame.grid_rowconfigure([0,1,2,4,5], weight=1)  
     
         
        
            if r_formula_json['formula'][f'{formula}']['values'][1][i] == 1:
                cal_inp_var[i].set(r_con_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][1]}"]['value'])
                box_x = ct.CTkRadioButton(master=inp_frame,text='', width=5 , border_color=grey_disa,
                                                       state='disabled',corner_radius=5,)
                box_x.grid(row=0, column=0, pady=5, padx=(5,0))
                var_inp = ct.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=self.colorscale(col_th, 0.5), border_width=0, bg_color='transparent',
                                    placeholder_text_color=grey_disa,
                                    textvariable=cal_inp_var[i],
                                    state='disabled'
                                    )
                                   
                
                unit_label = ct.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                                text= r_con_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'])
            
            else:
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
                                text= self.translate(r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit']))
                        # ! not functional for more var than three
            if r_formula_json['formula'][f'{formula}']['values'][1].index(0) == i:
                var_inp.configure(state='disabled')
                var_inp.configure(fg_color=self.colorscale(col_th,0.5))
                self.cal_rad_var.set(i)

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
            symb_label = ct.CTkLabel(master = inp_frame  ,text=self.translate(var), font=font1, 
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
        v_radio =ct.CTkRadioButton(master=self.c_page, text=self.translate('video...en'), corner_radius=5,
                                              value='V', variable=self.cal_rad2_var)
        v_radio.grid(row=3, column=2, sticky='nswe', pady=10,padx=10)

              
        cal_but = ct.CTkButton(master=self.c_page, text=self.translate('calculata'), height=35,
                    command= lambda val =inp, chosen = self.cal_rad_var, 
                    format = self.cal_rad2_var , formula = formula:(self.set_values_check(val,chosen,format, formula)) )
        cal_but.grid(row = 3, column=3, sticky='nwse', pady = 15) 
       
    def set_values_check(self, val, chosen, format, formula):
        format.get()
        values = []
        message = 'are you sure all inputs are right?'
        sound = False
        icon = 'check'
        title = 'save inputs'
        option1 = 'calucalte'
        for i in range(len(val)):
            
                if i != chosen.get():
                    try:
                    
                        float(val[i].get())
                        values.append(val[i].get())
                    except:
                        message = 'Es ist ein Fehler aufgetretten'
                        sound = True
                        option1 = None
                        title = 'Fehler'   
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
                Cal_label = ct.CTkLabel(master=scr_cal, text=self.translate(data))
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
            elif r_formula_json['formula'][f'{formula}']['values'][1][i] != 1:
                var.configure(state=NORMAL)
                var.configure(fg_color=col_th)

    def sub(self, si_index, f, i):
        
        if si_index[i] != 0:
            self.si_index[i] -=1
        if bool(r_formula_json['formula'][f'{f}']['values'][1][i]):
            Unit = r_con_json[f"{r_formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        else:
            Unit = r_char_json[f"{r_formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index[i]] + f'{Unit}')
                
    def add(self, si_index, f, i):
           
        if si_index[i]  != 16:
           self.si_index[i]  +=1         
        if bool(r_formula_json['formula'][f'{f}']['values'][1][i]):
            Unit = r_con_json[f"{r_formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        else:
            Unit = r_char_json[f"{r_formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index[i] ] + f'{Unit}')

    def sypmy_solve(self, formula, chosen):
        pass
    
    def messagebox(self, message, icon, options, justify, sound, title):
        mis_win = CTkMessagebox.CTkMessagebox(master= root,message=message, 
                                              icon=icon, 
                                              options=options,
                                              option_1= None,
                                              justify=justify,sound=sound,
                                              title=title,
                                              cancel_button='circle') 

        if mis_win.get() == options[0] and options[0] != None:
            return True
        
    def home(self):
        global sort_but
        self.user_settings()
        
       
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
                                command=lambda: (self.sorting(r_formula_json)),height=40,width=35)
        sort_but.grid(row = 0, column=0, pady =  5, padx=(0,5), sticky='nwe')
        CTkToolTip.CTkToolTip(sort_but,message=self.sort_tip_var)
        
        search_inp = ct.CTkEntry(master=self.h_page, placeholder_text=self.translate('idk'), 
                                    width=100, height=40,  fg_color=col_th, 
                                    placeholder_text_color=text_col, border_width=0)
        search_inp.grid(row = 0, column=1, pady= 5, columnspan=1, sticky='nwe')
        
        search_but = ct.CTkButton(master=self.h_page, text=self.translate('search'), command=self.search_formula,
                                        width=100, height=40)
        search_but.grid(row = 0, column=2, pady =  5, padx=5, sticky='nwe')

        frame_list = ct.CTkScrollableFrame(self.h_page,fg_color=grey_fram)
        frame_list.grid(row=1,column=0,columnspan=3, sticky='nwes')
        frame_list.grid_columnconfigure(0, weight=1)

        for i, formula in enumerate(r_formula_json['formula']):
           
            frame_formula = ct.CTkFrame(frame_list,width=250, height=75,fg_color=grey)
            frame_formula.grid(row=i,column=0,pady=5, padx=5, sticky='nswe')
            frame_formula.grid_columnconfigure((0,1), weight=(1))
            frame_formula.grid_columnconfigure(2, weight=(2))

            ct.CTkButton(frame_formula,text=self.translate(formula),width=85, command=lambda k = formula: (self.set_values(k))
                                    ).grid(row=0, column=0, pady = 5, padx=5,sticky='w')
            ct.CTkLabel(frame_formula, text=self.translate(r_formula_json['formula'][formula]['formula'][0]), 
                                 font=font1).grid(row=0, column=1, pady =8, padx=5,sticky='we')
            
            ct.CTkLabel(frame_formula, text=self.translate(r_formula_json['formula'][formula]["category"]), 
                                   font=font1).grid(row=0, column=2, pady =8, padx=10,sticky='e')
            ct.CTkLabel(frame_formula, text=self.translate(r_formula_json['formula'][formula]["creationdate"]), 
                                   font=font1).grid(row=0, column=3, pady =8, padx=10,sticky='e')
    
    def sorting(self, dictionary:dict)-> dict:   
        global r_formula_json, sort_but
        
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
                                      fg_color='transparent', hover=True, hover_color=menu_h_col[def_col]
                                      ,image=pngs['speaker_on'], border_width=2,border_color=menu_col[def_col],
                                      command=lambda bool = self.sound_slider_boo
                                      ,int = self.sound_slider_var: self.sound_slider((int, bool)))
        sound_but.grid(row = 0, column=0,pady=5, padx=5, sticky='nswe')
        
        if self.sound_slider_var.get() ==0:
            sound_but.configure(image=pngs['speaker_off'])
            sound_but.configure(border_color=del_col[def_col])
        

        #TODO make look better
        #TODO disabled and not better seeable
        
        manuell_th_swi = ct.CTkSwitch(self.s_page,text='Light/Dark-Mode',
                                                 variable=self.man_th_var,
                                                 command=lambda:(self.mode(self.man_th_var)))
        manuell_th_swi.grid(row = 1, column=1,pady=30, padx=5 ,sticky='nwe')
        if self.auto_th_var.get():
            manuell_th_swi.configure(state='disabled')        
                
        auto_th_swi = ct.CTkSwitch(self.s_page, text=self.translate('get system mode'), 
                                              variable=self.auto_th_var,
                                              command=lambda:(self.auto_thm(self.auto_th_var)))
        auto_th_swi.grid(row = 1, column=0,pady=30, padx=5 ,sticky='nwe')
        
        col_thms = ['green', 'blue', 'dark-blue', 'orange']
        col_them_menu = ct.CTkOptionMenu(self.s_page,values=[def_col])
        
        col_them_menu.grid(row = 2, column=1,pady=30, padx=5 ,sticky='nwe')
       
        CTkScrollableDropdown(col_them_menu, values=col_thms, command=self.update_col,
                              scrollbar=False)
        g = user_json['language']
        languages =  ['Englisch', 'Deutsch', 'Français']
        lang_them_menu = ct.CTkOptionMenu(self.s_page,values=['t_l'],variable=self.lan_menu_var)
        lang_them_menu.set(g)
        CTkScrollableDropdown(lang_them_menu,values=languages)
        lang_them_menu.grid(row = 2, column=0,pady=30, padx=5 ,sticky='nwe')
        
        
        less_popu_box = ct.CTkCheckBox(self.s_page, text='Less safty popups',
                                                   variable=self.popup_var, 
                                                   command=lambda:(self.popup(self.popup_var)))
        less_popu_box.grid(row = 3, column=0,pady=30, padx=5 ,sticky='nwe')
        
        
        
        save_but = ct.CTkButton(self.s_page, text=self.translate('save'), command=self.save_settings)
        save_but.grid(row = 5, column=1, sticky='nesw', pady=(4,5), padx=(5,5))

    def auto_thm (self,bool):
        if bool.get() == 1:
            manuell_th_swi.configure(state='disabled')
            ct.set_appearance_mode('System')
            self.user_json_cp['auto_app'] = True
            
        else:
            manuell_th_swi.configure(state='Normal')
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

        self.user_json_cp['def_col'] = col_change

        ct.set_default_color_theme(col_change)
        for child in frame.winfo_children():      
            child.configure(fg_color=menu_col[col_change])
            child.configure(hover_color= menu_h_col[col_change])
            
        
        self.settings()
        col_them_menu.set(col_change)
       
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
        
        with open ('json_files/user_data.json', 'w') as f:
            
            json.dump(user_json,f , indent=4)
      
        self.user_settings()
        self.settings()

    def user_settings(self):
        global less_popu, lang, col_th, def_col,  t_lang, auto_app, var_app, user_json
        with open ('json_files/user_data.json') as f:
            user_json = json.load(f)
        self.user_json_cp = user_json.copy()
        def_col = user_json['def_col']
       

        #language_mapping = {
        #'german': dlt.lang.GERMAN,
        #'english': dlt.lang.ENGLISH,
        #}
        #user_language = user_json.get('language')
        #t_lang = language_mapping.get(user_language.lower())
        t_lang = user_json.get('language')
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
        
    def run(self):
        global r_formula_json, r_char_json, r_con_json, user_json
        with open ('json_files/formula.json') as f:
            r_formula_json = json.load(f)
            
        with open ('json_files/formula_char.json') as f:
            r_char_json = json.load(f)
            
        with open ('json_files/formula_con.json') as f:
            r_con_json = json.load(f)
        

        
        self.user_settings()
        self.sorting(r_formula_json)
        self.home()
        self.menue_buts()
        root.mainloop()

if __name__ == '__main__':
    app = Gui()
    app.run()
