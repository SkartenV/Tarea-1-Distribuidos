import socket

# Definir Host y Puerto
HOST = 'servidor'
PORT = 5000

# Crear archivo
f = open ('log.txt','w')
f.write("IP           Mensaje\n\n")

# Crear socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET para IPv4 y SOCK_STREAM para TCP
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

# Obtener IP
nombre_equipo = socket.gethostname()
IP = socket.gethostbyname(nombre_equipo)

Cont = 0

# Conectarse con el Cliente
while (True):
    # Espera conexion del Cliente
    print("Esperando peticiones...")

    # Se recibe mensaje desde el Cliente
    pipe = conn.recv(1024)
    msg = str(pipe, 'utf-8')

    # Finalizar conexion
    if not pipe:
        break

    # El mensaje se printea y se escribe en el archivo junto con la IP
    print("El mensaje del Cliente es: %s" %msg)
    f.write('{0} {1}\n'.format(IP, msg))

    # Se responde al Cliente
    texto = "Respuesta " + str((Cont+1)) + " desde el Servidor"
    conn.sendall(texto.encode())
    Cont += 1
# Cerrar el archivo y el socket
f.close()
s.close()