from tools import lectura_info
from tools import get_max
import serial
import time
import pandas as pd

#Comunicacion con el arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#Comienza la funcion de lectura
parcial = lectura_info(ser)
#Lee la tabla que esta en el archivo data.txt
data = pd.read_table('data.txt', header=None, sep="\t", names=["time", "focus"])
#Obtiene el tiempo con el valor maximo de enfoque
time_max, focus_level=get_max(data)
#Le envia al arduino el tiempo que encontro
ser.write(time_max)
print("finished focusing at", time_max, "with focus level =", focus_level)
ser.close()