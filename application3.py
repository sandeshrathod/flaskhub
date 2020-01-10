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



message = tk.Label(window, text="FACE DETECTION SYSTEM INDIAN RAILWAY" ,bg="white",width=95  ,height=5,font=('times', 25, 'italic bold underline'))

message.place(x=0, y=0)



CurrentStation= [
"pachora.jn",
"jalgaon.jn",
"Bhusawal.jn"
]

variableStation = tk.StringVar(window)
variableStation.set(CurrentStation[0])


lbl = tk.Label(window, text="select station",width=20  ,height=2 ,bg="#8c8c8c" ,font=('times', 9, ' bold ') )
lbl.place(x=5, y=200)

opt = tk.OptionMenu(window, variableStation, *CurrentStation)
opt.config(width=20, font=('Helvetica', 12))
opt.place(x=240, y=200)



def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read(r"C:\Users\sandesh\Documents\finale\TrainingImage\trainimage.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    df=pd.read_csv(r"C:\Users\sandesh\Documents\finale\travelerdetail\travelerdetail.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['Id','Name','Date','Time','station','leagal']
    present = pd.DataFrame(columns = col_names)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf < 50):
                temp1 = df['fromstation']
                temp2 = df['tostation']
                station = variableStation.get()
                st = str(station)

                leagal = (df.fromstation == st).any() or (df.tostation == st).any()

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                present.loc[len(present)] = [Id,aa,date,timeStamp,station,leagal]

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



Scanbtn = tk.Button(window, text="scan", command = TrackImages ,bg="#8c8c8c"  ,width=20  ,height=4 ,activebackground = "Red" ,font=('times', 12, ' bold '))
Scanbtn.place(x=100, y= 500)

quitWindow = tk.Button(window, text="Quit", command=window.destroy,bg="#8c8c8c"  ,width=20  ,height=4, activebackground = "Red" ,font=('times', 12, ' bold '))
quitWindow.place(x=400, y=500)


window.mainloop()
