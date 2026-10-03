import socket

HOST = "127.0.0.1"
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print(client_socket.recv(1024).decode())

print(client_socket.recv(1024).decode(), end=" ")
student_id = input()
client_socket.send(student_id.encode())

print(client_socket.recv(1024).decode(), end=" ")
num_subjects = input()
client_socket.send(num_subjects.encode())

for i in range(int(num_subjects)):
    print(client_socket.recv(1024).decode(), end=" ")
    credit_hours = input()
    client_socket.send(credit_hours.encode())

    print(client_socket.recv(1024).decode(), end=" ")
    marks = input()
    client_socket.send(marks.encode())

result = client_socket.recv(4096).decode()

print(result)

client_socket.close()