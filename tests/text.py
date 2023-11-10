from tkinter import *
import customtkinter

from PIL import Image, ImageTk
import json
import si_prefix
import CTkMessagebox

import darkdetect

WIDTH, HEIGHT = int(500), int(500)

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
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
green ='#2FA572'
green_b ='#00947D'
text_col = '#DCE4DB'
grey='#333333'
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
        self.si_index = 8
        self.si_str = si_prefix.SI_PREFIX_UNITS
        self.cal_rad_var = customtkinter.IntVar(value=0)
        self.cal_rad2_var = customtkinter.StringVar(value='T')
        self.cal_inp_var = [customtkinter.StringVar(value=''), customtkinter.StringVar(value=''),customtkinter.StringVar(value='')]
       
    def add_formula(self):
        global edit_formula_but, del_formula_but

        
        self.a_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.a_page.tkraise()
        self.cal_bool= True
        
        edit_formula_img = ImageTk.PhotoImage(Image.open("pictures/edit-formula.png").resize((50,50)))
        edit_formula_but = customtkinter.CTkButton(master=frame, image=edit_formula_img,text='', width=60,
                                          height=60, )
        edit_formula_but.grid(row=1 ,column=0,pady=10, padx=10)
        
        
        #remove formula
        del_formula_img = ImageTk.PhotoImage(Image.open("pictures/remove-formula.png").resize((50,50)))
        del_formula_but = customtkinter.CTkButton(master=frame, image=del_formula_img,text='', width=60,
                                                  height=60, fg_color=red, hover_color=red_h,
                                                  )
        del_formula_but.grid(row = 2, column=0,pady=10, padx=10)      

    def edit_formula(self):
        pass
    
    def remove_formula(self):
        print(HEIGHT)
    
    def search_formula(self):
        print(5)
    
    def set_values(self, formula):
        global unit_label, Buttons, Units
        

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
        


        ryd_loop =formula_json['formula'][f'{formula}']['formula'].replace('*', '').replace('+', '').replace('-', '').replace('=', '').replace('/', '')
        print(ryd_loop)
        Units, Buttons, inp = [], [[],[]], []

        for i, var in enumerate(ryd_loop)  :            
            inp_frame = customtkinter.CTkFrame(master=scr_frame, fg_color=grey)
            inp_frame.grid(row=i, column=0, sticky='nswe', pady=(0,5))
            inp_frame.grid_columnconfigure([0,1,2,4,5], weight=1)
            inp_frame.grid_rowconfigure([0,1,2,4,5], weight=1)  
            inp_frame.grid_columnconfigure(3, weight=2)
            
           
                
            
              
        
        
            if formula_json['formula'][f'{formula}']['values'][1][i] == 1:
                c_box_x = customtkinter.CTkRadioButton(master=inp_frame,text='', width=5 , border_color=grey_disa,
                                                       state='disabled',corner_radius=5,)
                c_box_x.grid(row=0, column=0, pady=5, padx=(5,0))
                var_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=green, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,
                                    textvariable=self.cal_inp_var[i],
                                    state='disabled')
            
            else:
                box_x = customtkinter.CTkRadioButton(master=inp_frame,text='', width=5,
                                                     corner_radius=5,
                                                     value=i, variable=self.cal_rad_var,
                                                     command=lambda inp = inp: self.disable_inp(inp, Units))
                box_x.grid(row=0, column=0, pady=5, padx=(5,0))     
                var_inp = customtkinter.CTkEntry(master=inp_frame
                                    ,width=50, height=35,  fg_color=green, border_width=0, bg_color='transparent',
                                    placeholder_text_color=text_col,
                                    textvariable=self.cal_inp_var[i])
            
               
                                 


            var_inp.grid(row = 0, column=1, pady= 5, padx=(5,0), sticky='nwes')
            inp.append(var_inp)
            if len(inp) == 1:
                var_inp.configure(state='disabled')
            
                                                     
           
            
            
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
 
 
            unit_label = customtkinter.CTkLabel(master = inp_frame,  font=font1,  fg_color=grey,
                                text= char_json[f"{formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'])
                                           
            Units.append(unit_label)
            
            unit_label.grid(row = 0, column=3, pady= (8,5), padx=10, sticky='nwes')
        
        #change to listU
            symb_label = customtkinter.CTkLabel(master = inp_frame  ,text=var, font=font1, 
                                           fg_color=grey)
            symb_label.grid(row = 0, column=4, pady= (8,5), padx=10, sticky='nwes')
        
            info_but = customtkinter.CTkButton(master=inp_frame, 
                                           text='Info', height=35,  )
            info_but.grid(row = 0, column=5, sticky='nwe', pady = 5) 
                #video radio

                        
        t_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Text',corner_radius=5,
                                              value='T', variable=self.cal_rad2_var)
                                              
        t_radio.grid(row=3, column=0, sticky='nswe', pady=10,padx=10 )
        p_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Foto',corner_radius=5,
                                              value='P', variable=self.cal_rad2_var)
        p_radio.grid(row=3, column=1, sticky='nswe', pady=10,padx=10)
        v_radio =customtkinter.CTkRadioButton(master=self.c_page, text='Video', corner_radius=5,
                                              value='V', variable=self.cal_rad2_var)
        v_radio.grid(row=3, column=2, sticky='nswe', pady=10,padx=10)
        
        Cal_but = customtkinter.CTkButton(master=self.c_page, text='Berechnen', height=35,
                    command= lambda val =inp, chosen = self.cal_rad_var, 
                    format = self.cal_rad2_var , formula = formula:(self.set_values_check(val,chosen,format, formula)) )
        Cal_but.grid(row = 3, column=3, sticky='nwse', pady = 15) 
        
       
    def set_values_check(self, val, chosen, format, formula):
        format.get()
        values = []
        message = 'Alles richtig eingegeben?'
        sound = False
        icon = 'check'
        title = 'Inputs Speichern'
        l = ['Berechnen', 'Abbrechen']
        for i in range(len(val)):
            
                if i != chosen.get():
                    try:
                        int(val[i].get())
                        float(val[i].get())
                        values.append(val[i].get())
                    except:
                        message = 'Es ist ein Fehler aufgetretten'
                        sound = True
                        l[0] = None    
                        title = 'Fehler'   
                        icon =  "cancel"                 
                        
                        
                else:
                   values.append(None)     
        mis_win = CTkMessagebox.CTkMessagebox(master= root,message=message, 
                                              icon=icon, option_1=None, options=l,
                                              justify='center',sound=sound,
                                              title=title) 
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
                
                    if char_json[f"{formula_json['formula'][f'{formula}']['values'][0][i]}"]['unit'] == Units[i].cget('text'):
                        si_units.append('')
                    else:
                        si_units.append(Units[i].cget('text')[0])
                    print(si_units)
            
            #self.algebra?

        elif format.get() == 'F':
            pass
        else :
            pass
    
    def disable_inp(self, inp, C):
        for i , var in enumerate(inp):
            if int(self.cal_rad_var.get()) == i:
                var.configure(state='disabled')
                print(self.cal_inp_var[i].get())
                self.cal_inp_var[i].set( '')
            else:
                var.configure(state=NORMAL)
    #change to list V
    #maby animate
    def sub(self,si_index, f,i):
        
        if si_index != 0:
            self.si_index -=1
        if bool(formula_json['formula'][f'{f}']['values'][1][i]):
            Unit = con_json[f"{formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        else:
            Unit = char_json[f"{formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index] + f'{Unit}')
            
    #change to list V        
    def add(self,si_index, f,  i):
           
        if si_index != 16:
            self.si_index +=1         
        if bool(formula_json['formula'][f'{f}']['values'][1][i]):
            Unit = con_json[f"{formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        else:
            Unit = char_json[f"{formula_json['formula'][f'{f}']['values'][0][i]}"]['unit']
        Units[i].configure(text = self.si_str[self.si_index] + f'{Unit}')
            
    def home(self, formula_json):  
        
       
        if self.cal_bool:
            del_formula_but.grid_forget()
            edit_formula_but.grid_forget() 
        self.h_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.h_page.grid_columnconfigure(0, weight=1)
        self.h_page.grid_rowconfigure(1, weight=1)
        self.h_page.tkraise()
        
        search_inp = customtkinter.CTkEntry(master=self.h_page, placeholder_text='Formel eingeben', 
                                    width=100, height=35,  fg_color=green, 
                                    placeholder_text_color=text_col, border_width=0)
        search_inp.grid(row = 0, column=0, pady= 5, columnspan=1, sticky='nwe')
        
        search_but = customtkinter.CTkButton(master=self.h_page, text='Suchen', command=self.search_formula,
                                        width=100, height=35)
        search_but.grid(row = 0, column=1, pady =  5, padx=5, sticky='nwe')

        frame_list = customtkinter.CTkScrollableFrame(self.h_page)
        frame_list.grid(row=1,column=0,pady=(0,5),columnspan=2, sticky='nwes')
        frame_list.grid_columnconfigure(0, weight=1)



        
        for i, formula in enumerate(formula_json['formula']):
           
            frame_formula = customtkinter.CTkFrame(frame_list,width=250, height=75,fg_color=grey)
            frame_formula.grid(row=i,column=0,pady=5, padx=5, sticky='nswe')
            frame_formula.grid_columnconfigure((0,1), weight=(1))
            frame_formula.grid_columnconfigure(2, weight=(2))

            customtkinter.CTkButton(frame_formula,text=formula,width=85, command=lambda k = formula: (self.set_values(k))
                                    ).grid(row=0, column=0, pady = 5, padx=5,sticky='w')
            customtkinter.CTkLabel(frame_formula, text=formula_json['formula'][formula]['formula'], 
                                 font=font1).grid(row=0, column=1, pady =(0,5), padx=5,sticky='we')
            
            customtkinter.CTkLabel(frame_formula, text=formula_json['formula'][formula]["search_terms"][-1:], 
                                   font=font1).grid(row=0, column=2, pady =(0,5), padx=10,sticky='e')
            
    def settings(self):
        if self.cal_bool:
            del_formula_but.grid_forget()
        
            edit_formula_but.grid_forget()
        self.s_page.grid(row = 0,rowspan=2, column=1, sticky='nesw', pady=(4,5), padx=(5,5))
        self.s_page.tkraise()
    
    def run(self):
        global formula_json, char_json, con_json, add_formula_but
        with open ('json_files/formula.json') as f:
            formula_json = json.load(f)
            
        with open ('json_files/formula_char.json') as f:
            char_json = json.load(f)
            
        with open ('json_files/formula_con.json') as f:
            con_json = json.load(f)
            
        self.home(formula_json)

  

#makes formula
        add_formula_img = ImageTk.PhotoImage(Image.open("pictures/add-list.png").resize((50,50)))
        add_formula_but = customtkinter.CTkButton(master=frame, image=add_formula_img,text='', width=60,
                                          height=60,     command=self.add_formula)
        add_formula_but.grid(row=0, column=0,pady=10, padx=10)


#edits formula





    #settings
        setting_img = ImageTk.PhotoImage(Image.open("pictures/settings.png").resize((50,50)))
        setting_but = customtkinter.CTkButton(master=frame, image=setting_img,text='', width=60, height=60,
                                       command= self.settings)
        setting_but.grid(row=4, column=0,pady=10, padx=10, sticky='nwe')
    
    #home
        home_img = ImageTk.PhotoImage(Image.open("pictures/home.png").resize((50,50)))
        home_but = customtkinter.CTkButton(master=frame, image=home_img,text='', width=60, height=60,
                                   command=lambda: (self.home(formula_json)))
   
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
