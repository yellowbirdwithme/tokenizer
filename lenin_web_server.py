"""
This module implements an HTTP server for serving Search Engine.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from lenin_search_engine import SearchEngine, Context


class SearchRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Creates a simple HTML page with a field and a button.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="UTF-8"))

    def do_POST(self):
        """
        Seends search results in response to the search query.
        """
        print("here")
        form = cgi.FieldStorage(fp = self.rfile,
                            headers = self.headers,
                            environ ={'REQUEST_METHOD':'POST'})
        print("got form")
        query = str(form.getvalue("query"))
        se = SearchEngine("tolstoy_db")
        print(query)
        result = se.search_to_sentence(query)
        print(result)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
            <body>
                <form method="post">
                    <input type="text" name="query" value="%s"/>
                    <input type="submit" value="Search"/>
                </form>""" % query, encoding="UTF-8"))
        self.wfile.write(bytes("<ol>", encoding="UTF-8"))
        for f in result:
            self.wfile.write(bytes("<li><p>%s</p></li>" % f, encoding="UTF-8"))
            self.wfile.write(bytes("<ul>", encoding="UTF-8"))
            for window in result[f]:
                quote = window.cut_and_highlight()
                self.wfile.write(bytes("<li><p>%s</p></li>" % quote,
                                       encoding="UTF-8"))
            self.wfile.write(bytes("</ul>", encoding="UTF-8"))
        self.wfile.write(bytes("</ol>", encoding="UTF-8"))         
        

def main():
    server = HTTPServer(('', 80), SearchRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
