import socket

# Definir Host y Puerto
HOST = 'servidor'
PORT = 5000

# Crear archivo
f = open ('respuestas.txt','w')
f.write("Respuesta\n\n")

# Crear socket y conectar al Servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Numero de mensajes a enviar
NumMensajes = 10

# Contador de mensajes
Cont = 0

# Acciones a realizar con el Servidor
while(Cont < NumMensajes):
    # Se escribe un mensaje al Cliente
    texto = "Mensaje desde el Cliente " + (str(Cont+1))
    s.sendall(texto.encode())

    # Se recibe mensaje desde el Servidor
    pipe = s.recv(1024)
    msg = str(pipe, 'utf-8')

    # El mensaje se printea y se escribe en el archivo
    print("La respuesta del Servidor es: %s" %msg)
    f.write('{0}\n'.format(msg))

    Cont += 1

# Cerrar el archivo y el socket
f.close()
s.close()