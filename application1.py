from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("facial recognition system for Indian Railway")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry('1280x720')
window.configure(background='#404040')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#path = "profile.jpg"

#Setting it up


message = tk.Label(window, text="INDIAN RAILWAY TICKET COUNTER" ,bg="white",width=100  ,height=5,font=('times', 25, 'italic bold underline'))

message.place(x=0, y=0)



From= [
"pachora.jn",
"jalgaon.jn",
"Bhusawal.jn"
]
To= [
"pachora.jn",
"jalgaon.jn",
"Bhusawal.jn"
]
Concession=[
"no",
"senior citizen"

]
mxstation = [
"pachora.jnpachora.jn",
"pachora.jnjalgaon.jn",
"pachora.jnBhusawal.jn",
"jalgaon.jnjalgaon.jn",
"jalgaon.jnpachora.jn",
"jalgaon.jnBhusawal.jn",
"Bhusawal.jnBhusawal.jn",
"Bhusawal.jnpachora.jn",
"Bhusawal.jnjalgaon.jn"
]

charge = [10,30,60,10,30,30,10,60,30]

variable1 = tk.StringVar(window)
variable1.set(From[0])


lbl = tk.Label(window, text="select station",width=20  ,height=2 ,bg="#8c8c8c" ,font=('times', 9, ' bold ') )
lbl.place(x=5, y=200)

opt = tk.OptionMenu(window, variable1, *From)
opt.config(width=20, font=('Helvetica', 12))
opt.place(x=240, y=200)

lbl2 = tk.Label(window, text="Going To",width=20 ,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl2.place(x=550, y=200)
variable2 = tk.StringVar(window)
variable2.set(To[0])

opt = tk.OptionMenu(window, variable2, *To)
opt.config(width=20, font=('Helvetica', 12))
opt.place(x=790, y=200)



lbl3= tk.Label(window, text="CONCESSION",width=30 ,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl3.place(x=5, y=300)

variable3 = tk.StringVar(window)
variable3.set(To[0])
opt = tk.OptionMenu(window, variable3, *Concession)
opt.config(width=20, font=('Helvetica', 12))
opt.place(x=240, y=300)

lbl4= tk.Label(window, text="TOTAL AMOUNT TO PAY",width=30 ,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl4.place(x=550, y=300)


lbl5= tk.Label(window, text="" ,width=30 ,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl5.place(x=790, y=300)



def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read(r"C:\Users\sandesh\Documents\finale\TrainingImage\trainimage.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df=pd.read_csv(r"C:\Users\sandesh\Documents\finale\travelerdetail\travelerdetail.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['Id','Name','Date','Time','station']
    present = pd.DataFrame(columns = col_names)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf < 50):
                station = variable1.get()
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                present.loc[len(present)] = [Id,aa,date,timeStamp,station]

            else:
                Id='Unknown'
                tt=str(Id)
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
        present=present.drop_duplicates(subset=['Id'],keep='first')
        cv2.imshow('im',im)
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="present\present_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    present.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=present
    message.configure(text= res)












trackimage = tk.Button(window, text="scan" ,bg="#8c8c8c" ,command= TrackImages ,width=20  ,height=4 ,activebackground = "Red" ,font=('times', 12, ' bold '))
trackimage.place(x=10, y= 500)

PrintTicket = tk.Button(window, text="PRINT TICKET",bg="#8c8c8c"  ,width=20  ,height=4 ,activebackground = "Red" ,font=('times', 12, ' bold '))
PrintTicket.place(x=250, y=500)


quitWindow = tk.Button(window, text="Quit", command=window.destroy,bg="#8c8c8c"  ,width=20  ,height=4, activebackground = "Red" ,font=('times', 12, ' bold '))
quitWindow.place(x=750, y=500)

window.mainloop()
