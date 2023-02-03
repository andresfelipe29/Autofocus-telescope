import pandas as pd
import cv2
import time
import math
import serial

#Funcion que evalua el maximo enfoque, retorna su valor y el tiempo en el que obtuvo ese enfoque.
def get_max(data_frame):
    index_max = data_frame['focus'].idxmax()
    time_max=data_frame.loc[index_max, 'time']
    focus_level=data_frame.loc[index_max, 'focus']
    return(time_max, focus_level)

#Funcion que cuando el arduino arranca comienza a evaluar los bordes de cada imagen que se transmiten desde el telescopio.
def lectura_info(ser):

    tiempo_lectura = 0
    focusing = ser.read().decode('ascii')

    #Inicializacion y creacion de archivo data.txt
    raw_video = cv2.VideoCapture(1)
    start = time.time()
    previous = 0
    f = open('data.txt', 'r+') #Archivo en el que se guardan todos los datos que va obteniendo Python de cada imagen
    f.truncate(0)
    f.close()
    #display

    while focusing != '0':
        focusing = ser.read().decode('ascii')

        if focusing == '1':
            tiempo_lectura = 1
            #Cuando el arduino arranca comienza a evaluar la imagen
        if tiempo_lectura == 1:
            partial = time.time() - start
            current = int(math.floor(partial))
            ret, frame = raw_video.read()
            gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #create border images with canny and save contrast values
            canny = cv2.Canny(gray_video,0,100)
            canny_var = cv2.Canny(gray_video,0,100).var()

            cv2.imshow("Canny", canny)

            if (current % 1 == 0) & (current != previous):
                escritura = str(round(partial,3)) + "\t"+ str(round(canny_var,3)) + "\n"
                print(escritura)
                with open("data.txt", "a") as testfile1:
                    testfile1.write(escritura)
                    previous = current

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
#La toma de datos termina cuando el telescopio ha recorrido todo su trayecto y toca el boton que cambia la direccion.
    raw_video.release()
    cv2.destroyAllWindows()    
    return(partial)