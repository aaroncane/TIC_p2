import base64


def contennt(s_strings):    
    contenido = [] 
    while True:
        try:
            if s_strings[0] in contenido:
                c = s_strings[0] + s_strings[1]
                del s_strings[:2]
                s_strings.insert(0,c)     
            else:          
                contenido.append(s_strings[0])
                s_strings.pop(0)
            if len(s_strings) == 0:
                break
        except IndexError:
            pass
            break
    return contenido
      
def location(content):
    localizacion = {}  
    n = len(content)   
    
    formato = "{0:02x}" 
    try:
        localizacion[''] = formato.format(0)   
        for i in range(n):
            localizacion[content[i]] = formato.format(i+1) 
    except IndexError:
            pass
    return localizacion

def codeword(location):
    llave = list(location.items())[1][0]

    longitud_minima = len(llave)

    c = []
    s = ''

    for key in location:
        try:
            s = key[-1]     
            s = key[-longitud_minima:]
            if len(key) == longitud_minima: 
                s = location[''] + s
            else:         
                s = location[key[:-longitud_minima]] + s
            c.append(s)
        except IndexError:
                pass
    return c    

def decodeword(location):
    print('location', location)

    indice = list(location.values())[0]     
    print('indice', indice)

    location = modificarDic(location)       
    c = []  
    s = ''  
    for key in location:
        try:
            s = location[key][:-1]      
            if indice == s:             
                s = location[key][-1]
                location[key] = s       
                c.append(s)
            else:                                       
                s = location[s] + location[key][-1]     
                location[key] = s       
                c.append(s)
        except:
            pass
    
    return c
        
def modificarDic(location):  
    nuevo_diccionario = {}
    primer_item = True

    for clave, valor in location.items():
        if primer_item:
            nuevo_diccionario[clave] = valor
            primer_item = False
        else:
            nuevo_diccionario[valor] = clave
    
    return nuevo_diccionario


def crearArchivo(cadena, nombreArchivo):

    cadena_utf16 = []

    for elem in cadena:
        hex_valor = elem[:-1]
   
        int_valor = int(hex_valor, 16)


        char_utf16 = chr(int_valor)

        cadena_utf16.append(char_utf16 + elem[-1])

    print(cadena_utf16)
    with open(nombreArchivo, 'w') as f:
        f.write(''.join(cadena))
        f.close()
 

with open("archivo.bin", "rb") as file:
    encoded_string = base64.b64encode(file.read())
    file.close()

cadena = encoded_string.decode('utf-16')  
s_strings = list(map(str, cadena))      

print(cadena,'\n', len(s_strings))

contenido = contennt(s_strings)    
print('contenido',contenido)
localizacion = location(contenido)  
print('localizaicon', localizacion)
codigo = codeword(localizacion)     
print('codigo', codigo, len(''.join(codigo)))

crearArchivo(codigo, 'archivo_Codificado.lpzv')

with open("archivo_Codificado.lpzv", "r") as file:
    cadena = file.read()
    file.close()
print('esto',cadena, len(cadena))

longitud_segmento = 3

codigo = [cadena[i:i+longitud_segmento] for i in range(0, len(cadena), longitud_segmento)]

print(codigo)


localizacion = location(codigo)  
decodificacion = decodeword(localizacion)

decodificacion = ''.join(decodificacion)
print(decodificacion)

decodificacion = decodificacion.encode('utf-16')
decodificacion = base64.b64decode(decodificacion)

with open('archivo_Decodificado.bin', 'wb') as f:
    f.write(decodificacion)