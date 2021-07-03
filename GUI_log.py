from tkinter import *
##import tkinter.messagebox
import pymysql
import wave
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Activation

from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
from keras.preprocessing import image as image_utils

from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Tk,Label,Canvas,NW,Entry,Button 
from PIL import ImageFile
from tkinter.font import Font
import random
import os,glob
from sklearn import svm
import pickle
from sklearn.neighbors import KNeighborsClassifier
from tkinter import messagebox 
import time
from datetime import datetime as dff
import tkinter as Tkinter
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.constants import CENTER, LEFT, N, E, W, S
from tkinter import StringVar
from tkinter import filedialog
##############
ent_fn,ent_ln,ent_age,ent_email,ent_ph,e_gender,txt_addr,ent_user,ent_pswd,ent_cnfpswd=0,0,0,0,0,0,0,0,0,0

import calendar
import datetime

def calculateAge(birthDate): 
	today = datetime.date.today() 
	age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)) 

	return age 
	
# Driver code
def calcu(a,b,c):
    print(type(a),type(b),type(c),a,b,c)
    print(calculateAge(datetime.date(int(a), int(b), int(c))), "years")
    return calculateAge(datetime.date(int(a), int(b), int(c)))
d1,d2="",""


def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)


class Calendar(ttk.Frame):
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, year=None, month=None, firstweekday=calendar.MONDAY, locale=None, activebackground='#b1dcfb', activeforeground='black', selectbackground='#003eff', selectforeground='white', command=None, borderwidth=1, relief="solid", on_click_month_button=None):
       
        if year is None:
            year = self.datetime.now().year
        
        if month is None:
            month = self.datetime.now().month

        self._selected_date = None

        self._sel_bg = selectbackground 
        self._sel_fg = selectforeground

        self._act_bg = activebackground 
        self._act_fg = activeforeground
        
        self.on_click_month_button = on_click_month_button
        
        self._selection_is_visible = False
        self._command = command

        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)
        
        self.bind("<FocusIn>", lambda event:self.event_generate('<<DatePickerFocusIn>>'))
        self.bind("<FocusOut>", lambda event:self.event_generate('<<DatePickerFocusOut>>'))
    
        self._cal = get_calendar(locale, firstweekday)

        # custom ttk styles
        style = ttk.Style()
        style.layout('L.TButton', (
            [('Button.focus', {'children': [('Button.leftarrow', None)]})]
        ))
        style.layout('R.TButton', (
            [('Button.focus', {'children': [('Button.rightarrow', None)]})]
        ))

        self._font = tkFont.Font()
        
        self._header_var = StringVar()

        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._on_press_left_button)
        lbtn.pack(side=LEFT)
        
        self._header = ttk.Label(hframe, width=15, anchor=CENTER, textvariable=self._header_var)
        self._header.pack(side=LEFT, padx=12)
        
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._on_press_right_button)
        rbtn.pack(side=LEFT)
        hframe.grid(columnspan=7, pady=4)

        self._day_labels = {}

        days_of_the_week = self._cal.formatweekheader(3).split()
 
        for i, day_of_the_week in enumerate(days_of_the_week):
            Tkinter.Label(self, text=day_of_the_week, background='grey90').grid(row=1, column=i, sticky=N+E+W+S)

        for i in range(6):
            for j in range(7):
                self._day_labels[i,j] = label = Tkinter.Label(self, background = "white")
                
                label.grid(row=i+2, column=j, sticky=N+E+W+S)
                label.bind("<Enter>", lambda event: event.widget.configure(background=self._act_bg, foreground=self._act_fg))
                label.bind("<Leave>", lambda event: event.widget.configure(background="white"))

                label.bind("<1>", self._pressed)
        
        # adjust its columns width
        font = tkFont.Font()
        maxwidth = max(font.measure(text) for text in days_of_the_week)
        for i in range(7):
            self.grid_columnconfigure(i, minsize=maxwidth, weight=1)

        self._year = None
        self._month = None

        # insert dates in the currently empty calendar
        self._build_calendar(year, month)

    def _build_calendar(self, year, month):
        if not( self._year == year and self._month == month):
            self._year = year
            self._month = month

            # update header text (Month, YEAR)
            header = self._cal.formatmonthname(year, month, 0)
            self._header_var.set(header.title())

            # update calendar shown dates
            cal = self._cal.monthdayscalendar(year, month)

            for i in range(len(cal)):
                
                week = cal[i] 
                fmt_week = [('%02d' % day) if day else '' for day in week]
                
                for j, day_number in enumerate(fmt_week):
                    self._day_labels[i,j]["text"] = day_number

            if len(cal) < 6:
                for j in range(7):
                    self._day_labels[5,j]["text"] = ""

        if self._selected_date is not None and self._selected_date.year == self._year and self._selected_date.month == self._month:
            self._show_selection()

    def _find_label_coordinates(self, date):
         first_weekday_of_the_month = (date.weekday() - date.day) % 7
         
         return divmod((first_weekday_of_the_month - self._cal.firstweekday)%7 + date.day, 7)
        
    def _show_selection(self):
        """Show a new selection."""

        i,j = self._find_label_coordinates(self._selected_date)

        label = self._day_labels[i,j]

        label.configure(background=self._sel_bg, foreground=self._sel_fg)

        label.unbind("<Enter>")
        label.unbind("<Leave>")
        
        self._selection_is_visible = True
        
    def _clear_selection(self):
        """Show a new selection."""
        i,j = self._find_label_coordinates(self._selected_date)

        label = self._day_labels[i,j]
        label.configure(background= "white", foreground="black")

        label.bind("<Enter>", lambda event: event.widget.configure(background=self._act_bg, foreground=self._act_fg))
        label.bind("<Leave>", lambda event: event.widget.configure(background="white"))

        self._selection_is_visible = False

    # Callback

    def _pressed(self, evt):
        """Clicked somewhere in the calendar."""
        
        text = evt.widget["text"]
        
        if text == "":
            return

        day_number = int(text)

        new_selected_date = dff(self._year, self._month, day_number)
        if self._selected_date != new_selected_date:
            if self._selected_date is not None:
                self._clear_selection()
            
            self._selected_date = new_selected_date
            
            self._show_selection()
        
        if self._command:
            self._command(self._selected_date)

    def _on_press_left_button(self):
        self.prev_month()
        
        if self.on_click_month_button is not None:
            self.on_click_month_button()
    
    def _on_press_right_button(self):
        self.next_month()

        if self.on_click_month_button is not None:
            self.on_click_month_button()
        
    def select_prev_day(self):
        """Updated calendar to show the previous day."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date - self.timedelta(days=1)

        self._build_calendar(self._selected_date.year, self._selected_date.month) # reconstruct calendar

    def select_next_day(self):
        """Update calendar to show the next day."""

        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date + self.timedelta(days=1)

        self._build_calendar(self._selected_date.year, self._selected_date.month) # reconstruct calendar


    def select_prev_week_day(self):
        """Updated calendar to show the previous week."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date - self.timedelta(days=7)

        self._build_calendar(self._selected_date.year, self._selected_date.month) # reconstruct calendar

    def select_next_week_day(self):
        """Update calendar to show the next week."""
        if self._selected_date is None:
            self._selected_date = datetime.datetime(self._year, self._month, 1)
        else:
            self._clear_selection()
            self._selected_date = self._selected_date + self.timedelta(days=7)

        self._build_calendar(self._selected_date.year, self._selected_date.month) # reconstruct calendar

    def select_current_date(self):
        """Update calendar to current date."""
        if self._selection_is_visible: self._clear_selection()

        self._selected_date = datetime.datetime.now()
        self._build_calendar(self._selected_date.year, self._selected_date.month)

    def prev_month(self):
        """Updated calendar to show the previous week."""
        if self._selection_is_visible: self._clear_selection()
        
        date = self.datetime(self._year, self._month, 1) - self.timedelta(days=1)
        self._build_calendar(date.year, date.month) # reconstuct calendar

    def next_month(self):
        """Update calendar to show the next month."""
        if self._selection_is_visible: self._clear_selection()

        date = self.datetime(self._year, self._month, 1) + \
            self.timedelta(days=calendar.monthrange(self._year, self._month)[1] + 1)

        self._build_calendar(date.year, date.month) # reconstuct calendar

    def prev_year(self):
        """Updated calendar to show the previous year."""
        
        if self._selection_is_visible: self._clear_selection()

        self._build_calendar(self._year-1, self._month) # reconstruct calendar

    def next_year(self):
        """Update calendar to show the next year."""
        
        if self._selection_is_visible: self._clear_selection()

        self._build_calendar(self._year+1, self._month) # reconstruct calendar

    def get_selection(self):
        """Return a datetime representing the current selected date."""
        return self._selected_date
        
    selection = get_selection

    def set_selection(self, date):
        """Set the selected date."""
        if self._selected_date is not None and self._selected_date != date:
            self._clear_selection()

        self._selected_date = date

        self._build_calendar(date.year, date.month) # reconstruct calendar


from datetime import date 
  
def numOfDays(date1, date2): 
    return (date2-date1).days

class Datepicker(ttk.Entry):
    def __init__(self, master, entrywidth=None, entrystyle=None, datevar=None, dateformat="%Y-%m-%d", onselect=None, firstweekday=calendar.MONDAY, locale=None, activebackground='#b1dcfb', activeforeground='black', selectbackground='#003eff', selectforeground='white', borderwidth=1, relief="solid"):
        
        if datevar is not None:
            self.date_var = datevar
        else:
            self.date_var = Tkinter.StringVar()

        entry_config = {}
        if entrywidth is not None:
            entry_config["width"] = entrywidth
            
        if entrystyle is not None:
            entry_config["style"] = entrystyle
    
        ttk.Entry.__init__(self, master, textvariable=self.date_var, **entry_config, validate="focusout", validatecommand=self.callback)

        self.date_format = dateformat
        
        self._is_calendar_visible = False
        self._on_select_date_command = onselect

        self.calendar_frame = Calendar(self.winfo_toplevel(), firstweekday=firstweekday, locale=locale, activebackground=activebackground, activeforeground=activeforeground, selectbackground=selectbackground, selectforeground=selectforeground, command=self._on_selected_date, on_click_month_button=lambda: self.focus())

        self.bind_all("<1>", self._on_click, "+")

        self.bind("<FocusOut>", lambda event: self._on_entry_focus_out())
        self.bind("<Escape>", lambda event: self.hide_calendar())
        self.calendar_frame.bind("<<DatePickerFocusOut>>", lambda event: self._on_calendar_focus_out())


        # CTRL + PAGE UP: Move to the previous month.
        self.bind("<Control-Prior>", lambda event: self.calendar_frame.prev_month())
        
        # CTRL + PAGE DOWN: Move to the next month.
        self.bind("<Control-Next>", lambda event: self.calendar_frame.next_month())

        # CTRL + SHIFT + PAGE UP: Move to the previous year.
        self.bind("<Control-Shift-Prior>", lambda event: self.calendar_frame.prev_year())

        # CTRL + SHIFT + PAGE DOWN: Move to the next year.
        self.bind("<Control-Shift-Next>", lambda event: self.calendar_frame.next_year())
        
        # CTRL + LEFT: Move to the previous day.
        self.bind("<Control-Left>", lambda event: self.calendar_frame.select_prev_day())
        
        # CTRL + RIGHT: Move to the next day.
        self.bind("<Control-Right>", lambda event: self.calendar_frame.select_next_day())
        
        # CTRL + UP: Move to the previous week.
        self.bind("<Control-Up>", lambda event: self.calendar_frame.select_prev_week_day())
        
        # CTRL + DOWN: Move to the next week.
        self.bind("<Control-Down>", lambda event: self.calendar_frame.select_next_week_day())

        # CTRL + END: Close the datepicker and erase the date.
        self.bind("<Control-End>", lambda event: self.erase())

        # CTRL + HOME: Move to the current month.
        self.bind("<Control-Home>", lambda event: self.calendar_frame.select_current_date())
        
        # CTRL + SPACE: Show date on calendar
        self.bind("<Control-space>", lambda event: self.show_date_on_calendar())
        
        # CTRL + Return: Set to entry current selection
        self.bind("<Control-Return>", lambda event: self.set_date_from_calendar())

    def callback(self):
        print(self.date_var.get())
        daat=self.date_var.get()
        alist=str(daat).split("-")
        print("alist,",alist)
        ageyear=calcu(alist[0],alist[1],alist[2])
        ent_age.delete(0, 'end')
        ent_age.insert(0,str(ageyear))
        return True
    
    def set_date_from_calendar(self):
        if self.is_calendar_visible:
            selected_date = self.calendar_frame.selection()
            print("---->",selected_date)

            if selected_date is not None:
                self.date_var.set(selected_date.strftime(self.date_format))
                
                if self._on_select_date_command is not None:
                    self._on_select_date_command(selected_date)

            self.hide_calendar()
      
    @property
    def current_text(self):
        return self.date_var.get()
        
    @current_text.setter
    def current_text(self, text):
        return self.date_var.set(text)
        
    @property
    def current_date(self):
        try:
            date = dff.strptime(self.date_var.get(), self.date_format)
            return date
        except ValueError:
            return None
    
    @current_date.setter
    def current_date(self, date):
        self.date_var.set(date.strftime(self.date_format))
        
    @property
    def is_valid_date(self):
        if self.current_date is None:
            return False
        else:
            return True

    def show_date_on_calendar(self):
        date = self.current_date
        if date is not None:
            self.calendar_frame.set_selection(date)

        self.show_calendar()

    def show_calendar(self):
        if not self._is_calendar_visible:
            self.calendar_frame.place(in_=self, relx=0, rely=1)
            self.calendar_frame.lift()

        self._is_calendar_visible = True

    def hide_calendar(self):
        if self._is_calendar_visible:
            self.calendar_frame.place_forget()
        
        self._is_calendar_visible = False

    def erase(self):
        self.hide_calendar()
        self.date_var.set("")
    
    @property
    def is_calendar_visible(self):
        return self._is_calendar_visible

    def _on_entry_focus_out(self):
        if not str(self.focus_get()).startswith(str(self.calendar_frame)):
            self.hide_calendar()
        
    def _on_calendar_focus_out(self):
        if self.focus_get() != self:
            self.hide_calendar()

    def _on_selected_date(self, date1):
        self.date_var.set(date1.strftime(self.date_format))
        print("=---->",date1.strftime(self.date_format))
        global dateval
        global ent_fn,ent_ln,ent_age,ent_email,ent_ph,e_gender,txt_addr,ent_user,ent_pswd
        ageyear=calcu(date1.strftime("%Y"),date1.strftime("%m"),date1.strftime("%d"))
        ent_age.delete(0, 'end')
        ent_age.insert(0,str(ageyear))
        #################
        ##########3######
        dateval=str(date1.strftime(self.date_format))
        global d1,d2
        self.hide_calendar()
        
        if self._on_select_date_command is not None:
            self._on_select_date_command(date1)
        

    def _on_click(self, event):
        str_widget = str(event.widget)

        if str_widget == str(self):
            if not self._is_calendar_visible:
                self.show_date_on_calendar()
        else:
            if not str_widget.startswith(str(self.calendar_frame)) and self._is_calendar_visible:
                self.hide_calendar()



##############

##myFonthead = Font(family="Times New Roman", size=12)
top=0
def back():
    global top
    top.withdraw()
    logg()
def close_window (root): 
    root.destroy()
def password_check(passwd):
      
    SpecialSym =['$', '@', '#', '%']
    ss = "true"
      
    if len(passwd) < 6:
        ss='length should be at least 6'
          
    if len(passwd) > 20:
        ss='length should be not be greater than 20'
          
    if not any(char.isdigit() for char in passwd):
        ss='Password should have at least one numeral'
          
    if not any(char.isupper() for char in passwd):
        ss ='Password should have at least one uppercase letter'
          
    if not any(char.islower() for char in passwd):
        ss = 'Password should have at least one lowercase letter'
          
    if not any(char in SpecialSym for char in passwd):
        ss = 'Password should have at least one of the symbols $@#'
        
    return ss
def agecheck(num):
    print(num)
    if len(num)>2:
        return "Invalid age given"
    elif not num.isdigit():
        return "Invalid age given. String"
    else:
        return "okay"
import re
def isValidPhn(s):
    print("num ",s)
    if(len(s)>11):
        return "Not a valid mobile. Length greater."
    if not s.isdigit():
        return "Not a valid mobile. Strings given."
    return "okay"
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
import re
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def check(email):
    if(re.search(regex,email)):
        print("Valid Email")
        return 0
    else:
        print("Invalid Email")
        return 1
def checkUsername(usr):
        try:
                db=pymysql.connect(host="localhost",user="root",password="",db="birds")
                cursor=db.cursor()
                sql="select username,password from registration where username='%s'"%(usr)
                print (sql)
                try:
                        cursor.execute(sql)
                        res=cursor.fetchall()
                        print ("res",res)
                        print (type(res))
                        print ("length:",len(res))
                        if len(res)==0:
                                return "okay"
                        else:
                                return "Username Already taken"
                except:
                        return "Errors occured"
                db.close()
        except Exception as exx:
                print("Exx: ", exx)
                return "Please connect your Xamp Serverxx"
import numpy as np
mylist=""
def pp(a):
    global mylist
    mylist.insert(END, a)
    

#_________________________________________________function_SAVE_______________________________________________________

def save(e1,e2,e10,e4,e5,e6,e7,e8,e9,cnf):
    global dateval,ent_fn,ent_ln,ent_age,ent_email,ent_ph,e_gender,txt_addr,ent_user,ent_pswd,ent_cnfpswd
    
    e3=dateval
    print (e1,e2,"dob=:",e3,e4,e5,e6,e7,e8,e9)
    if e1=="" or e2=="" or e3=="" or e4=="" or e5=="" or e6=="" or e7=="" or e8=="" or e9=="":
        tkinter.messagebox.showinfo("SUBMIT","Fill All Fields")
    elif cnf!=e9:
        messagebox.showinfo("SUBMIT","Passwords does not match")
    elif hasNumbers(e1):
        messagebox.showinfo("SUBMIT","First name contains digit")
    elif  hasNumbers(e2):
        messagebox.showinfo("SUBMIT","Second name contains digit")
    elif  check(e4)==1:
        messagebox.showinfo("SUBMIT","Invalid email address")
    elif  password_check(e9)!="true":
        messagebox.showinfo("SUBMIT",password_check(e9))
    elif  agecheck(e10)!="okay":
        messagebox.showinfo("SUBMIT",agecheck(e10))
    elif isValidPhn(e5)!="okay":
        messagebox.showinfo("SUBMIT",isValidPhn(e5))
    elif checkUsername(e8)!="okay":
        messagebox.showinfo("SUBMIT",checkUsername(e8))
    else:
        try:
                db=pymysql.connect(host="localhost",user="root",password="",db="birds")
                cursor=db.cursor()
                sql="""insert into registration(first_nm,last_nm,dob,age,email,phno,gender,addr,username,password)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(e1,e2,e3,str(e10),e4,e5,e6,e7,e8,e9)
                print (sql)
                try:
                    cursor.execute(sql)
                    db.commit()
                    print ("inserted")
                    ent_fn.delete(0, 'end')
                    ent_ln.delete(0, 'end')
                    ent_age.delete(0, 'end')
                    ent_email.delete(0, 'end')
                    ent_ph.delete(0, 'end')
                    txt_addr.delete("1.0", 'end')
                    ent_user.delete(0, 'end')
                    ent_pswd.delete(0, 'end')
                    ent_cnfpswd.delete(0, 'end')
                    Datepicker(top).place(x=250,y=250)
                    e_gender.set(None)
                    messagebox.showinfo("SUBMIT","Registration Successful")
                except Exception as e:
                    db.rollback()
                    messagebox.showinfo("SUBMIT","Already Registered. Duplicate Fields found")
                    print ("error",e)
                db.close()
        except:
            messagebox.showinfo("SUBMIT","Please connect your Xamp Server")
               

    
#_________________________________________________SAVE_______________________________________________________
new_top=0
#_________________________________________________function_login_______________________________________________________
import cv2
import numpy as np
import glob
lbl_vdo=0
import tkinter as tk, threading
import imageio
from PIL import Image, ImageTk
import cv2


def login():
    global new_top
    new_top=Toplevel()
    myFont = Font(family="Times New Roman", size=10)
    global top
    top.withdraw()
    image = Image.open("bg.jpg")
    image = image.resize((360, 170), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic = ImageTk.PhotoImage(image)
    lbl_reg=Label(new_top,image=pic)
    lbl_reg.place(x=0,y=0)
    new_top.config(bg="#0bffff")
    new_top.minsize(350,400)
    log_name=StringVar()
    log_pass=StringVar()
    un=log_name.get()
    ps=log_pass.get()
    print ("un",un,"ps",ps)
    print ("..*..")
##
##    l1=Label(new_top,text="EYE HOSPITAL",bg="white",font=myFonthead)
##    l1.place(x=52,y=20)
##    
    usr_nm=Label(new_top,text="USER NAME",font=myFont)
    usr_nm.place(x=15,y=200)
    usr_nm_ent=Entry(new_top,textvariable=log_name,bg="white",width=15,font=myFont)
    usr_nm_ent.place(x=150,y=200)

    usr_pass=Label(new_top,text="PASSWORD",font=myFont)
    usr_pass.place(x=15,y=240)
    usr_pass_ent=Entry(new_top,show="*",textvariable=log_pass,bg="white",width=15,font=myFont)
    usr_pass_ent.place(x=150,y=240)

    btn_login=Button(new_top,text="LOGIN",bg="white",fg="black",font=myFont,relief=RIDGE,command=lambda: check_tb(log_name.get(),log_pass.get()))
    btn_login.place(x=150,y=300)
    btn_login=Button(new_top,text="REGISTER",bg="white",fg="black",font=myFont,relief=RIDGE,command=lambda: logg())
    btn_login.place(x=50,y=300)

    new_top.mainloop()
#_________________________________________________function_check_tb_____________________________________________________9745608293
def user(username):
    global top, lbl_vdo
    print('Home page loaded')
    top=Toplevel()
    top.geometry("750x550")
    top.title("FORM")
    top.minsize(550,460)
    top.config(bg="#ff8201")

    image = Image.open("bg.jpg")
    image = image.resize((750, 550), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic = ImageTk.PhotoImage(image)
    lbl_reg=Label(top,image=pic)
    lbl_reg.place(x=0,y=0)
    lbl_vdo=Label(top)
    lbl_vdo.place(x=200,y=200)

    ''' Button 1'''
    myFont = Font(family="Times New Roman", size=10)
    

    btn3 = Button(top, text = 'CHECK',bg="light yellow",  font=myFont,height=2,width=40,
                 command = lambda:userPred()) 
    btn3.place(x = 220, y = 480)
    btn4 = Button(top, text = 'BACK',bg="light green",  font=myFont,height=1,width=20,
                 command = lambda:back()) 
    btn4.place(x = 550, y = 50)
    thread = threading.Thread(target=stream, args=(lbl_vdo,))
    thread.daemon = 1
    thread.start()
    top.mainloop()
newtop=""

def adminhomepage():
    global top
    print('Home page loaded')
    top=Toplevel()
    top.geometry("750x550")
    top.title("FORM")
    top.minsize(550,460)
    top.config(bg="#ff8201")
    image = Image.open("bg.jpg")
    image = image.resize((1600, 700), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic = ImageTk.PhotoImage(image)
    lbl_reg=Label(top,image=pic,anchor=CENTER)
    lbl_reg.place(x=0,y=0)

    ''' Button 1'''
    myFont = Font(family="Times New Roman", size=10)
    

    btn3 = Button(top, text = 'TRAIN',bg="light yellow",  font=myFont,height=2,width=40,
                 command = lambda:trainSystem() )
    btn3.place(x = 220, y = 350)
    btn4 = Button(top, text = 'LOGOUT',bg="light green",  font=myFont,height=1,width=20,
                 command = lambda:back()) 
    btn4.place(x = 550, y = 50)
    
    top.mainloop()
    
def check_tb(un,ps):
    global d1,d2
    d1="";d2=""
    print (":",un,":",ps)
    if un=="admin" and ps=="admin":
        messagebox.showinfo("login","Welcome Admin")
        global new_top
        new_top.withdraw()
        adminhomepage()
    else:
        db=pymysql.connect(host="localhost",user="root",password="",db="birds")
        cursor=db.cursor()
        sql="select username,password from registration where username='%s'"%(un)
        print (sql)
        try:
            cursor.execute(sql)
            res=cursor.fetchall()
            print ("res",res)
            print (type(res))
            print ("length:",len(res))
            if len(res)==0:
                print ("invalid username/password")
                messagebox.showinfo("login","invalid username/password")
            else:
                for i in res:
                    fname=i[0]
                    fpass=i[1]
                    print ("username",fname,"password",fpass)
                    if fname==un and ps==fpass:
                        print ("sucessfull")
                        messagebox.showinfo("login","Successful")
                        new_top.withdraw()
                        userHome()
    ##                    user(fname)
                    elif int(i[2])==0:
                        print ("invalid username/password")
                        messagebox.showinfo("login","Admin not Approved")
                    else:
                        print ("invalid username/password")
                        messagebox.showinfo("login","invalid username/password")

        except Exception as e:
            print ("Error",e)

root=""

def trainSystem():
        global root
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        #Initialize the CNN
        classifier = Sequential()
        #Convolution and Max pooling
        classifier.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3),padding="same", activation = 'relu'))
        classifier.add(MaxPooling2D(pool_size=(3, 3)))
        classifier.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        classifier.add(Conv2D(64, (3, 3), padding="same"))
        classifier.add(Activation("relu"))
        classifier.add(Conv2D(64, (3, 3), padding="same"))
        classifier.add(Activation("relu"))
        classifier.add(MaxPooling2D(pool_size=(2, 2)))
        classifier.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        classifier.add(Conv2D(128, (3, 3), padding="same"))
        classifier.add(Activation("relu"))
        classifier.add(Conv2D(128, (3, 3), padding="same"))
        classifier.add(Activation("relu"))
        classifier.add(MaxPooling2D(pool_size=(2, 2)))
        classifier.add(Dropout(0.25))

        #Flatten
        classifier.add(Flatten())
        classifier.add(Dense(1024))
        classifier.add(Activation("relu"))
        classifier.add(Dropout(0.5))



        #Full connection
        classifier.add(Dense(128, activation = 'relu'))
        classifier.add(Dense(5, activation = 'softmax'))

        #Compile classifier
        classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

        #Fitting CNN to the images
        train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True) 
        test_datagen = ImageDataGenerator(rescale=1./255)
        training_set = train_datagen.flow_from_directory('./dataset/train', target_size=(128, 128), batch_size=32, class_mode='categorical')
        test_set = test_datagen.flow_from_directory('./dataset/test', target_size=(128, 128), batch_size=32, class_mode='categorical')
        classifier.fit_generator(training_set, steps_per_epoch=400/32, epochs=10, validation_data=test_set, validation_steps = 100/32)

        #save model
        import os
        target_dir = './models/'
        if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        classifier.save('./models/model_25.h5')
        classifier.save_weights('./models/weights_25.h5')
        messagebox.showinfo("train", "Training Completed") 



def userPred():
        global root
        filename =  filedialog.askopenfilename(initialdir = "E:/Projects 2020/Bird Species/",title = "choose your file")
        print("*************************",filename)
        img_width, img_height = 128, 128
        model_path = './models/model_25.h5'
        model_weights_path = './models/weights_25.h5'
        model = load_model(model_path)
        model.load_weights(model_weights_path)
        test_image = Image.open(filename)#BytesIO(response.content))
        test_image = test_image.resize((128,128))  
        test_image = image_utils.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)


        result = model.predict_on_batch(test_image)
        print(result)
        n = np.argmax(result[0])
        if n == 0:
                ans='AFRICAN CROWNED CRANE'        
        elif n == 1:
                ans = 'AFRICAN FIREFINCH'
        elif n == 2:
                ans='INDIAN BUSTARD'        
        elif n == 3:
                ans = 'INDIAN PITTA'       
        elif n == 4:
                ans = 'INDIGO BUNTING'     
        print ("prediction",ans)
        root.after(500, lambda : pp("Loading Image."))
        root.after(500, lambda : pp("Model called."))
        root.after(500, lambda : pp("Result predicted."))
        root.after(500, lambda : pp("Result: "+ans+"."))

  
def userHome():
    global root, mylist
    root = Toplevel()
    root.geometry("1600x700+0+0")
    root.title("BIRD SPECIES")

    image = Image.open("bg.jpg")
    image = image.resize((1600, 700), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic = ImageTk.PhotoImage(image)
    lbl_reg=Label(root,image=pic,anchor=CENTER)
    lbl_reg.place(x=0,y=0)
        
    #------------------TIME--------------
    localtime=time.asctime(time.localtime(time.time()))
    #-----------------INFO TOP------------
    lblinfo = Label(root, font=( 'aria' ,30, 'bold' ),text="USER - BIRD SPECIES",fg="black",bg="white",bd=10,anchor='w')
    lblinfo.place(x=450,y=10)
    lblinfo = Label(root, font=( 'aria' ,20, ),text=localtime,fg="black",bg="white",anchor=W)
    lblinfo.place(x=500,y=80)

    lblin = Label(root, font=( 'aria' ,15, 'bold' ),text="INPUT IMAGE TO PREDICT",fg="black",bg="white",bd=10,anchor='w')
    lblin.place(x=125,y=560)

    btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="CHECK", bg="powder blue", command=lambda:userPred())
    btntrn.place(x=150, y=600)

    def qexit():
        root.destroy()
        logg()
    mylist = Listbox(root,width=70, height=20, bg="#b6fc03" )

    mylist.place( x = 880, y = 200 )



    btnexit=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="LOGOUT", bg="powder blue",command=qexit)
    btnexit.place(x=1000, y=600)


    root.mainloop()


def trial():
    global ent_fn,ent_ln,ent_age,ent_email,ent_ph,e_gender,txt_addr,ent_user,ent_pswd
    e_gender.set(None)
def logg():
    global top
    global ent_fn,ent_ln,ent_age,ent_email,ent_ph,e_gender,txt_addr,ent_user,ent_pswd,ent_cnfpswd
    t=Tk()
    t.withdraw()
    top=Toplevel()
    e_gender=StringVar()
    top.geometry("650x750")
    top.title("BIRD SPECIES")
    top.minsize(650,790)
    top.config(bg="#0bffff")
    myFont = Font(family="Times New Roman", size=10)
    myFonthead = Font(family="Times New Roman", size=10)
    import sys
#################_____________IMAGE_____________#################
    ##reg_img=PhotoImage(file="eye.gif")
    ##lbl_reg=Label(top,image=reg_img,anchor=CENTER)
    ##lbl_reg.pack()
    ##background_image=PhotoImage("dbeyenew.jpg")
    ##background_label = Label(top, image=background_image)
    ##background_label.place(x=0, y=0, relwidth=1, relheight=1)
    image = Image.open("bg.jpg")
    image = image.resize((550, 150), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic = ImageTk.PhotoImage(image)
    lbl_reg=Label(top,image=pic,anchor=CENTER)
    lbl_reg.pack()
    ##image = Image.open()
    ##image = image.resize((550, 650), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    ##pic = ImageTk.PhotoImage(image)
    ##lbl_reg1=Label(top,image=pic,anchor=CENTER)
    ##lbl_reg1.pack()
    #################_____________LABEL-ENTRY-FUNCTION_____________#################
    #First Name
    lbl_fn=Label(top,text="First Name",bg="white",width=15,font=myFont)
    lbl_fn.place(x=30,y=170)
    ent_fn=Entry(top,font="12",width=30,bg="white")
    ent_fn.place(x=250,y=170)
    #Last Name
    lbl_Ln=Label(top,text="Last Name",bg="white",width=15,font=myFont)
    lbl_Ln.place(x=30,y=210)
    ent_ln=Entry(top,font="12",width=30,bg="white")
    ent_ln.place(x=250,y=210)
    #Date of birth
    lbl_dob=Label(top,text="Date Of Birth",bg="white",width=15,font=myFont)
    lbl_dob.place(x=30,y=250)
    ##ent_dob=Entry(top,textvariable=e_dob,font="12",width=10,bg="white")
    ##ent_dob.place(x=250,y=250)
    Datepicker(top).place(x=250,y=250)

    ##image = Image.open("images.png")
    ##image = image.resize((20, 19), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    ##pic1 = ImageTk.PhotoImage(image)
    ##lbl_reg1=Label(top,image=pic,anchor=CENTER)
    ##lbl_reg1.pack()


    ##dob_hint=Button(top,image=pic1,anchor=CENTER,command=lambda:test())
    ##dob_hint.place(x=350,y=250)
    ##ent_dob.insert(0, 'YYYY-DD-MM')

    #Age
    lbl_dob=Label(top,text="Age",bg="white",width=15,font=myFont)
    lbl_dob.place(x=30,y=280)
    ent_age=Entry(top,font="12",width=30,bg="white")
    ent_age.place(x=250,y=280)


    #email
    lbl_email=Label(top,text="Email ID",bg="white",width=15,font=myFont)
    lbl_email.place(x=30,y=320)
    ent_email=Entry(top,font="12",width=30,bg="white")
    ent_email.place(x=250,y=320)
    #ph_no
    lbl_ph=Label(top,text="Phone Number",bg="white",width=15,font=myFont)
    lbl_ph.place(x=30,y=360)
    ent_ph=Entry(top,font="12",width=30,bg="white")
    ent_ph.place(x=250,y=360)
    #gender
    lbl_gender=Label(top,text="Gender",bg="white",width=15,font=myFont)
    lbl_gender.place(x=30,y=400)
    r1=Radiobutton(top,text="MALE",variable=e_gender,value="male",bg="white")
    r1.place(x=250,y=400)
    r2=Radiobutton(top,text="FEMALE",variable=e_gender,value="female",bg="white")
    r2.place(x=380,y=400)
    trial()
    #address
    lbl_addr=Label(top,text="Address",bg="white",width=15,font=myFont)
    lbl_addr.place(x=30,y=440)
    txt_addr=Text(top,font="12",width=30,height=5,bg="white")
    txt_addr.place(x=250,y=440)
    #username
    lbl_user=Label(top,text="Username",bg="white",width=15,font=myFont)
    lbl_user.place(x=30,y=550)
    ent_user=Entry(top,font="12",width=30,bg="white")
    ent_user.place(x=250,y=550)
    #password
    lbl_pswd=Label(top,text="Password",bg="white",width=15,font=myFont)
    lbl_pswd.place(x=30,y=590)
    ent_pswd=Entry(top,show="*",font="12",width=30,bg="white")
    ent_pswd.place(x=250,y=590)
    #confirm
    lbl_pswd=Label(top,text="Confirm Password",bg="white",width=15,font=myFont)
    lbl_pswd.place(x=30,y=640)
    ent_cnfpswd=Entry(top,show="*",font="12",width=30,bg="white")
    ent_cnfpswd.place(x=250,y=640)
    ###Submit
    submit_btn=Button(top,text="SUBMIT",bg="white",fg="black",font=myFont,relief=RIDGE,command=lambda:save(ent_fn.get(),ent_ln.get(),ent_age.get(),ent_email.get(),ent_ph.get(),e_gender.get(),txt_addr.get("1.0",END),ent_user.get(),ent_pswd.get(),ent_cnfpswd.get()))
    submit_btn.place(x=150,y=690)
    ###login
    login_btn=Button(top,text="LOGIN",bg="white",fg="black",font=myFont,relief=RIDGE,command=login)
    login_btn.place(x=300,y=690)

    ############################################################################
    top.mainloop()

logg()
