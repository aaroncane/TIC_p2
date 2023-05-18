
import time
inicio = time.time()
def split_list(lst):
    total = sum(freq for _, freq in lst)    
    half = total / 2
    
    index = 0
    right = 0 
    inicio = 0
    fin = len(lst)-1
    
    if len(lst) == 2:   
        index = 1        
    else:               
        while True:
            right += lst[inicio][1]      
            if (right >= half):      
                index = inicio       
                if inicio == fin:    
                    index = inicio+1 
                    break            
                break
            fin += -1       
            inicio += 1    
    return lst[:index], lst[index:]


def shannon_fano(lst, code=""):
    if len(lst) == 1:
        symbol = lst[0][0]
        codes[symbol] = code 
        return
    right, left = split_list(lst)
    shannon_fano(left, code + "0")
    shannon_fano(right, code + "1")
 


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
    if tope == 16: break                 
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
sorted_freqs = sorted(dic_frecuencias.items(), key=lambda x: (x[1]))

codes = {} 
shannon_fano(sorted_freqs)

cadena_binaria = ''
for i in range(0, len(cadena), tope):   
    llave = cadena[i:i+tope]          
    cadena_binaria +=  codes[llave] 

resto = len(cadena_binaria)%8
if resto != 0:
    cadena_binaria += '1'+('0'*(7-resto))

lista_de_Bytes = [int(cadena_binaria[i:i+8],2) for i in range(0, len(cadena_binaria),8)] 

with open("codificado.shfa", "wb") as f:      
    for b in lista_de_Bytes:
        f.write(bytes([b]))  
    f.close()

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos en crear el archivo .shfa")

with open("codificado.shfa", "rb") as f:
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

diccionario_invertido = {valor: clave for clave, valor in codes.items()}

for bit in cadena_codificada:
    codigo_temporal += bit  
    if codigo_temporal in diccionario_invertido.keys():  
        simbolo = diccionario_invertido[codigo_temporal]
        cadena_decodificada += simbolo
        codigo_temporal = ''

print(cadena_decodificada == cadena)

with open ("decodificado.bin", 'wb') as f:
    f.write(cadena_decodificada)
    f.close

fin = time.time()
tiempo_total = fin - inicio
print(f"El programa tardó {tiempo_total} segundos.")