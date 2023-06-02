import qrcode
import psycopg2
import smtplib
import imghdr
import random
from email.message import EmailMessage



# In[1]:
"""
Data base stuff
"""

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



def insert_query(query,data):
    try:
        con = connection()
        if con and query != '' and data != []: #Con mas parametros (WHERE - INSERT)
            cursor = con.cursor()
            cursor.execute(query,data)
        con.commit()
    except(Exception, con.Error) as error:
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
"""
System 
"""

def registroperson():
    rut = ""
    nombre = ""
    apellido = ""
    mail = ""
    print("\nBienvenido ingrese sus datos para registrarse") 
    print("Ingrese rut:")
    rut = str(input())
    print("Ingrese su nombre:")
    nombre = str(input())
    print("Ingrese su apellido:")
    apellido = str(input())
    print("Ingrese su email:")
    mail = str(input())
    codigo = generarQrCode()  
    try:
        query = "insert into person(rut,mail,namePerson,lastName) values (%s,%s,%s,%s)"
        insert_query(query, (rut,mail,nombre,apellido))        
        print("fail")
              
        query = "insert into person_qrcode(rut,qrcode) values (%s,%s)"
        insert_query(query, (rut,codigo))
        print("Registro realizado con exito")
        print("Enviando correo")
        senteamil(codigo, )


    except(Exception, psycopg2.Error) as error:
        print("Error: %s" % error)


def generarQrCode():
    while(True):
        codigo = ""
        for i in range(20):
                codigo += str(random.randint(0, 9))
        query = "select rut from person_qrcode where qrcode=%s"
        data = select_query(query, [codigo])
        if(data == []):
            return str(codigo)
             


def senteamil(nameImage, mail):
    img=qrcode.make(nameImage)
    img.save('qrCode.png')
    mensaje = """<html>
    <body><p>Codigo qr aaaa.</p>
    <image src="qrCode.png"/></body></html>"""
    msg = EmailMessage()

    remitente = "ceferinoguajardo@gmail.com"
    destinatario = mail

    with open('qrCode.png', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = mail
    email["Subject"] = "Correo de prueba"
    email.set_content(mensaje,subtype='html')
    email.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, "crcmtxfuoacbdlif")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()



print("Genrador de qr's y registro")
print("Ingrese -1 para salir")
rut = ""

while(True):
    print("\nIngrese el rut del cliente")
    rut = input()
    query = "select rut from person where rut=%s"
    if(rut == "-1"):
        break
    else:
        data = select_query(query, [rut])
        if(data == []):
            print("\npersona no encontrado")
            print("[1] registrarlo")
            print("[2] volver a intentarlo")
            eleccion = input()
            if(eleccion == "1"):
                registroperson()
        else:
            #Aca deve ir el generar codigo qr para X persona y leugo enviarlo al gmail
            print("Generando qr para X persona y leugo enviar")
            query = "select mail from person where rut=%s"
            data, = select_query(query, [rut])[0]
            infoMail = str(data)
            query = "select qrcode from person_qrcode where rut=%s"
            data, = select_query(query, [rut])[0]
            infoQrCode = str(data)
            print(infoMail)
            senteamil(infoQrCode, infoMail)




    print("\n(Ingrese -1 para salir)")




