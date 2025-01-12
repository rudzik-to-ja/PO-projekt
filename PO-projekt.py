from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class User:
    def __init__(self, user_id, name, lastname):
        self.id = user_id
        self.name = name
        self.lastname = lastname


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    users = []
    next_id = 1

    def _set_response(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/users":
            self._set_response()
            self.wfile.write(
                json.dumps([user.__dict__ for user in self.users]).encode("utf-8")
            )
        elif self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            user = next((user for user in self.users if user.id == user_id), None)
            if user:
                self._set_response()
                self.wfile.write(json.dumps(user.__dict__).encode("utf-8"))
            else:
                self._set_response(400)
                self.wfile.write(
                    json.dumps({"error": "User not found"}).encode("utf-8")
                )

    def do_POST(self):
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            post_data = json.loads(self.rfile.read(content_length))
            if "name" in post_data and "lastname" in post_data:
                new_user = User(self.next_id, post_data["name"], post_data["lastname"])
                self.users.append(new_user)
                self.next_id += 1
                self._set_response(201)
                self.wfile.write(json.dumps(new_user.__dict__).encode("utf-8"))
            else:
                self._set_response(400)
                self.wfile.write(
                    json.dumps({"error": "Invalid user data"}).encode("utf-8")
                )

    def do_PATCH(self):
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            patch_data = json.loads(self.rfile.read(content_length))
            user = next((user for user in self.users if user.id == user_id), None)
            if user and ("name" in patch_data or "lastname" in patch_data):
                if "name" in patch_data:
                    user.name = patch_data["name"]
                if "lastname" in patch_data:
                    user.lastname = patch_data["lastname"]
                self._set_response(204)
            else:
                self._set_response(400)
                self.wfile.write(
                    json.dumps({"error": "Invalid user data or user not found"}).encode(
                        "utf-8"
                    )
                )

    def do_PUT(self):
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = json.loads(self.rfile.read(content_length))
            if "name" in put_data and "lastname" in put_data:
                user = next((user for user in self.users if user.id == user_id), None)
                if user:
                    user.name = put_data["name"]
                    user.lastname = put_data["lastname"]
                else:
                    new_user = User(user_id, put_data["name"], put_data["lastname"])
                    self.users.append(new_user)
                self._set_response(204)
            else:
                self._set_response(400)
                self.wfile.write(
                    json.dumps({"error": "Invalid user data"}).encode("utf-8")
                )

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[-1])
            user = next((user for user in self.users if user.id == user_id), None)
            if user:
                self.users.remove(user)
                self._set_response(204)
            else:
                self._set_response(400)
                self.wfile.write(
                    json.dumps({"error": "User not found"}).encode("utf-8")
                )


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
