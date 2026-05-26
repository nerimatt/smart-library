import socket

class WebServer:
    s: socket.socket

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((station.ifconfig()[0], 80))
        self.s.listen(5) # max 5 socket connections // max possible should be 16

    def send_response(conn, body, content_type = "text/plain"):
        if isinstance(body, str):
            body = body.encode("utf-8")

        header = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: " + content_type.encode("utf-8") + b"\r\n"
            b"Content-Length: " + str(len(body)).encode("utf-8") + b"\r\n"
            b"Connection: close\r\n"
            b"\r\n"
        )

        conn.sendall(header + body)


    def accept(self):
        conn, addr = self.s.accept()

        try:
            # recieve data (of infinite length)
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                request += chunk

            header_bytes, body = request.split(b"\r\n\r\n", 1)

            header_text = header_bytes.decode("utf-8")
            header_lines = header_text.split("\r\n")

            method, path, protocol = header_lines[0].split()

            headers = {}
            for line in header_lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()

            content_type = headers.get("content-type")
            content_length = int(headers.get("content-length", "0"))

            # Read remaining body bytes, if recv() did not get all of it
            while len(body) < content_length:
                body += conn.recv(content_length - len(body))

            print("recieved request:", method, path, content_type)


            # TODO:

        except Exception as e:
            print("server error:", e)
            try:
                self.send_response(conn, dumps({"ok": False, "error": str(e)}), "application/json")
            except:
                pass

        finally:
            conn.close()
            sleep(0.01)


