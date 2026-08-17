"""
Universal Robots Dashboard Server - Python Client

Indusrial automation project demonstrating TCP/IP communication between a Python application and a Universal Robots controller 

Dashboard Server default port: 29999
"""

import socket
import time


ROBOT_IP = "YOUR_ROBOT_IP"
DASHBOARD_PORT = 29999
TIMEOUT = 5


def send_command(sock: socket.socket, command: str) -> str:
    """Send a command to the UR Dashboard Server and return its response."""

    sock.sendall((command + "\n").encode("utf-8"))
    time.sleep(0.2)

    response = sock.recv(4096)

    return response.decode(
        "utf-8",
        errors="ignore"
    ).strip()


def main():

    print(f"Connecting to Universal Robot at {ROBOT_IP}:{DASHBOARD_PORT}...")

    try:
        with socket.create_connection(
            (ROBOT_IP, DASHBOARD_PORT),
            timeout=TIMEOUT
        ) as sock:

            welcome = sock.recv(4096).decode(
                "utf-8",
                errors="ignore"
            ).strip()

            print("Connected successfully.")
            print("Server:", welcome)

            # Robot status
            robot_mode = send_command(sock, "robotmode")
            program_state = send_command(sock, "programState")

            print("Robot mode:", robot_mode)
            print("Program state:", program_state)

            # -------------------------------------------------
            # Optional program control examples
            # Uncomment only when testing in a safe environment.
            # -------------------------------------------------

            # print(
            #     send_command(
            #         sock,
            #         "load YOUR_PROGRAM.urp"
            #     )
            # )

            # print(send_command(sock, "play"))

            # print(send_command(sock, "stop"))

    except socket.timeout:
        print("Connection timed out.")

    except ConnectionRefusedError:
        print("Connection refused by the robot controller.")

    except OSError as error:
        print(f"Communication error: {error}")


if _name_ == "_main_":
    main()
