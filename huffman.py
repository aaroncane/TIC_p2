import time
import os

inicio = time.time()
class NodoABB:
    def __init__(self, info):
        self.info = info
        self.izq = None
        self.der = None

def insertar_nodo(raiz, dato):
    if raiz is None:
        raiz = NodoABB(dato)
    elif dato < raiz.info:
        raiz.izq = insertar_nodo(raiz.izq, dato)
    else:
        raiz.der = insertar_nodo(raiz.der,dato)
    return raiz

def buscar(raiz,clave):
    pos = None
    if raiz is not None:
        if raiz.info == clave:
            pos = raiz
        elif clave < raiz.info:
            pos = buscar(raiz.izq, clave)
        else:
            pos = buscar(raiz.der, clave)
    return pos

def crear_Arbol(list_frecuencias):
    nodo_Aux = NodoABB(None)
    nodo_Aux.info = (None, list_frecuencias[0].info[1] + list_frecuencias[1].info[1])
    nodo_Aux.izq = list_frecuencias[0]
    nodo_Aux.der = list_frecuencias [1]

    list_frecuencias.append(nodo_Aux)   
    del list_frecuencias[0:2]   
    
    return list_frecuencias

def preorden_binario(raiz, diccionario, binario):
    if raiz is not None:
        diccionario[raiz.info[0]] = binario
        preorden_binario(raiz.izq, diccionario, (binario + '0') )
        preorden_binario(raiz.der,diccionario, (binario + '1'))
        
    return diccionario

archivo = 'file.jpg'

with open(archivo, 'rb') as f:  
    cadena = f.read()
    f.close()

if (len(cadena)) % 2 != 0:    
    cadena += b'\x00'         

tope = 1     
while True:
    if len(cadena) == 2:    
        break
    if len(cadena)//tope <= tope:break   
    if tope == 32: break                 
    else: tope *= 2                     
           
dic_frecuencias = {}     
for i in range(0, len(cadena), tope):   
    simbolo = cadena[i:i+tope]          
    if simbolo in dic_frecuencias:           
        dic_frecuencias[simbolo] += 1
    else:
        dic_frecuencias[simbolo] = 1
if len(dic_frecuencias)==1:
    print("Solo hay un simbolo en el archivo, se interrumpe el script.")
    exit()

def ordenar_Frecuencias(frecuencia):   
    diccionario_ordenado = dict(sorted(frecuencia.items(), key = lambda x: x[1])) 
    return diccionario_ordenado

dic_frecuencias = ordenar_Frecuencias(dic_frecuencias)  

list_frecuencias = list(dic_frecuencias.items())        


for i in range(len(list_frecuencias)):                  
    list_frecuencias[i] = NodoABB(list_frecuencias[i])   

while len(list_frecuencias)>=2:      
    list_frecuencias = crear_Arbol(list_frecuencias) 
dic_frecuencias = preorden_binario(list_frecuencias[0], dic_frecuencias, '') 


del dic_frecuencias[list(dic_frecuencias.keys())[-1]]   

cadena_binaria = ''
for i in range(0, len(cadena), tope):   
    llave = cadena[i:i+tope]          
    cadena_binaria +=  dic_frecuencias[llave] #

resto = len(cadena_binaria)%8
if resto != 0:
    cadena_binaria += '1'+('0'*(7-resto))

lista_de_Bytes = [int(cadena_binaria[i:i+8],2) for i in range(0, len(cadena_binaria),8)] 

with open("codificado.huff", "wb") as f:     
    for b in lista_de_Bytes:
        f.write(bytes([b]))  
    f.close()

fin = time.time()
tiempo_total = fin - inicio
print("El programa tardo: ", tiempo_total," segundos en crear el archivo .huff")


with open("codificado.huff", "rb") as f:
    
    contenido = f.read()
    f.close()

cadena_codificada = ''.join([bin(b)[2:].zfill(8) for b in contenido])

while True:
    if cadena_codificada[-1] == '1': 
        cadena_codificada = cadena_codificada[:-1]
        break
    else:
        cadena_codificada = cadena_codificada[:-1] 

codigo_temporal = ''
cadena_decodificada = bytes()

diccionario_invertido = {valor: clave for clave, valor in dic_frecuencias.items()}

for bit in cadena_codificada:
    codigo_temporal += bit  

    if codigo_temporal in diccionario_invertido.keys():  
        simbolo = diccionario_invertido[codigo_temporal]
        cadena_decodificada += simbolo
        codigo_temporal = ''



with open ("decodificado.bin", 'wb') as f:
    f.write(cadena_decodificada)
    f.close

fin = time.time()
print("Tamanio de imagen sin codificar: ", os.stat("file.jpg").st_size, " Bytes")
print("Tamanio de imagen con extension .huff: ", os.stat("codificado.huff").st_size, " Bytes")
print("Tamanio de imagen con extension .bin: ", os.stat("decodificado.bin").st_size, " Bytes")

tiempo_total = fin - inicio

print("El programa tardo: ", tiempo_total," segundos.")
