import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

log_lock = threading.Lock()


def calculate_grade(marks):
    if marks >= 90:
        return "A+", 4.00
    elif marks >= 86:
        return "A", 4.00
    elif marks >= 82:
        return "A-", 3.67
    elif marks >= 78:
        return "B+", 3.33
    elif marks >= 74:
        return "B", 3.00
    elif marks >= 70:
        return "B-", 2.67
    elif marks >= 66:
        return "C+", 2.33
    elif marks >= 62:
        return "C", 2.00
    elif marks >= 58:
        return "C-", 1.67
    elif marks >= 54:
        return "D+", 1.33
    elif marks >= 50:
        return "D", 1.00
    else:
        return "F", 0.00


def handle_client(client_socket, address):
    try:
        client_socket.send(
            b"Welcome to FAST-NUCES Karachi Campus CGPA Calculator!"
        )

        client_socket.send(b"Enter Student ID:")
        student_id = client_socket.recv(1024).decode()

        client_socket.send(b"Enter number of subjects:")
        num_subjects = int(client_socket.recv(1024).decode())

        subjects = []
        total_quality_points = 0
        total_credit_hours = 0

        for i in range(num_subjects):
            client_socket.send(
                f"Enter Credit Hours for Subject {i + 1}:".encode()
            )
            credit_hours = int(client_socket.recv(1024).decode())

            client_socket.send(
                f"Enter Marks for Subject {i + 1} (out of 100):".encode()
            )
            marks = float(client_socket.recv(1024).decode())

            grade, gpa = calculate_grade(marks)

            subjects.append({
                "credit_hours": credit_hours,
                "marks": marks,
                "grade": grade,
                "gpa": gpa
            })

            total_quality_points += gpa * credit_hours
            total_credit_hours += credit_hours

        cgpa = total_quality_points / total_credit_hours

        result = "\nCGPA CALCULATION RESULT\n"
        result += "-----------------------\n"

        for i, subject in enumerate(subjects):
            result += (
                f"Subject {i + 1}: "
                f"Credit Hours: {subject['credit_hours']}, "
                f"Marks: {subject['marks']}, "
                f"Grade: {subject['grade']}, "
                f"GPA: {subject['gpa']:.2f}\n"
            )

        result += f"\nOverall CGPA: {cgpa:.2f}"

        client_socket.send(result.encode())

        with log_lock:
            with open("cgpa_log.txt", "a") as file:
                file.write(f"Student ID: {student_id}\n")

                for i, subject in enumerate(subjects):
                    file.write(
                        f"Subject {i + 1}: "
                        f"Credit Hours: {subject['credit_hours']}, "
                        f"Marks: {subject['marks']}, "
                        f"Grade: {subject['grade']}, "
                        f"GPA: {subject['gpa']:.2f}\n"
                    )

                file.write(f"Overall CGPA: {cgpa:.2f}\n")
                file.write("-" * 50 + "\n")

        print(f"Client {address} completed calculation.")

    except Exception as e:
        print(f"Error with client {address}: {e}")

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server started on {HOST}:{PORT}")
print("Waiting for students to connect...")

while True:
    client_socket, address = server_socket.accept()

    print(f"Student connected from {address}")

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    client_thread.start()