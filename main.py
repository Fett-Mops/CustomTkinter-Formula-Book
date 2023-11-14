from tkinter import *
import customtkinter
from sympy import *
import CTkMessagebox
import CTkToolTip


from PIL import Image, ImageTk
import json
import si_prefix


WIDTH, HEIGHT = int(500), int(500)
appearance = ['System', 'light', 'dark']
color_def = ['green', 'blue','dark-blue']


root = customtkinter.CTk()
root.geometry(f'{WIDTH}'+'x'+f'{HEIGHT}')
root.title('Formelbüchlein')

# Grid configer
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

#colors
red = '#E26579'
red_b = '#D35B58'
red_h = '#C77C78'
main_col ={'green':'#00947D','blue': '#008FBE', 'dark-blue': '#5C84C3'}
menu_col = {'green': '#008180','blue': '#00B1BC', 'dark-blue': '#7764AC'}
menu_h_col = {'green': '#006E7A','blue': '#0073A0', 'dark-blue': '#4E5C9F'}
text_col = '#DCE4DB'
grey='#333333'
d = '#2FA572'
grey_disa = '#61676C'


font1 =("None",13)

frame = customtkinter.CTkFrame(root, width=25)
frame.grid(row = 0,rowspan=2, column=0, sticky='nws', pady=(4,5), padx=(5,5))
frame.grid_rowconfigure(3,weight=1)



class Gui:
    def __init__(self):
        self.cal_bool = False
        self.h_page =  customtkinter.CTkFrame(root, fg_color='transparent')
        self.c_page =  customtkinter.CTkFrame(root, fg_color='transparent')
        self.s_page =  customtkinter.CTkFrame(root, fg_color='transparent')
        self.a_page =  customtkinter.CTkFrame(root, fg_color='transparent')
        self.c1_page =  customtkinter.CTkFrame(root, fg_color='transparent')
        self.si_index = [8 for _ in range(3)]
        self.si_str = si_prefix.SI_PREFIX_UNITS
        self.cal_rad_var = customtkinter.IntVar(value=0)
        self.cal_rad2_var = customtkinter.StringVar(value='T')
        #flasch ist nur für 3 ausgerichtet verbessern!
        self.cal_inp_var = [customtkinter.StringVar(value='') for _ in range(3)]
        self.cal_rad_first = False
        self.toplevell = False
        self.toplevel = None
       
    def add_formula(self, new_frm_name):
        for kid in frame.winfo_children():
            kid.configure(state='disabled')
            kid.configure(fg_color='green')
            
        self.a_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.a_page.grid_columnconfigure([0,1,2], weight=1)
 
           
        self.a_page.grid_rowconfigure(2, weight=1)  
        self.a_page.tkraise()
        
        boxes = []
        name_formula = customtkinter.CTkEntry(master=self.a_page,
                                placeholder_text='Formel Name',
                                fg_color=col_th,border_width=0,
                                placeholder_text_color=text_col,justify='center'
                                )
        name_formula.insert('end',new_frm_name)
        name_formula.grid(row=0, column=0,columnspan=4, sticky='nswe', pady=(0,5))
        
        inp_formula = customtkinter.CTkEntry(master=self.a_page,width=50, height=35,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text='Formel',
                                        placeholder_text_color=text_col)
        inp_formula.grid(row=1, column=0,columnspan=3, sticky='nswe', pady=(0,5))
        
        helpful_frame = customtkinter.CTkFrame(master=self.a_page, fg_color='transparent')
        helpful_frame.grid(row=1, column=3, padx=(5,0),pady=(0,5))
        
        
        info_img = ImageTk.PhotoImage(Image.open("pictures\icon-infoo.png").resize((40,40)))
        info_format_but = customtkinter.CTkButton(master= helpful_frame, height=35, text = '',
                                                  image=info_img, width=10)
        info_format_but.grid(row=0, column=2, padx=(5,0))
        
        
        edit_info_img = ImageTk.PhotoImage(Image.open("pictures\edit-info.png").resize((30,30)))
        edit_info_but = customtkinter.CTkButton(master= helpful_frame, height=35, text = '',
                                                  image=edit_info_img, width=10, command=self.edit_info)
        edit_info_but.grid(row=0, column=1, padx=(5,0))
        
        reload_img =ImageTk.PhotoImage(Image.open("pictures/reload.png").resize((40,40)))
        reload_scr_frame = customtkinter.CTkButton(master=helpful_frame, image=reload_img,width=60, height=35, text = '')
        reload_scr_frame.grid(row=0, column=0)
        
        #scrolable fram
        scr_frame = customtkinter.CTkScrollableFrame(master=self.a_page)
        scr_frame.grid(row=2, column=0, columnspan=4, sticky='nswe')
        scr_frame.grid_columnconfigure(0, weight=1)
        scr_frame.grid_rowconfigure(0, weight=1)   
        
        cal_label = customtkinter.CTkLabel(master=scr_frame,
                                text='ajsdlfkajsdlkf', font=font1)
        cal_label.grid(row=0, column=0, sticky='nswe', padx=5)
        cal_label.grid_columnconfigure(0, weight=1)
        cal_label.grid_rowconfigure(0, weight=1)
        
        
        
        
        number = 5
        for i in range(number):            
            inp_frame = customtkinter.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i+1, column=0, columnspan=4,sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([0,1,2,4], weight=2)

            inp_frame.grid_rowconfigure( [j for j in range(number)], weight=1)  
            
            

            
            add_check_var = [customtkinter.Variable() for _ in range(number)]
            box_x = customtkinter.CTkCheckBox(master=inp_frame,text='', width=5,
                                                corner_radius=5,
                                                variable=add_check_var[i])
            boxes.append(box_x)
            box_x.grid(row=0, column=0, pady=5, padx=(5,0))    
                 
            var_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col)
            var_inp.grid(row = 0, column=1, pady= 5, sticky='nwes')
                                          
            unit_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,)
            unit_inp.grid(row = 0, column=2,  pady= 5, padx=(10,0), sticky='nwes')
        
        #change to listU
            symb_label = customtkinter.CTkLabel(master = inp_frame  ,text='d', font=font1, 
                                           fg_color=grey)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
            
            
            #info   
            
            edit_var_info_but = customtkinter.CTkButton(master=inp_frame,
                                           text='',image=edit_info_img,width=30,height= 35 )
            edit_var_info_but.grid(row = 0, column=5, sticky='nwe', pady = 5, padx=5) 
            
        
        inp_category = customtkinter.CTkEntry(master=self.a_page,
                                         fg_color=col_th, border_width=0, bg_color='transparent',
                                        placeholder_text='Kategory',height=35,
                                        placeholder_text_color=text_col)
        inp_category.grid(row=3, column=0,columnspan=4, sticky='we', pady=5)


        save_but = customtkinter.CTkButton(master=self.a_page, text='Speichern', height=35)
        save_but.grid(row = 4, column=2,columnspan= 2, sticky='nwse') 
        cancle_but = customtkinter.CTkButton(master=self.a_page, text='Cancle', height=35, fg_color=red,hover_color=red_h)
        cancle_but.grid(row = 4, column=0, columnspan= 2,sticky='nwse',padx=(0,5)) 
       
    def edit_info(self):
        
        if self.toplevell:
            self.toplevell = False
        else:
            self.toplevel = customtkinter.CTkToplevel()
            self.toplevel.geometry("400x200")
            self.toplevel.rowconfigure(0, weight=1)
            self.toplevel.columnconfigure(0, weight=1)
            self.attributes("-topmost", True)
            self.toplevell = True
        
        edit_info_win = customtkinter.CTkTextbox(self.toplevel)
        #independent
        edit_info_win.insert('end',r_formula_json['formula']['Uri']['information'])
        edit_info_win.grid(row=0,column=0, sticky='nswe')
        
    def add_formula_name(self):
        frm_name = customtkinter.CTkInputDialog(title='Formel Bennenen', text='Name der Formel eingebend')
        frm_var = frm_name.get_input()
        frm_safe = 'Unbennante Formel'
        if  frm_var!= None:
            if frm_var != '':
                frm_safe = frm_var
            r_formula_json['formula'][frm_safe] = {'search_terms':[],'formula':[[]],'values':[[],[]], 'information': 'insert info'}
            self.add_formula(frm_safe)
                
        

    def remove_formula(self,formula):
        
        rm_message = CTkMessagebox.CTkMessagebox(master= root,message="Bist du sicher das du die Formel: "+ f'{formula}'+" löschen willst?",
                                   justify='right', icon=False,
                                   title='Formel Löschen', option_1='Löschen') 
        rm_comp = customtkinter.CTkCheckBox(master = rm_message, text='Auch komponente löschen')
        rm_comp.place(x=10,y=160)
        
        if rm_message.get() == 'Löschen':
            if rm_comp.get():
                
                #optiation on chatgpt handeling json
                for i, var in enumerate(r_formula_json['formula']):
                    for i in range(len(r_formula_json['formula'][f'{formula}']['values'][0])):
                            if formula != var:
                                if r_formula_json['formula'][f'{formula}']['values'][0][i] in r_formula_json['formula'][var]['values'][0]:
                                    if r_formula_json['formula'][f'{formula}']['values'][1][i] != r_formula_json['formula'][var]['values'][1][i]:
                                        if r_formula_json['formula'][f'{formula}']['values'][1][i] == 0:
                                            print('var rm1',i)

                                            r_char_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                            #with open ('json_files/formula_char.json', 'w') as f:
                                            #    json.dump(r_char_json, f, indent=4)
                                           
                                        else:
                                            
                                            r_con_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                            #with open ('json_files/formula_con.json', 'w') as f:
                                                #json.dump(r_con_json, f, indent=4)
                                            print('con rm1',i)
                                    
                                else:
                                    print('var rm2',i)
                                    if r_formula_json['formula'][f'{formula}']['values'][1][i] == 0:

                                        r_char_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                            #with open ('json_files/formula_char.json', 'w') as f:
                                            #    json.dump(r_char_json, f, indent=4)
                                    else:
                                        print('con rm2',i)
                                        r_con_json.pop(f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}")
                                            
                                        #with open ('json_files/formula_con.json', 'w') as f:
                                            #json.dump(r_con_json, f, indent=4)
                                    
                
            r_formula_json['formula'].pop(formula)
            
            #with open ('json_files/formula.json', 'w') as f:
                #json.dump(r_formula_json, f, indent=4)
            

    
            self.home()

    def search_formula(self):
        pass
   
    def edit_formula(self):
        pass
   
    def set_values(self, formula):

        global unit_label, Buttons, Units, edit_formula_but, del_formula_but
        
        add_formula_but.grid_forget()
        edit_formula_img = ImageTk.PhotoImage(Image.open("pictures/edit-formula.png").resize((50,50)))
        edit_formula_but = customtkinter.CTkButton(master=frame, image=edit_formula_img,text='', width=60,
                                                height=60,fg_color=menu_col[def_col],hover_color=menu_h_col[def_col])
        edit_formula_but.grid(row=1 ,column=0,pady=10, padx=10)
        
        
        #remove formula
        del_formula_img = ImageTk.PhotoImage(Image.open("pictures/remove-formula.png").resize((50,50)))
        del_formula_but = customtkinter.CTkButton(master=frame, image=del_formula_img,text='', width=60,
                                                  height=60, fg_color=red, hover_color=red_h,
                                                  command=lambda formula= formula :self.remove_formula(formula),
                                                 )
        del_formula_but.grid(row = 2, column=0,pady=10, padx=10)     
        self.cal_bool = True
            

        self.c_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.c_page.tkraise()
        self.c_page.grid_columnconfigure([0,1,2], weight=1)        
        self.c_page.grid_rowconfigure(2, weight=1)     
        #label
        label_frame= customtkinter.CTkFrame(master=self.c_page)
        label_frame.grid(row=0, column=0, columnspan=4, sticky='nswe',pady=(0,10))
        
        cal_label = customtkinter.CTkLabel(master=label_frame,
                                text='ajsdlfkajsdlkf', font=font1)
        cal_label.grid(row=1, column=0, sticky='nswe', padx=5)
        cal_label.grid_columnconfigure(0, weight=1)
        cal_label.grid_rowconfigure(0, weight=1)
        
        
        #scrolable fram
        scr_frame = customtkinter.CTkScrollableFrame(master=self.c_page)
        scr_frame.grid(row=2, column=0, columnspan=4, sticky='nswe')
        scr_frame.grid_columnconfigure(0, weight=1)
        scr_frame.grid_rowconfigure(0, weight=1)   
        


        ryd_loop =r_formula_json['formula'][f'{formula}']['formula'][0].replace('*', '').replace('+', '').replace('-', '').replace('=', '').replace('/', '')
        Units, Buttons, inp = [], [[],[]], []
        for i, var in enumerate(ryd_loop)  :            
            inp_frame = customtkinter.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i, column=0, sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([0,1,2,4], weight=2)
           
            inp_frame.grid_rowconfigure([0,1,2,4,5], weight=1)  
     
         
        
            if r_formula_json['formula'][f'{formula}']['values'][1][i] == 1:
                self.cal_inp_var[i].set(r_con_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][1]}"]['value'])
                box_x = customtkinter.CTkRadioButton(master=inp_frame,text='', width=5 , border_color=grey_disa,
                                                       state='disabled',corner_radius=5,)
                box_x.grid(row=0, column=0, pady=5, padx=(5,0))
                var_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=grey_disa,
                                    textvariable=self.cal_inp_var[i],
                                    state='disabled'
                                    )
                                   
                
                unit_label = customtkinter.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                                text= r_con_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'])
            
            else:
                box_x = customtkinter.CTkRadioButton(master=inp_frame,text='', width=5,
                                                     corner_radius=5,
                                                     value=i, variable=self.cal_rad_var,
                                                     command=lambda inp = inp: self.disable_inp(inp, formula))
                box_x.grid(row=0, column=0, pady=5, padx=(5,0))     
                var_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=col_th, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,
                                    textvariable=self.cal_inp_var[i]
                                    )
                unit_label = customtkinter.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                                text= r_char_json[f"{r_formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'])
                        # not functional for more var than three
            if r_formula_json['formula'][f'{formula}']['values'][1].index(0) == i:
                var_inp.configure(state='disabled')
                self.cal_rad_var.set(i)

            var_inp.grid(row = 0, column=1, pady= 5, padx=(5,0), sticky='nwes')
            inp.append(var_inp)

            ud_frame = customtkinter.CTkFrame(master =inp_frame,bg_color='transparent', fg_color=grey)
            ud_frame.grid(column=2, row=0)
        
            ud_img=Image.open("pictures/arrow.png").resize((20,20))
            up_img = ImageTk.PhotoImage(ud_img)
            up_but = customtkinter.CTkButton(master=ud_frame, image=up_img, text='',  width=0, height=0,
                                             hover=False, fg_color=grey,
                                         command=lambda i = i, f = formula: (self.add(self.si_index,f,i)))
            up_but.grid(row = 0, column=0, sticky='nswe')
            Buttons[0].append(up_but)
        
            down_img = ImageTk.PhotoImage(ud_img.rotate(angle=180))
            down_but = customtkinter.CTkButton(master=ud_frame, image=down_img, text='', width=0, height=0,
                                               hover=False, fg_color=grey,
                                               command=lambda i = i, f = formula: (self.sub(self.si_index,f,i)))
            down_but.grid(row = 1, column=0, sticky='nswe')                
            Buttons[1].append(down_but)
                                           
            Units.append(unit_label)
            unit_label.grid(row = 0, column=3, pady= (8,5), padx=10, sticky='nwes')
        
        #change to listU
            symb_label = customtkinter.CTkLabel(master = inp_frame  ,text=var, font=font1, 
                                           fg_color=grey)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
            
            
            #info png        
            info_img = ImageTk.PhotoImage(Image.open("pictures\icon-infoo.png").resize((40,40)))
            info_but = customtkinter.CTkButton(master=inp_frame, 
                                           text='',image=info_img,width=30,height= 35 )
            info_but.grid(row = 0, column=5, sticky='nwe', pady = 5, padx=5) 

                        
        t_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Text',corner_radius=5,
                                              value='T', variable=self.cal_rad2_var)
                                              
        t_radio.grid(row=3, column=0, sticky='nswe', pady=10,padx=10 )
        p_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Foto',corner_radius=5,
                                              value='P', variable=self.cal_rad2_var)
        p_radio.grid(row=3, column=1, sticky='nswe', pady=10,padx=10)
        v_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Video', corner_radius=5,
                                              value='V', variable=self.cal_rad2_var)
        v_radio.grid(row=3, column=2, sticky='nswe', pady=10,padx=10)

              
        cal_but = customtkinter.CTkButton(master=self.c_page, text='Berechnen', height=35,
                    command= lambda val =inp, chosen = self.cal_rad_var, 
                    format = self.cal_rad2_var , formula = formula:(self.set_values_check(val,chosen,format, formula)) )
        cal_but.grid(row = 3, column=3, sticky='nwse', pady = 15) 
       
    def set_values_check(self, val, chosen, format, formula):
        format.get()
        values = []
        message = 'Alles richtig eingegeben?'
        sound = False
        icon = 'check'
        title = 'Inputs Speichern'
        l = 'Berechnen'
        for i in range(len(val)):
            
                if i != chosen.get():
                    try:
                    
                        float(val[i].get())
                        values.append(val[i].get())
                    except:
                        message = 'Es ist ein Fehler aufgetretten'
                        sound = True
                        l = None
                        title = 'Fehler'   
                        icon =  "cancel"                 
                        
                        
                else:
                   values.append(None)     
        mis_win = CTkMessagebox.CTkMessagebox(master= root,message=message, 
                                              icon=icon, option_1=l,
                                              justify='center',sound=sound,
                                              title=title,
                                              cancel_button='circle') 
        if mis_win.get() == 'Berechnen':
            self.calculate(val, chosen, format, formula)
                
    def calculate(self, val, chosen, format, formula):
        si_units = []
        if format.get() == 'T':
            self.c1_page.tkraise()
            self.c1_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
            self.c1_page.grid_columnconfigure(0, weight=1)
            self.c1_page.grid_rowconfigure(0, weight=1)
            
            scr_cal = customtkinter.CTkScrollableFrame(master=self.c1_page)
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
                Cal_label = customtkinter.CTkLabel(master=scr_cal, text=data)
                Cal_label.grid(row=i,column=0)
   
            
            #self.algebra?

        elif format.get() == 'F':
            pass
        else :
            pass
    
    def disable_inp(self, inp, C):
        
        for i , var in enumerate(inp):
            if int(self.cal_rad_var.get()) == i:
                var.configure(state='disabled')

                self.cal_inp_var[i].set('')
            else:
                var.configure(state=NORMAL)

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
        
    def home(self):
        if self.cal_bool:
            del_formula_but.grid_forget()
            edit_formula_but.grid_forget() 
            add_formula_but.grid(row=0, column=0,pady=10, padx=10)
        self.h_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.h_page.grid_columnconfigure(0, weight=1)
        self.h_page.grid_rowconfigure(1, weight=1)
        self.h_page.tkraise()
        
        search_inp = customtkinter.CTkEntry(master=self.h_page, placeholder_text='Formel eingeben', 
                                    width=100, height=35,  fg_color=col_th, 
                                    placeholder_text_color=text_col, border_width=0)
        search_inp.grid(row = 0, column=0, pady= 5, columnspan=1, sticky='nwe')
        
        search_but = customtkinter.CTkButton(master=self.h_page, text='Suchen', command=self.search_formula,
                                        width=100, height=35)
        search_but.grid(row = 0, column=1, pady =  5, padx=5, sticky='nwe')

        frame_list = customtkinter.CTkScrollableFrame(self.h_page)
        frame_list.grid(row=1,column=0,pady=(0,5),columnspan=2, sticky='nwes')
        frame_list.grid_columnconfigure(0, weight=1)



        
        for i, formula in enumerate(r_formula_json['formula']):
           
            frame_formula = customtkinter.CTkFrame(frame_list,width=250, height=75,fg_color=grey)
            frame_formula.grid(row=i,column=0,pady=5, padx=5, sticky='nswe')
            frame_formula.grid_columnconfigure((0,1), weight=(1))
            frame_formula.grid_columnconfigure(2, weight=(2))

            customtkinter.CTkButton(frame_formula,text=formula,width=85, command=lambda k = formula: (self.set_values(k))
                                    ).grid(row=0, column=0, pady = 5, padx=5,sticky='w')
            customtkinter.CTkLabel(frame_formula, text=r_formula_json['formula'][formula]['formula'][0], 
                                 font=font1).grid(row=0, column=1, pady =(0,5), padx=5,sticky='we')
            
            customtkinter.CTkLabel(frame_formula, text=r_formula_json['formula'][formula]["search_terms"][-1:], 
                                   font=font1).grid(row=0, column=2, pady =(0,5), padx=10,sticky='e')
            
    def settings(self):
        if self.cal_bool:
            del_formula_but.grid_forget()
        
            edit_formula_but.grid_forget()
            add_formula_but.grid(row=0, column=0,pady=10, padx=10)


        
        self.s_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.s_page.tkraise()
    
    def user_settings(self):
        global less_popu, lang, col_th, def_col

        def_col = user_json['def_col']
        auto_app = user_json['auto_app']
        var_app = user_json['var_app']
        lang = user_json['language']
        less_popu = user_json['less_popup']
        col_th = main_col[def_col]
        
        if auto_app:
            customtkinter.set_appearance_mode('System')
        else:
            customtkinter.set_appearance_mode(var_app)
            
        customtkinter.set_default_color_theme(def_col)
        
    def run(self):
        global r_formula_json, r_char_json, r_con_json, user_json, add_formula_but
        with open ('json_files/formula.json') as f:
            r_formula_json = json.load(f)
            
        with open ('json_files/formula_char.json') as f:
            r_char_json = json.load(f)
            
        with open ('json_files/formula_con.json') as f:
            r_con_json = json.load(f)
        
        with open ('json_files/user_data.json') as f:
            user_json = json.load(f)
        
        self.user_settings()
            
        self.home()
            

  

#makes formula
        add_formula_img = ImageTk.PhotoImage(Image.open("pictures/add-list.png").resize((50,50)))
        add_formula_but = customtkinter.CTkButton(master=frame, image=add_formula_img,text='', width=60,
                                          height=60,     command=self.add_formula_name,
                                          fg_color=menu_col[def_col],hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(add_formula_but, message='Neue Formel')   
        add_formula_but.grid(row=0, column=0,pady=10, padx=10)


#edits formula





    #settings
        setting_img = ImageTk.PhotoImage(Image.open("pictures/settings.png").resize((50,50)))
        setting_but = customtkinter.CTkButton(master=frame, image=setting_img,text='', width=60, height=60,
                                       command= self.settings, fg_color=menu_col[def_col],
                                       hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(setting_but, message='Einstellungen')   
        setting_but.grid(row=4, column=0,pady=10, padx=10, sticky='nwe')
    
    #home
        home_img = ImageTk.PhotoImage(Image.open("pictures/home.png").resize((50,50)))
        home_but = customtkinter.CTkButton(master=frame, image=home_img,text='', width=60, height=60,
                                   command=lambda: (self.home()), fg_color=menu_col[def_col], hover_color=menu_h_col[def_col])
        CTkToolTip.CTkToolTip(home_but, message='Home')
        home_but.grid(row=5,column=0,pady=10, sticky='nwe', padx=10)
        

        
    #sound_img = ImageTk.PhotoImage(Image.open("pictures/settings.png").resize((50,50)))
    #sound_but = customtkinter.CTkButton(master=root, image=sound_img,text='', width=60, height=60,
    #                                   command=home,)
    #sound_but.grid(row = 0, column=0,pady=5, padx=5)

    #sound_slider = customtkinter.CTkSlider(master=root )
    #sound_slider.grid(row = 0, column=0,pady=5, padx=5)
        

        root.mainloop()

if __name__ == '__main__':
    app = Gui()
    app.run()