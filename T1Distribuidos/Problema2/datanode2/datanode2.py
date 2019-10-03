import socket

# Definir Host y Puerto
#HOST = 'localhost'
HOST = 'datanode2'
PORT = 5002

# Crear archivo
f = open ('data.txt','w')
f.write("Mensaje\n\n")

# Crear socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET para IPv4 y SOCK_STREAM para TCP
s.bind((HOST, int(PORT)))
s.listen()
conn, addr = s.accept()

# Obtener IP
nombre_equipo = socket.gethostname()
IP = socket.gethostbyname(nombre_equipo)

# Espera conexion del Headnode
print("Esperando peticiones...")

# Conectarse con el Headnode
while True:
    
    # Se recibe mensaje desde el Headnode
    pipe = conn.recv(1024)
    msg = str(pipe, 'utf-8')

    if(msg == "confirmar"):
        resp = "confirmo"
        conn.sendall(resp.encode())
    elif(msg == "kill"):
        break
    else:
        # Finalizar conexion
        if not pipe:
            break

        # El mensaje se escribe en el archivo
        f.write('{0} \n'.format(msg))
        respuesta = "Mensaje guardado correctamente"
        conn.sendall(respuesta.encode())

    # Se responde al Cliente
    #print("Escriba la respuesta para el Cliente:")
    #texto = input()
    #conn.sendall(texto.encode())

# Cerrar el archivo y el socket
f.close()
s.close()