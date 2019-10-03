import socket
import random
import threading
import time
import sys

# Definir Host y Puerto
#HOST = 'localhost'
HOST = 'headnode'
PORT = 5000

PORT1 = 5001
PORT2 = 5002
PORT3 = 5003

ListaVivos = [0,0,0]

# Crear archivo
f = open ('registro_server.txt','a')
f.write("Num Datanode           Mensaje\n\n")

f2 = open ('heartbeat_server.txt','w')

# Crear socket cliente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET para IPv4 y SOCK_STREAM para TCP
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

# Crear socket datanode1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s1.connect(("localhost", PORT1))
s1.connect(("datanode1", PORT1))
ListaVivos[0] = 1

# Crear socket datanode2
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s2.connect(("localhost", PORT2))
s2.connect(("datanode2", PORT2))
ListaVivos[1] = 1

# Crear socket datanode3
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s3.connect(("localhost", PORT3))
s3.connect(("datanode3", PORT3))
ListaVivos[2] = 1


def Alive(Puerto1, Puerto2, Puerto3, Socket1, Socket2, Socket3, Archivo):
    while(True):
        global flag
        global ListaVivos

        confirmo = "confirmar"

        if(ListaVivos[0] == 1):
            Socket1.sendall(confirmo.encode())
        if(ListaVivos[1] == 1):
            Socket2.sendall(confirmo.encode())
        if(ListaVivos[2] == 1):
            Socket3.sendall(confirmo.encode())

        time.sleep(5)

        try:
            respuesta1 = Socket1.recv(1024)
            ACK1 = str(respuesta1, 'utf-8')
            Archivo.write("Datanode1 vivo\n")
            if(ACK1 == ""):
                ListaVivos[Puerto1 - 5001] = 0
                Archivo.write("Datanode1 no vivo\n")
        except:
            print("")

        try:
            respuesta2 = Socket2.recv(1024)
            ACK2 = str(respuesta2, 'utf-8')
            Archivo.write("Datanode2 vivo\n")
            if(ACK2 == ""):
                ListaVivos[Puerto2 - 5001] = 0
                Archivo.write("Datanode2 no vivo\n")
        except:
            print("")

        try:
            respuesta3 = Socket3.recv(1024)
            ACK3 = str(respuesta3, 'utf-8')
            Archivo.write("Datanode3 vivo\n")
            if(ACK3 == ""):
                ListaVivos[Puerto3 - 5001] = 0
                Archivo.write("Datanode3 no vivo\n")
        except:
            print("")
        #result1 = Socket1.connect_ex(('localhost', Puerto1))
        #result2 = Socket2.connect_ex(('localhost', Puerto2))
        #result3 = Socket3.connect_ex(('localhost', Puerto3))
        
        if(flag):
            break

# Obtener IP
nombre_equipo = socket.gethostname()
IP = socket.gethostbyname(nombre_equipo)

# Espera conexion del Cliente
print("Esperando peticiones...")

# Conectarse con el Cliente
while True:
    flag = False
    t = threading.Thread(target = Alive, args = (PORT1, PORT2, PORT3, s1, s2, s3, f2))
    t.start()
    # Se recibe mensaje desde el Cliente
    pipe = conn.recv(1024)
    msg = str(pipe, 'utf-8')
    if(msg == '1'):
        pipeCliente = conn.recv(1024)
        msgCliente = str(pipeCliente, 'utf-8')
        while(True):
            NumDatanode = random.choice([1,2,3])
            if(ListaVivos[NumDatanode-1] == 1):
                break
        if(NumDatanode == 1 and ListaVivos[0]):
            s1.sendall(msgCliente.encode())
            pipe1 = s1.recv(1024)
            ACK = str(pipe1, 'utf-8')
        elif(NumDatanode == 2 and ListaVivos[1]):
            s2.sendall(msgCliente.encode())
            pipe2 = s2.recv(1024)
            ACK = str(pipe2, 'utf-8')
        elif(NumDatanode == 3 and ListaVivos[2]):
            s3.sendall(msgCliente.encode())
            pipe3 = s3.recv(1024)
            ACK = str(pipe3, 'utf-8')
        if(ACK != "confirmo"):
            print("Mensaje guardado correctamente")
        MensajeCliente = str(NumDatanode) + '                      ' + msgCliente
        f.write('{0} \n'.format(MensajeCliente))
        conn.sendall(MensajeCliente.encode())
    
    elif(msg == '2'):
        matar = "kill"
        s1.sendall(matar.encode())
        pipe1 = s1.recv(1024)
    elif(msg == '3'):
        matar = "kill"
        s2.sendall(matar.encode())
        pipe2 = s2.recv(1024)
    elif(msg == '4'):
        matar = "kill"
        s3.sendall(matar.encode())
        pipe3 = s3.recv(1024)
    # Finalizar conexion
    elif not pipe:
        flag = True
        break

# Cerrar el archivo y el socket
f.close()
s.close()
s1.close()
s2.close()
s3.close()
sys.exit()