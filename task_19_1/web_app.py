from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = "localhost"
server_port = 8001


class LocalWebServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих 
    запросов от клиентов."""
    
    def get_context_data(self):
        file_name = "index.html"
        with open(file_name, mode="r", encoding="UTF-8") as data:
            context = data.read()
            return context

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(self.get_context_data(), "UTF-8"))

if __name__ == "__main__":        
    web_server = HTTPServer((host_name, server_port), LocalWebServer)
    print(f"Server started http://{host_name}:{server_port}")
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass
    web_server.server_close()
    print("Server stopped.")
