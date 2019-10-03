import socket
import time

# Definir Host y Puerto
#HOST = 'localhost'
HOST = 'headnode'
PORT = 5000

# Crear archivo
f = open ('registro_cliente.txt','w')
f.write("Num Datanode           Mensaje\n\n")

# Crear socket y conectar al Servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

flag = 0

# Acciones a realizar con el Servidor
while(True):
    # Menu de opciones
    print("Seleccione una opcion:")
    print("1. Enviar mensaje al Headnode")
    print("2. Finalizar conexion con el Datanode1")
    print("3. Finalizar conexion con el Datanode2")
    print("4. Finalizar conexion con el Datanode3")
    print("5. Finalizar conexion completa")

    # Se elige una opcion
    if(flag < 5):
        opcion = '1'
        flag += 1

    elif(flag == 5):
        opcion = '4'
        flag += 1

    elif(flag < 11):
        opcion = '1'
        flag += 1

    elif(flag == 11):
        opcion = '2'
        flag += 1

    elif(flag < 17):
        opcion = '1'
        flag += 1

    elif(flag == 17):
        opcion = '5'

    # Si la opcion es 1, se escribe un mensaje al Servidor y se espera una respuesta
    if(opcion == '1'):
        s.sendall(opcion.encode())
        if(flag < 6):
            texto = "Mensaje numero " + str(flag)
        elif(flag >= 7 and flag < 12):
            texto = "Mensaje numero " + str(flag - 1)
        elif(flag >= 12 and flag < 18):
            texto = "Mensaje numero " + str(flag - 2)
        time.sleep(1)
        s.sendall(texto.encode())

        # Se recibe mensaje desde el Servidor
        pipe = s.recv(1024)
        msg = str(pipe, 'utf-8')

        # El mensaje se escribe en el archivo
        f.write('{0}\n'.format(msg))

    elif(opcion == '2'):
        texto = "2"
        s.sendall(texto.encode())
        print("Datanode1 finalizado")
    elif(opcion == '3'):
        texto = "3"
        s.sendall(texto.encode())
        print("Datanode2 finalizado")
    elif(opcion == '4'):
        texto = "4"
        s.sendall(texto.encode())
        print("Datanode3 finalizado")
    # Si la opcion es 5, se finaliza la conexion con el Servidor
    elif(opcion == '5'):
        print("Conexion finalizada")
        break
    else:
        print("Opcion invalida, vuelva a intentar")

# Cerrar el archivo y el socket
f.close()
s.close()