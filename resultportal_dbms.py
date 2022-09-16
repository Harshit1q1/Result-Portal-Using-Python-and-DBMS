from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import tkinter as tk
import tkinter.scrolledtext as st
import threading
import time
import os
import pyautogui
import random
from fpdf import FPDF
import cx_Oracle


master = Tk() 
master.title("Nirma University Result Portal")

bg=PhotoImage(file="nirmabackground1.png")
Label(master,image=bg).place(x=0,y=0,relwidth=1,relheight=1)

master.geometry("1080x680+150+10")
master.resizable(False,False)

dbmsuser=input("Enter user/password for dbms (system/harshit) : ")
con=cx_Oracle.connect(dbmsuser)
cursor=con.cursor()

f=open("DBMS.txt","a")
if os.path.getsize("DBMS.txt")==0:
    cursor.execute("create table student(Student_id varchar2(10),Student_name varchar2(40),Department varchar2(40))")
    cursor.execute("create table login(Id varchar2(10),Password varchar2(20),Question varchar2(30),Answer varchar2(20))")
    cursor.execute("create table faculty(Faculty_id varchar2(10),Course_id varchar2(20),Course_name varchar2(40),Faculty_name varchar2(40),Department varchar2(30))")
    cursor.execute("create table result(Student_id varchar2(10),Faculty_id varchar2(10),Course_id varchar2(10),Marks int,Grade varchar2(5))")
    cursor.execute("create table department(Department_id varchar2(15),Faculty_id varchar2(10),Faculty_name varchar2(40),Course_id varchar2(10),Course_name varchar2(30))")
    cursor.execute("create table course(course_id varchar2(10),course_name varchar2(30),credits int)")
    cursor.execute("create table mobile(Id varchar2(10),MobileNo_1 varchar2(10),MobileNo_2 varchar2(10))")
    f.write("DBMS")
f.close()

frame=Frame(master,bg="white")
frame.place(x=340,y=180,height=300,width=400)
bg2=PhotoImage(file="background4.png")


def usertext(event) :

    nentry.delete(0,END)

def loginfocus() :
    
    usertext("<Button>")
    nentry.focus()
  
def create(): 
    
    newWindow = Toplevel(master) 
    newWindow.title("Registration Window") 
    Label(newWindow,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)
    newWindow.geometry("1080x680+150+10")
    newWindow.resizable(False,False)

    n=StringVar()
    p=StringVar()
    q=StringVar()
    r=StringVar()
    s=StringVar()
    t=StringVar()
    u=StringVar()
    m=StringVar()
    d=StringVar()
    w=StringVar()
    c=StringVar()
    m2=StringVar()
    var = IntVar()
        
    def submit():
    
        first=n.get()
        last=p.get()
        id=q.get()
        department=d.get()
        mobile=m.get()
        mobile2=m2.get()
        password=r.get()
        password2=s.get()
        select=w.get()
        answer=u.get()
        position=t.get()
        if(position=="Faculty"):
            course=c.get()
            list=course.split(",")
            tot=0
            cursor.execute("select * from course")
            for row3 in cursor:
                if(row3[0]==list[1].upper()):
                    tot=1
                    break
                    
            tota=0
            cursor.execute("select * from course")
            for row1 in cursor:
                if(row1[1]==list[0].upper()):
                    tota=1
                    break
                    
            total=0
            cursor.execute("select * from course")
            for row2 in cursor:
                if((row2[1]==list[0].upper()) and (row2[0]==list[1].upper())):
                    total=1
                    break
        
        to=0
        cursor.execute("select * from login")
        for row in cursor:
            if(row[0]==id.upper()):
                to=1
                
        total2=0
        cursor.execute("select * from mobile")
        for row in cursor:
            if((row[1]==mobile) or (row[2]==mobile) or (row[1]==mobile2) or (row[2]==mobile2)):
                total2=1

        
        if(id!=""):
            check=id[0]+id[1]+id[2]
        
        if((r.get())!=(s.get())):
            messagebox.showerror('Error','Password mismatch')
        elif(to==1):
            messagebox.showerror('Error','User is already exist')
        elif(((r.get())=="") or ((s.get())=="") or ((n.get())=="") or ((p.get())=="") or ((q.get())=="") or ((t.get())=="You are a-") or ((u.get())=="Answer") or ((u.get())=="") or ((w.get())=="Choose Recovery Question") or ((m.get())=="") or ((d.get())=="Choose your department")):
            messagebox.showerror('Error','All field are required')
        elif(total2==1):
            messagebox.showerror('Error','Mobile number is already registered')
        elif(var.get()!=1):
            messagebox.showerror('Error','Please agree with our terms and condition')
        elif(len((r.get()))<6):
            messagebox.showerror('Error','Password contain at least 6 characters')
        elif(len((q.get()))!=8):
            messagebox.showerror('Error','ID is roll no. so it must be 8 character')
        elif((position=="Faculty") and (course=="")):
            messagebox.showerror('Error','For Faculty Course id and anem is required')
        elif((position=="Faculty") and (check.upper()!="NUF")):
            messagebox.showerror('Error','Faculty Username format is not correct')
        elif((position=="Faculty") and (len(list[1])!=6)):
            messagebox.showerror('Error','Course id must contain 6 characters')
        elif((mobile2!="") and (len((m.get()))!=10)):
            messagebox.showerror('Error','Mobile no must contain 10 digits')
        elif(len((m.get()))!=10):
            messagebox.showerror('Error','Mobile no must contain 10 digits')
        elif((position=="Faculty") and (tot==1) and (list[0].upper()!=row3[1])):
            messagebox.showerror('Error','Your course name is wrong.it must be {}'.format(row3[1]))
        elif((position=="Faculty") and (tota==1) and (list[1].upper()!=row1[0])):
            messagebox.showerror('Error','Your course id is wrong.it must be {}'.format(row1[0]))
        else:
            messagebox.showinfo('Done','You are registered Successfully')
            newWindow.destroy()
            
            if(position=="Student"):
                sql=("insert into student(student_id,student_name,department) values (:1,:2,:3)")
                cursor.execute(sql,(id.upper(),first+" "+last,department))
                con.commit()
            else:
                sql=("insert into faculty(faculty_id,course_id,course_name,faculty_name,department) values (:1,:2,:3,:4,:5)")
                cursor.execute(sql,(id.upper(),list[1].upper(),list[0].upper(),first+" "+last,department))
                con.commit()
                
                index=(depa.index(department)+1)
                
                sql=("insert into department(department_id,Faculty_id,Faculty_name,course_id,course_name) values (:1,:2,:3,:4,:5)")
                cursor.execute(sql,("NUIOT00"+str(index),id.upper(),first+" "+last,list[1].upper(),list[0].upper()))
                con.commit()
                
                if(total==1):
                    of=0
                elif(tot==1):
                    sql=("insert into course(course_id,course_name,credits) values (:1,:2,:3)")
                    cursor.execute(sql,(list[1].upper(),list[0].upper(),row3[2]))
                    con.commit()
                elif(tota==1):
                    sql=("insert into course(course_id,course_name,credits) values (:1,:2,:3)")
                    cursor.execute(sql,(list[1].upper(),list[0].upper(),row1[2]))
                    con.commit()
                else:
                    sql=("insert into course(course_id,course_name,credits) values (:1,:2,:3)")
                    cursor.execute(sql,(list[1].upper(),list[0].upper(),random.randint(3,4)))
                    con.commit()
                    
            if(mobile2!=""):
                sql=("insert into mobile(id,MobileNo_1,MobileNo_2) values (:1,:2,:3)")
                cursor.execute(sql,(id.upper(),mobile,mobile2))
                con.commit()
            else:
                sql=("insert into mobile(id,MobileNo_1,MobileNo_2) values (:1,:2,:3)")
                cursor.execute(sql,(id.upper(),mobile,"NA"))
                con.commit()
            
            sql=("insert into login(id,password,question,answer) values (:1,:2,:3,:4)")
            cursor.execute(sql,(id.upper(),password,select,answer))
            con.commit()
    
    def useranswer(event) :
        
        uentry.delete(0,END)
        
    def useranswer2(event) :
        
        centry.delete(0,END)

    label2 = Label(newWindow,text ="Register Yourself",font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
    label2.place(x=250,y=50,height=50,width=600)

    nlabel = Label(newWindow, text = 'First Name', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    nlabel.place(x=120,y=150,height=35,width=170)
    nentry = Entry(newWindow,textvariable = n, font=("cambria",15,"normal"),bg="white",relief="flat")
    nentry.place(x=310,y=150,height=35,width=190)

    plabel = Label(newWindow, text = 'Last Name', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    plabel.place(x=120,y=200,height=35,width=170)
    pentry = Entry(newWindow, textvariable = p, font=("cambria",15,"normal"),bg="white",relief="flat")
    pentry.place(x=310,y=200,height=35,width=190)
    
    option=["Faculty","Student"]
    t.set("You are a-")
    drop1=OptionMenu(newWindow,t,*option)
    drop1.config(bd=0,font=("calibre",14,"bold"),fg="white",bg="purple",activebackground="white",activeforeground="purple",cursor="hand2")
    drop1.place(x=595,y=150,width=320)
    drop1['menu'].config(font=("cambria",14,"normal"),fg="black",bg="white")

    qlabel = Label(newWindow, text = 'Id', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    qlabel.place(x=120,y=250,height=35,width=170)
    qentry = Entry(newWindow, textvariable = q, font=("cambria",15,"normal"),bg="white",relief="flat")
    qentry.place(x=310,y=250,height=35,width=190)
    
    depa=["Computer","Electrical","Mechanical","Electronics and Communication","Civil","Chemical","Instrumentation and Control"]
    d.set("Choose your department")
    drop1=OptionMenu(newWindow,d,*depa)
    drop1.config(bd=0,font=("calibre",14,"bold"),fg="white",bg="purple",activebackground="white",activeforeground="purple",cursor="hand2")
    drop1.place(x=595,y=200,width=320)
    drop1['menu'].config(font=("cambria",14,"normal"),fg="black",bg="white")
    
    mlabel = Label(newWindow, text = 'Mobile No.1', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    mlabel.place(x=120,y=300,height=35,width=170)
    mentry = Entry(newWindow, textvariable = m, font = ('cambria',15,'normal'),bg="white",relief="flat")
    mentry.place(x=310,y=300,height=35,width=190)
    
    mlabel = Label(newWindow, text = 'Mobile No.2(Optional)', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    mlabel.place(x=550,y=350,height=35,width=210)
    mentry = Entry(newWindow, textvariable = m2, font = ('cambria',15,'normal'),bg="white",relief="flat")
    mentry.place(x=770,y=350,height=35,width=190)
    
    rlabel = Label(newWindow, text = 'Password', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    rlabel.place(x=120,y=350,height=35,width=170)
    rentry = Entry(newWindow, textvariable = r, font = ('cambria',15,'normal'), show = '*')
    rentry.place(x=310,y=350,height=35,width=190)

    slabel = Label(newWindow, text = 'Confirm Password', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    slabel.place(x=120,y=400,height=35,width=185)
    sentry = Entry(newWindow, textvariable = s, font = ('cambria',15,'normal'), show = '*')
    sentry.place(x=310,y=400,height=35,width=190)
    
    option=["Your Primary School Name","Your Favourite Sports Man","Your Favourite Hero","Your Favorite Color"]
    w.set("Choose Recovery Question")
    drop1=OptionMenu(newWindow,w,*option)
    drop1.config(bd=0,font=("calibre",14,"bold"),fg="white",bg="purple",activebackground="white",activeforeground="purple",cursor="hand2")
    drop1.place(x=595,y=250,width=320)
    drop1['menu'].config(font=("cambria",14,"normal"),fg="black",bg="white")

    uentry = Entry(newWindow, textvariable = u, font=("cambria",15,"normal"),bg="white",relief="flat")
    uentry.place(x=660,y=300,height=30,width=190)
    uentry.insert(0,"Answer")
    uentry.bind("<Button>",useranswer)
         
    clabel = Label(newWindow, text = 'Course Name and Id', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    clabel.place(x=550,y=400,height=35,width=210)
    centry = Entry(newWindow, textvariable = c, font = ('cambria',15,'normal'),bg="white",relief="flat")
    centry.place(x=770,y=400,height=35,width=190)
    centry.insert(0,"PSC,2CS402")
    centry.bind("<Button>",useranswer2)
   
    R1 = Radiobutton(newWindow, text="I hereby declare that all information given in this website is true and correct to the \nbest of my knowledge and belief.In case any information given here proves to be\n false or incorrect, I shall be responsible for consequences.", variable=var, value=1, font=("calibre",15,"bold"))
    R1.place(x=120,y=480,height=70,width=840)
       
    btn=Button(newWindow,text='Sign Up',command=submit,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
    btn.place(x=445,y=600,height=45,width=190)

    newWindow.mainloop()
    
def loginvalidate(): 
    
    name=n.get()
    password=p.get()
    
    c=0
    cursor.execute("select * from login")
    for row in cursor:
        if(row[0]==name.upper()):
            c=1
            break
    
    if((name=="") or (password=="")):
        messagebox.showerror('Error','All fields are required')
    elif(len(password)<6):
        messagebox.showerror('Error','Password must contain at least 6 characters')
    elif(len(name)!=8):
        messagebox.showerror('Error','Username must contain exactly 8 character')
    elif(c==0):
        messagebox.showerror('Error','You are not registered')
    elif((password!=row[1]) or (row[0]!=name.upper())):
         messagebox.showerror('Error','Password mismatch')
    else:
        messagebox.showinfo('Done','You are Logged in Successfully')
        
        c=0
        cursor.execute("select * from faculty")
        for row in cursor:
            if(row[0]==name.upper()):
                c=1
                break
                
        def updatemobile():
            newWindow = Toplevel(master)
            newWindow.title("Update Mobile Number")

            bg2=PhotoImage(file="nirmabackground2.png")
            Label(newWindow,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)

            newWindow.geometry("1080x680+150+10")
            newWindow.resizable(False,False)
                    
            n=StringVar()
            x=StringVar()
            y=StringVar()
            
            def submit():
           
                password=x.get()
                password2=y.get()
                
                total2=0
                tot=0
                cursor.execute("select * from mobile")
                for row in cursor:
                    if((row[1]==password) or (row[2]==password2) or (row[1]==password) or (row[2]==password2)):
                        if(row[0]==name.upper()):
                            tot=1
                        else:
                            total2=1

                if((name=="") or (password=="")):
                    messagebox.showerror('Error','All fields are required')
                elif(total2==1):
                    messagebox.showerror('Error','Mobile No. is already registered with another id')
                elif(tot==1):
                    messagebox.showerror('Error','Mobile No. is already registered with your id')
                elif(len(password)!=10):
                    messagebox.showerror('Error','Mobile Number Must Consist 10 Digits')
                elif((len(password2)!=10) and (password2!="")):
                    messagebox.showerror('Error','Mobile Number Must Consist 10 Digits')
                else:
                    messagebox.showinfo('Done','Your Mobile Number is Updated')
                    newWindow.destroy()
                    
                    if(password2!=""):
                        sql="Update mobile set MobileNo_1= :1,MobileNo_2= :2 where id =:3"
                        cursor.execute(sql,(password,password2,name.upper()))
                        con.commit()
                    else:
                        sql="Update mobile set MobileNo_1= :1 where id =:2"
                        cursor.execute(sql,(password,name.upper()))
                        con.commit()

            label = Label(newWindow,text ="Update Your Mobile No.",font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
            label.place(x=250,y=40,height=50,width=600)

            nlabel = Label(newWindow, text = 'ID', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            nlabel.place(x=360,y=320,height=35,width=170)
            nentry = Entry(newWindow, textvariable = n, font=("cambria",15,"normal"),bg="white",relief="flat")
            nentry.place(x=540,y=320,height=35,width=190)
            nentry.insert(0,name.upper())

            xlabel = Label(newWindow, text = 'Mobile no.1', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            xlabel.place(x=360,y=360,height=35,width=170)
            xentry = Entry(newWindow, textvariable = x, font=("cambria",15,"normal"),bg="#eee",relief="flat")
            xentry.place(x=540,y=360,height=35,width=190)

            ylabel = Label(newWindow, text = 'Mobile no.2(Optional)', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            ylabel.place(x=320,y=400,height=35,width=210)
            yentry = Entry(newWindow, textvariable = y, font=('cambria',15,'normal'))
            yentry.place(x=540,y=400,height=35,width=190)

            btn=Button(newWindow,text='Update',command=submit,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=450,y=500,height=45,width=190)
            
            newWindow.mainloop()
     
        # Result window creation starts from here.
        if(c==0):
            nw = Toplevel(master) 
            nw.title("View your result") 
            nw.attributes('-fullscreen',True)
           
            cursor.execute("select * from student")
            for row in cursor:
                if(row[0]==name.upper()):
                    fn=row[1].capitalize()
                    br=row[2]
                    break
            con.commit()
            
            list=[]
            list2=[]
            list3=[]
            cursor.execute("select * from result")
            for row in cursor:
                if(row[0]==name.upper()):
                    list.append(row[2])
                    list2.append(row[3])
                    list3.append(row[4])
            con.commit()
            
            list4=[]
            list5=[]
            for i in range(5):
                cursor.execute("select * from course")
                for row in cursor:
                    if(row[0]==list[i]):
                        list4.append(row[1])
                        list5.append(row[2]) 
                con.commit()
            
            list6=[]
            list7=[]
            def grade(o,cr):
                if((o>=90) and (o<=100)):
                    list6.append((cr*10))
                elif(o>=80):
                    list6.append((cr*9))
                elif(o>=70):
                    list6.append((cr*8))
                elif(o>=60):
                    list6.append((cr*7))
                elif(o>=50):
                    list6.append((cr*6))
                elif(o>=40):
                    list6.append((cr*5))
                else:
                    list7.append(1)
                    list6.append((cr*4))
            
            Label(nw,text ="\nNirma University,Ahmedabad",font = ('calibre',16,'bold')).pack()
            Label(nw,text ="Programme Name : B.Tech in {} Engineering".format(br),font = ('calibre',16,'bold')).pack()
            Label(nw,text ="Roll No : {}".format(name.upper()),font = ('calibre',16,'bold')).pack()
            Label(nw,text ="Student's Name : {}".format(fn),font = ('calibre',16,'bold')).pack()
            
            Label(nw,text ="-------------------------------------------------------------",font = ('calibre',16)).pack()
            Label(nw,text ="| Semester |  Course  | Name | Marks | Grade |",font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            f=grade(int(list2[0]),int(list5[0]))
            Label(nw,text ="|       4        | {}  | {}  |    {}   |     {}     |".format(list[0],list4[0],list2[0],list3[0]),font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            f=grade(int(list2[1]),int(list5[1]))
            Label(nw,text ="|       4        | {}  |  {}  |    {}   |     {}     |".format(list[1],list4[1],list2[1],list3[1]),font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            f=grade(int(list2[2]),int(list5[2]))
            Label(nw,text ="|       4        | {}  |  {}  |    {}   |     {}     |".format(list[2],list4[2],list2[2],list3[2]),font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            f=grade(int(list2[3]),int(list5[3]))
            Label(nw,text ="|       4        | {}  |  {}  |    {}   |     {}     |".format(list[3],list4[3],list2[3],list3[3]),font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            f=grade(int(list2[4]),int(list5[4]))
            Label(nw,text =" |       4        | {}  | {} |    {}   |     {}     |".format(list[4],list4[4],list2[4],list3[4]),font = ('calibre',16)).pack()
            Label(nw,text ="--------------------------------------------------------------",font = ('calibre',16)).pack()
            Label(nw,text ="Total Score : {}           Your Score : {}".format((sum(list5)*10),sum(list6)),font = ('calibre',16,'bold')).pack()
            if (sum(list7)==0):
                Label(nw,text ="Remark : Congratulations, you are Pass in all Subjects",font = ('calibre',16,'bold')).pack()
                spi=sum(list6)/sum(list5)
                Label(nw,text ="Your SPI : {:.2}".format(spi),font = ('calibre',16,'bold')).pack()
            else:
                Label(nw,text ="Remark : Better luck next time, you are Fail in {} Subject".format(sum(list7)),font = ('calibre',16,'bold')).pack()
                
            def logout():
                messagebox.showinfo("Thank You","Thank you for Visiting!",parent=frame)
                nw.destroy()
                usertext("<Button>")
                
                
            def download():

                def downloadpdf():
                    # pdf creation starts from here
                    pdf=FPDF()
                    pdf.add_page()
                    pdf.image('a4cover.png',0,0,210,0)
                    pdf.set_font('Arial','B',size=16)
                    pdf.set_left_margin(5)

                    pdf.ln(30)
                    pdf.cell(200,10,txt="Nirma University, Ahmedabad",ln=1,align="C")
                    pdf.cell(200,10,txt="Program Name : B.Tech in {} Engineering".format(br),ln=1,align="C")
                    pdf.cell(200,10,txt="Roll No. : {}".format(name.upper()),ln=1,align="C")
                    pdf.cell(200,10,txt="Student Name : {}".format(fn),ln=1,align="C")
                    pdf.cell(200,10,txt="\n-------------------------------------------------------------",ln=1,align="C")
                    pdf.cell(200,10,txt="| Semester |  Course  | Name | Marks | Grade |",ln=1,align="C")
                    pdf.cell(200,10,txt="--------------------------------------------------------------",ln=1,align="C")
                    pdf.set_font('Arial',size=16)
                    f=grade(int(list2[0]),int(list5[0]))
                    pdf.cell(200,10,txt=r"|       4        | {}  | {}  |    {}   |     {}     |".format(list[0],list4[0],list2[0],list3[0]),ln=1,align="C")
                    pdf.cell(200,10,txt="--------------------------------------------------------------",ln=1,align="C")
                    f=grade(int(list2[1]),int(list5[1]))
                    pdf.cell(200,10,txt=r"|       4        | {}  |  {}  |    {}   |     {}     |".format(list[1],list4[1],list2[1],list3[1]),ln=1,align="C")
                    pdf.cell(200,10,txt="--------------------------------------------------------------",ln=1,align="C")
                    f=grade(int(list2[2]),int(list5[2]))
                    pdf.cell(200,10,txt=r"|       4        | {}  |  {}  |    {}   |     {}     |".format(list[2],list4[2],list2[2],list3[2]),ln=1,align="C")
                    pdf.cell(200,10,txt="--------------------------------------------------------------",ln=1,align="C")
                    f=grade(int(list2[3]),int(list5[3]))
                    pdf.cell(200,10,txt=r"|       4        | {}  |  {}  |    {}   |     {}     |".format(list[3],list4[3],list2[3],list3[3]),ln=1,align="C")
                    pdf.cell(200,10,txt="--------------------------------------------------------------",ln=1,align="C")
                    f=grade(int(list2[4]),int(list5[4]))
                    pdf.cell(200,10,txt=r"|       4        | {}  | {} |    {}   |     {}     |".format(list[4],list4[4],list2[4],list3[4]),ln=1,align="C")
                    pdf.set_font('Arial','B',size=16)
                    pdf.cell(200,10,txt="--------------------------------------------------------------\n",ln=1,align="C")
                    pdf.cell(200,10,txt="Your Score : {}           Total Score : {}".format((sum(list5)*10),sum(list6)),ln=1,align="C")
                    if (sum(list7)==0) :
                        pdf.cell(200,10,txt="Remark : Congratulations, you are Pass in all Subjects",ln=1,align="C")
                        pdf.cell(200,10,txt="Your SPI : {:.2f}".format(spi),ln=1,align="C")
                    else :
                        pdf.cell(200,10,txt="Remark : Better luck next time, you are Fail in {} Subject".format(sum(list7)),ln=1,align="C")

                    pdf.output('{}_Result.pdf'.format(name.upper()))
                    messagebox.showinfo('Done','{}_Result.pdf is Downloaded!'.format(name.upper()),parent=nw)

                def downloadpng():
                    s=pyautogui.screenshot()
                    s.save(r'{}_Result.png'.format(name.upper()))
                    messagebox.showinfo('Done','{}_Result.png is Downloaded!'.format(name.upper()),parent=nw)

                # execution order
                downloadpng()
                jtrix=messagebox.askquestion('Download','Do you want to download PDF as well?',parent=nw)
                if(jtrix=='yes'):
                    def progressbar_update():
                        lime=threading.Thread(target=downloadpdf)
                        lime.start()
                        # pdf creation takes approx 30 seconds
                        # if we need more time, then increase seconds
                        seconds=25
                        i=0
                        while (i<seconds):
                            time.sleep(1)
                            progress['value']=i*(100/seconds)
                            i+=1
                            temp.update_idletasks()
                            perc='{:.2f}'.format(i*(100/seconds))
                            percent.set(str(perc)+'%')
                        progress['value']=100
                        if (lime.is_alive()):
                            temp.destroy()

                    # new window to display progressbar
                    temp = Toplevel(master) 
                    temp.title("PDF Download")
                    temp.geometry("250x130+570+300")
                    temp.resizable(False,False)

                    percent=StringVar()
                    progress=Progressbar(temp, orient=HORIZONTAL, length=200, mode='determinate')
                    progress.pack(pady=10)
                    percentlabel=Label(temp, textvariable=percent).pack()
                    Button(temp, text='Start Downloading', command=progressbar_update,font=("Helvetica",13,"bold"),fg="white",bg="black",relief="raise").pack(pady=10)

            btn=Button(nw,text='Logout',font=("Inconsolata",20,"bold"),command = logout,fg="white",bg="#555",relief="raise",cursor="hand2")
            btn.place(x=980,y=680,height=35,width=190)
            btn=Button(nw,text='Update Your Mobile No.',font=("Inconsolata",20,"bold"),command = updatemobile,fg="white",bg="#555",relief="raise",cursor="hand2")
            btn.place(x=550,y=680,height=35,width=320)
            btn=Button(nw,text='Download',font=("Inconsolata",20,"bold"),command = download,fg="white",bg="#555",relief="raise",cursor="hand2")
            btn.place(x=250,y=680,height=35,width=190)
            
        else: 
    
            newWindow = Toplevel(master) 
            newWindow.title("Make the result of student") 
            Label(newWindow,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)
            newWindow.geometry("1080x680+150+10")
            newWindow.resizable(False,False)

            n1=StringVar()
            p1=StringVar()
            q=StringVar()
            r=StringVar()
            s=StringVar()
            s1=StringVar()
            
            cursor.execute("select * from faculty")
            for row in cursor:
                if(row[0]==name.upper()):
                    fn=row[3]
                    ci=row[1]
                    cn=row[2]
            
            def grade(o):
                if((o>=90) and (o<=100)):
                    return "A+"
                elif(o>=80):
                    return "A"+" "
                elif(o>=70):
                    return "B+"
                elif(o>=60):
                    return "B"+" "
                elif(o>=50):
                    return "C+"
                elif(o>=40):
                    return "C"+" "
                else:
                    return "D"+" "
                    
            def add():
                
                name2=n1.get()
                mark=p1.get()
                    
                c=0
                cursor.execute("select * from result")
                for row in cursor:
                    if((row[0]==name2.upper()) and (row[2]==ci)):
                        c=1
                        break
                con.commit() 

                error=0
                negativemarks=0
                error1=0
                try:
                    if(int(mark)>100):
                        error=1
                    if(int(mark)<0):
                        negativemarks=1
                except ValueError:
                    error1=1 
              
                if(((n1.get())=="") or ((p1.get())=="")):
                    messagebox.showerror('Error','Student Id and marks are required')
                elif(c==1):
                    messagebox.showerror('Error','You are already entered the marks of {}'.format(name2.upper()))
               
                elif(error==1):
                    messagebox.showerror('Error','Student can have maximum 100 Marks!',parent=newWindow)
                elif(negativemarks==1):
                    messagebox.showerror('Error','Student can not have Negative Marks!',parent=newWindow)
                elif(error1==1):
                    messagebox.showerror('Error','Student marks must be an integer!',parent=newWindow)
                elif(len((n1.get()))!=8):
                    messagebox.showerror('Error','Student Id. must contain 8 character')
                else:
                    messagebox.showinfo('Done','You are added Successfully')
                    gr=grade(int(mark))
                    
                    sql=("insert into result (Student_id,Faculty_id,Course_id,Marks,Grade) values (:1,:2,:3,:4,:5)")
                    cursor.execute(sql,(name2.upper(),name.upper(),ci,mark,gr))
                    con.commit()

            def update():
                
                name2=n1.get()
                mark=p1.get()
                    
                c=0
                cursor.execute("select * from result")
                for row in cursor:
                    if((row[0]==name2.upper()) and (row[2]==ci)):
                        c=1
                        break
                con.commit()
                
                error=0
                negativemarks=0
                error1=0
                try:
                    if(int(mark)>100) :
                        error=1
                    if(int(mark)<0): 
                        negativemarks=1
                except ValueError:
                    error1=1 
                            
                if(((n1.get())=="") or ((p1.get())=="")):
                    messagebox.showerror('Error','Student Id and marks are required')
                elif(c==0):
                    messagebox.showerror('Error','You are not add the marks of {}'.format(name2.upper()))
                elif(error==1):
                    messagebox.showerror('Error','Student can have maximum 100 Marks!',parent=newWindow)
                elif(negativemarks==1):
                    messagebox.showerror('Error','Student can not have Negative Marks!',parent=newWindow)
                elif(error1==1):
                    messagebox.showerror('Error','Student marks must be an integer!',parent=newWindow)
               
                elif(len((n1.get()))!=8):
                    messagebox.showerror('Error','Student Id. must contain 8 character')
                else:
                    messagebox.showinfo('Done','You are updaded Successfully')
                    gr=grade(int(mark))
                    
                    sql="Update result set Marks=:1,Grade=:2 where Student_id=:3 and Course_id=:4"
                    cursor.execute(sql,(mark,gr,name2.upper(),ci))
                    con.commit()
                    
            def delete():
            
                name2=n1.get()
                c=0
                cursor.execute("select * from result")
                for row in cursor:
                    if((row[0]==name2.upper()) and (row[2]==ci)):
                        c=1
                        break
                con.commit()
                            
                if(c==0):
                    messagebox.showerror('Error','You are not add the marks of {}'.format(name2.upper()))
                elif(((n1.get())=="")):
                    messagebox.showerror('Error','Student id is required')
                elif(len((n1.get()))!=8):
                    messagebox.showerror('Error','Student Id. must contain 8 character')
                else:
                    messagebox.showinfo('Done','You are deleted Successfully')
                    sql=("delete from result where Student_id=:1 and Course_id=:2")
                    cursor.execute(sql,(name2.upper(),ci))
                    con.commit()
                    
            def search():
                name2=n1.get()
                c=0
                cursor.execute("select * from result")
                for row in cursor:
                    if((row[0]==name2.upper()) and (row[2]==ci)):
                        c=1
                        break
                con.commit()
                   
                if(c==0):
                    messagebox.showerror('Error','You are not add the marks of {}'.format(name2.upper()))
                elif(((n1.get())=="")):
                    messagebox.showerror('Error','Student id is required')
                elif(len((n1.get()))!=8):
                    messagebox.showerror('Error','Student Id. must contain 8 character')
                else:
                    messagebox.showinfo('Done','{} is found in our database'.format(name2.upper()))
                    pentry.insert(INSERT,row[3])
                    
            def logout():
                messagebox.showinfo("Thank You","Thank you for Visiting!",parent=newWindow)
                newWindow.destroy()
                usertext("<Button>")
                
            def ss():
                marks=q.get()
                choice=r.get()
                
                error=0
                negativemarks=0
                error1=0
                try:
                    if(int(marks)>100):
                        error=1
                    if(int(marks)<0):
                        negativemarks=1
                except ValueError:
                    error1=1 
                    
                if((marks=="") or (choice=="Choose Your option")):
                    messagebox.showerror('Error','Marks and choice are required')
                elif(error==1):
                    messagebox.showerror('Error','Student can have maximum 100 Marks!',parent=newWindow)
                elif(negativemarks==1):
                    messagebox.showerror('Error','Student can not have Negative Marks!',parent=newWindow)
                elif(error1==1):
                    messagebox.showerror('Error','Student marks must be an integer!',parent=newWindow)
                else:
                    messagebox.showinfo('Done','Searching Successful')
                    index=option.index(choice)
                    
                    c=0
                    a="Roll-no. - Marks\n"
                    cursor.execute("select * from result")
                    if(index==0):
                        for row in cursor:
                            if((row[3]>int(marks)) and (row[2]==ci)):
                                a=a+row[0]+" - "+str(row[3])+"\n"
                                c=c+1
                    elif(index==1):
                        for row in cursor:
                            if((row[3]<int(marks)) and (row[2]==ci)):
                                a=a+row[0]+" - "+str(row[3])+"\n"
                                c=c+1
                    else:
                        for row in cursor:
                            if((row[3]==int(marks)) and (row[2]==ci)):
                                a=a+row[0]+" - "+str(row[3])+"\n"
                                c=c+1
                        
                    con.commit()
                        
                    sentry.delete(0,END)
                    s1entry.delete('0.0',END)
                    sentry.insert(INSERT,c)
                    s1entry.insert(INSERT,a)
                    
                    
            label2 = Label(newWindow,text ="Welcome {}".format(fn.capitalize()),font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
            label2.place(x=250,y=100,height=50,width=600)
            
            label2 = Label(newWindow,text ="Add/Delete/Update/Search".format(fn.capitalize()),font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
            label2.place(x=50,y=200,height=50,width=440)

            nlabel = Label(newWindow, text = 'Student Id', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            nlabel.place(x=85,y=300,height=35,width=170)
            nentry = Entry(newWindow,textvariable = n1, font=("cambria",15,"normal"),bg="white",relief="flat")
            nentry.place(x=265,y=300,height=35,width=190)

            plabel = Label(newWindow, text = "Enter "+cn+" Marks", font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            plabel.place(x=75,y=400,height=35,width=180)
            pentry = Entry(newWindow, textvariable = p1, font=("cambria",15,"normal"),bg="white",relief="flat")
            pentry.place(x=265,y=400,height=35,width=190)
                   
            btn=Button(newWindow,text='Add',command=add,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=85,y=500,height=45,width=170)
            
            btn=Button(newWindow,text='Update',command=update,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=285,y=500,height=45,width=170)
            
            btn=Button(newWindow,text='Delete',command=delete,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=85,y=600,height=45,width=170)
            
            btn=Button(newWindow,text='Search',command=search,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=285,y=600,height=45,width=170)
            
            label2 = Label(newWindow,text ="Search Student Using marks".format(fn),font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
            label2.place(x=590,y=200,height=50,width=450)
            
            label = Label(newWindow, text = 'Enter Marks', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            label.place(x=625,y=300,height=35,width=170)
            entry = Entry(newWindow,textvariable = q, font=("cambria",15,"normal"),bg="white",relief="flat")
            entry.place(x=805,y=300,height=35,width=190)
                
            option=["Greater than Marks","Less than Marks","Equal to Marks"]
            r.set("Choose Your option")
            drop1=OptionMenu(newWindow,r,*option)
            drop1.config(bd=0,font=("calibre",14,"bold"),fg="white",bg="purple",activebackground="white",activeforeground="purple",cursor="hand2")
            drop1.place(x=660,y=350,width=300)
            drop1['menu'].config(font=("cambria",14,"normal"),fg="black",bg="white")
            
            btn=Button(newWindow,text='Search Students',command=ss,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=685,y=400,height=45,width=250)
                
            slabel = Label(newWindow, text = 'Total Students', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            slabel.place(x=625,y=500,height=35,width=170)
            sentry = Entry(newWindow,textvariable = s, font=("cambria",15,"normal"),bg="white",relief="flat")
            sentry.place(x=805,y=500,height=35,width=190)
                
            s1label = Label(newWindow, text = 'Roll No.', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
            s1label.place(x=625,y=600,height=35,width=170)
            s1entry = st.ScrolledText(newWindow,font=("cambria",15,"normal"),bg="white",relief="flat")
            s1entry.place(x=805,y=600,height=70,width=190)
            
            btn=Button(newWindow,text='Logout',command=logout,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=970,y=10,height=45,width=100)
            
            btn=Button(newWindow,text='Update Your Mobile No.',command=updatemobile,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
            btn.place(x=10,y=10,height=45,width=320)

def change(): 
    
    newWindow = Toplevel(master)
    newWindow.title("Change Password")

    bg2=PhotoImage(file="nirmabackground2.png")
    Label(newWindow,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)

    newWindow.geometry("1080x680+150+10")
    newWindow.resizable(False,False)
            
    n=StringVar()
    x=StringVar()
    y=StringVar()
    
    def submit():
        name=n.get()
        password=x.get()
        password2=y.get()

        if((name=="") or (password=="") or (password2=="")):
            messagebox.showerror('Error','All fields are required')
        elif(len(name)!=8):
            messagebox.showerror('Error','ID must contain exactly 8 character')
        elif(password!=password2):
            messagebox.showerror('Error','Password mismatch')
        elif(len(password)<6):
            messagebox.showerror('Error','Password should contain at least 6 characters')
        else:
            messagebox.showinfo('Done','Your password is changed')
            newWindow.destroy()
            
            sql="Update login set password = :1 where id =:2"
            cursor.execute(sql,(password,name.upper()))
            con.commit()

    label = Label(newWindow,text ="Change Password",font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
    label.place(x=250,y=40,height=50,width=600)

    nlabel = Label(newWindow, text = 'ID', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    nlabel.place(x=360,y=320,height=35,width=170)
    nentry = Entry(newWindow, textvariable = n, font=("cambria",15,"normal"),bg="white",relief="flat")
    nentry.place(x=540,y=320,height=35,width=190)
    nentry.insert(0,gname.upper())

    xlabel = Label(newWindow, text = 'Password', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    xlabel.place(x=360,y=360,height=35,width=170)
    xentry = Entry(newWindow, textvariable = x, font=("cambria",15,"normal"), show='*',bg="#eee",relief="flat")
    xentry.place(x=540,y=360,height=35,width=190)

    ylabel = Label(newWindow, text = 'Confirm Password', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    ylabel.place(x=348,y=400,height=35,width=185)
    yentry = Entry(newWindow, textvariable = y, font=('cambria',15,'normal'), show = '*')
    yentry.place(x=540,y=400,height=35,width=190)

    btn=Button(newWindow,text='Confirm',command=submit,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
    btn.place(x=450,y=500,height=45,width=190)
    
    newWindow.mainloop()
 
def forgot():
    
    newWindow = Toplevel(master)
    newWindow.title("Forgot Password")

    bg2=PhotoImage(file="nirmabackground2.png")
    Label(newWindow,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)

    newWindow.geometry("1080x680+150+10")
    newWindow.resizable(False,False)
    
    n=StringVar()
    t=StringVar()
    u=StringVar()
    
    def submit():
        name=n.get()
        select=t.get()
        password=u.get()
        
        c=0
        cursor.execute("select * from login")
        for row in cursor:
            if(row[0]==name.upper()):
                c=1
                break
        
        if((name=="") or (password=="") or (select=="")):
            messagebox.showerror('Error','All field are required')  
        elif(c==0):
            messagebox.showerror('Error','You are not registered')
            newWindow.destroy()   
        elif((select!=row[2]) or (password!=row[3])):
            messagebox.showerror('Error','Question/Answer mismatch')
        else:
            messagebox.showinfo('Done','You are Log in Successfully')
            newWindow.destroy()
            global gname
            gname=n.get()
            change()
    
    def username(event) :

        nentry.delete(0,END)
       
    def useranswer(event) :

        uentry.delete(0,END)

    label = Label(newWindow,text ="Forgot Password",font=("calibre",25,"bold"),fg="white",bg="#555",anchor="center")
    label.place(x=250,y=40,height=50,width=600)

    nlabel = Label(newWindow, text = 'ID', font=("calibre",15,"bold"),fg="white",bg="purple",anchor="center")
    nlabel.place(x=360,y=320,height=35,width=170)
    nentry = Entry(newWindow, textvariable = n, font=("cambria",15,"normal"),bg="white",relief="flat")
    nentry.place(x=540,y=320,height=35,width=200)
    nentry.insert(0,"19BCE028/NUFCE028")
    nentry.bind("<Button>",username)

    option=["Your Primary School Name","Your Favourite Sports Man","Your Favourite Hero","Your Favorite Color"]
    t.set("Select Recovery Question")
    drop1=OptionMenu(newWindow,t,*option)
    drop1.config(bd=0,font=("calibre",14,"bold"),fg="white",bg="purple",activebackground="white",activeforeground="purple",cursor="hand2")
    drop1.place(x=390,y=375,width=300)
    drop1['menu'].config(font=("cambria",14,"normal"),fg="black",bg="white")

    uentry = Entry(newWindow, textvariable = u, font=("cambria",15,"normal"),bg="white",relief="flat")
    uentry.place(x=450,y=425,height=30,width=190)
    uentry.insert(0,"Answer")
    uentry.bind("<Button>",useranswer)
    
    btn=Button(newWindow,text='Verify Answer',command=submit,font=("Inconsolata",20,"bold"),fg="purple",bg="lightgray",activebackground="black",activeforeground="white")
    btn.place(x=450,y=500,height=45,width=190)
    
    newWindow.mainloop()

label = Label(master,text ="Welcome to Nirma University",font=("calibre",30,"bold"),fg="white",bg="#555",anchor="center")
label.place(x=250,y=50,height=50,width=600)

btn = Button(frame,text ="Sign Up",relief="raise",font=("cambria",15,"bold"),fg="black",bg="white",command = create,activebackground="white",activeforeground="green")
btn.place(x=6,y=8,height=35,width=190)

btn = Button(frame,text ="Log In",relief="raise",font=("cambria",15,"bold"),fg="black",bg="white",command = loginfocus,activebackground="white",activeforeground="green")
btn.place(x=203,y=8,height=35,width=190) 

n=StringVar()
p=StringVar()

nlabel = Label(frame, text = 'Username', font=("cambria",15,"bold"),fg="#d37377",bg="white")
nlabel.place(x=26,y=80,height=35,width=130)
nentry = Entry(frame,textvariable = n, font=("cambria",15,"normal"),bg="#eee",relief="flat")
nentry.place(x=163,y=80,height=35,width=200)
nentry.insert(0,"19BCE028/NUFCE028")
nentry.bind("<Button>",usertext)

plabel = Label(frame, text = 'Password', font=("cambria",15,"bold"),fg="#d37377",bg="white")
plabel.place(x=26,y=130,height=35,width=130)
pentry = Entry(frame, textvariable = p, font=("cambria",15,"normal"), show='*',bg="#eee",relief="flat")
pentry.place(x=163,y=130,height=35,width=200)

btn=Button(frame,text='Login',font=("Inconsolata",20,"bold"),command = loginvalidate,fg="white",bg="#555",relief="raise")
btn.place(x=110,y=195,height=35,width=190)

btn = Button(frame,text ="Forgot Your Password?",font=("cambria",14,"bold","underline"),fg="red",bg="white",command = forgot,relief="flat",activebackground="white") 
btn.place(x=160,y=250,height=30,width=230) 

master.mainloop() 