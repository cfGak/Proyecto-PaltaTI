import cv2
from pyzbar import pyzbar
import time
import psycopg2
from datetime import date

def connection():
    try:
        #connection = psycopg2.connect(host='proyecto-a.cp6afttaszko.us-east-1.rds.amazonaws.com',
        #                             database="Proyecto_A",user="postgres",password="12345678")
        connection = psycopg2.connect(host='localhost',
                                      database="personasProyectoGym",user="postgres",password="1234")
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


def read_barcodes(frame, barcode_info):
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
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame, barcode_info


def main():
    #1
    camera = cv2.VideoCapture(1)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        barcode_info = ""
        frame, reading = read_barcodes(frame, barcode_info)
        cv2.imshow('Barcode/QR code reader', frame)
        print(reading)
        if (reading != ""):
            query = "select fecha_de_caducidad from person_qrcode where qrcode=%s"
            data, = select_query(query, [reading])[0]
            today = date.today()
            print(data)
            if(data > today):
                print("192.168.1.1")
                
                time.sleep(1)
            else:
                print("paga")
                time.sleep(10)
        #time.sleep(1)
        elif cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()