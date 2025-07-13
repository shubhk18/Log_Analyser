import http.server
import socketserver
import os

PORT = 8000
LOG_FILES_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_LOG_FILES = [
    "mysql_connection.log",
    "mysql_connection_detailed.log",
]

class LogServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/log/'):
            log_file_name = self.path[5:]
            if log_file_name in ALLOWED_LOG_FILES:
                log_file_path = os.path.join(LOG_FILES_DIR, log_file_name)
                if os.path.exists(log_file_path):
                    try:
                        with open(log_file_path, 'r') as f:
                            log_content = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(log_content.encode('utf-8'))
                    except Exception as e:
                        self.send_error(500, f"Error reading log file: {e}")
                else:
                    self.send_error(404, "Log file not found on server.")
            else:
                self.send_error(403, "Access to this log file is forbidden.")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Log Server</h1><p>Use /log/&lt;log_filename&gt; to get log content.</p>")
            self.wfile.write(b"<p>Allowed files:</p><ul>")
            for f in ALLOWED_LOG_FILES:
                self.wfile.write(f"<li><a href='/log/{f}'>{f}</a></li>".encode('utf-8'))
            self.wfile.write(b"</ul>")


with socketserver.TCPServer(("", PORT), LogServer) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Use http://localhost:{PORT}/log/mysql_connection.log to access the log.")
    httpd.serve_forever()
