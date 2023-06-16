from tkinter import ttk
import cv2
from pyzbar import pyzbar
import time
import psycopg2
from datetime import date

from tkinter import *
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import imutils

import serial


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)


ser = serial.Serial('COM10', 9600)
if not ser.isOpen():
    ser.open()
print('COM10 is open', ser.isOpen())

def connection():
    try:
        connection = psycopg2.connect(host='proyecto-a.cp6afttaszko.us-east-1.rds.amazonaws.com',
                                     database="Proyecto_A",user="postgres",password="12345678")
        #connection = psycopg2.connect(host='localhost',
         #                             database="personasProyectoGym",user="postgres",password="1234")
        return connection
    
    except(Exception, connection.Error) as error:
        connection.rollback()
        print("Error:" % error)


def select_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
            result = cursor.fetchall()
            return result
        else:
            return ""
    except(Exception, con.Error) as error:
        print("Error unexpect, connection terminated")
        print("Error: %s" % error)


def read_barcodes(frame):
    barcode_info = ""
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #3
        with open("barcode_r2esult.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
        
    return frame, barcode_info



#4

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            reading=""
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame, reading = read_barcodes(frame)
            print(reading)
            #hide label here
            if (reading != ""):
                query = "select fecha_de_caducidad from person_qrcode where qrcode=%s"
                data, = select_query(query, [reading])[0]
                today = date.today()
                
                queryRut = "select rut from person_qrcode where qrcode=%s"
                data2, = select_query(queryRut, [reading])[0]
                print(data2)
                rutCosa = str(data2)
                queryName = "select namePerson from person where rut=%s"
                data3, = select_query(queryName, [rutCosa])[0]
                print(data)
                print(data3)
                if(data > today):
                    print("192.168.1.1")
                    lblStatus.config(text="Valid QR Code for:"+data3+"", bg="green")
                    #show label here    
                    ser.write(b'1')                
                    time.sleep(5)
                    
                else:
                    print("paga")
                    lblStatus.config(text="Expired QR Code for:"+data3+"", bg="red")
                    ser.write(b'2') 
                    time.sleep(0)

            else:
                lblStatus.config(text="", bg="SystemButtonFace")
                ser.write(b'0') 
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.place(x=0,y=40)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
            
            
        else:
            lblVideo.image = ""
            cap.release()
            
            



cap = None
root = Tk()




lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)
Label(text='Camara de lectura codigo qr',fg='white',background='black',font=('Agency FB',25)).place(relx = 0.5,y = 20, anchor = CENTER)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


lblStatus = Label(root, text="", bg="SystemButtonFace", wraplength=200)
lblStatus.grid(column=0, row=2, columnspan=2, pady=10)
lblStatus.place(relx = 0.5,rely  = 0.9, anchor = CENTER)

if cap is not None:
    ret, frame = cap.read()
    if ret == True:
        reading=""
        frame = imutils.resize(frame, width=640)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame, reading = read_barcodes(frame)
        if(reading==""):
            print("192.168.1.1")
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)
    else:
        lblVideo.image = ""
        cap.release()
        
root.mainloop()

