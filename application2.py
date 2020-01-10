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
from datetime import date
today = str(date.today())
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



message = tk.Label(window, text="PASS SERVICES INDIAN RAILWAY" ,bg="white",width=100  ,height=4,font=('times', 25, 'italic bold underline'))

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



lbl3= tk.Label(window, text="Name",width=30 ,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl3.place(x=5, y=300)

txt2 = tk.Entry(window,width=30  ,bg="White",font=('times', 15, ' bold ')  )
txt2.place(x=240, y=300)


lbl4 = tk.Label(window, text="MOBILE NUMBER",width=30,bg="#8c8c8c"    ,height=2 ,font=('times', 9, ' bold '))
lbl4.place(x=550, y=300)

txt4 = tk.Entry(window,width=30  ,bg="White",font=('times', 15, ' bold ')  )
txt4.place(x=790, y=300)




lbl5 = tk.Label(window, text="ADHAR CARD",width=30  ,bg="#8c8c8c",height=2 ,font=('times', 9, ' bold '))
lbl5.place(x=5, y=400)

txt5 = tk.Entry(window,width=30  ,bg="white",font=('times', 15, ' bold ')  )
txt5.place(x=240, y=400)


lbl6 = tk.Label(window, text="date of expiry",width=30  ,bg="#8c8c8c",height=2 ,font=('times', 9, ' bold '))
lbl6.place(x=550, y=400)

txt6 = tk.Entry(window,width=30  ,bg="white",font=('times', 15, ' bold ')  )
txt6.place(x=790, y=400)






#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("facial recognition system for Indian Railway")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

#window.geometry('1280x720')
window.configure(background='#404040')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="PASS SERVICES INDIAN RAILWAY" ,bg="white",width=100  ,height=5,font=('times', 25, 'italic bold underline'))

message.place(x=0, y=0)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    mobilenumber =(txt4.get())

    Adharcardnumber=(txt5.get())
    date = today
    fromstation = (variable1.get())
    tostation =(variable2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #incrementing sample number
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name, mobilenumber, Adharcardnumber, date, fromstation, tostation]
        with open(r'C:\Users\sandesh\Documents\finale\travelerdetail\travelerdetail.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.write(r"C:\Users\sandesh\Documents\finale\TrainingImage\trainimage.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #print(imagePaths)

    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids



Scanbtn = tk.Button(window, text="takeImage", command = TakeImages,bg="#8c8c8c"  ,width=20  ,height=4 ,activebackground = "Red" ,font=('times', 12, ' bold '))
Scanbtn.place(x=250, y= 500)


lbl1 = tk.Label(window, text="enter id",width=20  ,height=2 ,bg="#8c8c8c" ,font=('times', 9, ' bold ') )
lbl1.place(x=5, y=150)
txt = tk.Entry(window,width=30  ,bg="#8c8c8c",font=('times', 15, ' bold ')  )
txt.place(x=240, y=150)


trainimage = tk.Button(window, text="TRAINIMAGE", command=TrainImages ,bg="#8c8c8c"  ,width=20  ,height=4, activebackground = "Red" ,font=('times', 12, ' bold '))
trainimage.place(x=500,y=500)

PrintPass = tk.Button(window, text="PRINT",bg="#8c8c8c"  ,width=20  ,height=4 ,activebackground = "Red" ,font=('times', 12, ' bold '))
PrintPass.place(x=750, y=500)

quitWindow = tk.Button(window, text="Quit", command=window.destroy,bg="#8c8c8c"  ,width=20  ,height=4, activebackground = "Red" ,font=('times', 12, ' bold '))
quitWindow.place(x=1000, y=500)


#trackimage = tk.Button(window, text="TrackImages", command=TrackImages ,bg="#8c8c8c"  ,width=20  ,height=4, activebackground = "Red" ,font=('times', 12, ' bold '))
#trackimage.place(x=750, y=600)

window.mainloop()
