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
                        <img src="https://lh3.googleusercontent.com/AcCnZOCJ0XGI-7-kClWMbe1vBvYqX8fbkylC3ZRv2e40PKec9VTNlsmh86NZ-G4Mq33Vd97pjX2EIelXT_rBTPbq2fJjJxWWPIX-izGCpAQtieQNxhkCafBbQ_muyz6bgsMTM2V1ahsvOr8BlApkZ0PX0URUISpSaF9iWzqX5y-SfkzomblHpGbzZ58Vi28ihUTgXadchapHhiBDiqdscpwXG057nHB5DJ0WCdU51uUWqC0UI2EXsKkK7kDOAEDGCtGOnc0Wkq_C_Ss7xNafmoLLlQbzd42HI9tPuWsEEG-TdjiyonbfN-ZOgd9S4sLHSTXTjMHoo-xAUSb-BR00LMiFQP7X6NNd_MaYqW-FDaDkjEKv8dxSMrPox8ZRDZnML2o7M4fhQ1mdam8MpxakSoSv2fXbGEBAG6lUCbO_--I-KnofQJI9T67LxbJWn0iZhR-GZm5aPZtlQGte6_EBcpYmSSK8sOtUmy7GEi5V43Q7d-X9qUKMqtccEEPKDqunUEEAO42rWx3JwPyQ0FvcmOa0kxS0FWQP7-Vqzjs-8aHnZG3J0VAV3EyVu8MbF71M4N39UAZkjkSMzMYUBYqVr-hkIIbnXuchvMYaM5HCLiQIooB5s4KfqRM_AtAiePlGPyYfNXY08uPyjfp6U2tvWrqXewEcs4NqYO9gjNWy_dpiC9VBIQ_3tq_p=w467-h108-no" align="middle">
                        <form method="post">
                            <input type="text" name="query" size="47">
                            <input type="submit" value="Search">
                            <br>
                            <br>
                            <label>show
                            <input type="text" name="limit" placeholder="limit" size="5">
                            </label>
                            <label>documents starting from
                            <input type="text" name="offset" placeholder="offset" size="5">
                            </label>
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
        form = cgi.FieldStorage(fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'})
        print("got form")
        query = str(form.getvalue("query"))
        limit = form.getvalue("limit")
        offset = form.getvalue("offset")
        if not limit:
            limit = 10
        else:
            limit = int(limit)
        if not offset:
            offset = 0
        else:
            offset = int(offset)
        se = SearchEngine("tolstoy_db")
        print(query)
        result = se.search_to_sentence(query)
        print(result)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <img src="https://lh3.googleusercontent.com/AcCnZOCJ0XGI-7-kClWMbe1vBvYqX8fbkylC3ZRv2e40PKec9VTNlsmh86NZ-G4Mq33Vd97pjX2EIelXT_rBTPbq2fJjJxWWPIX-izGCpAQtieQNxhkCafBbQ_muyz6bgsMTM2V1ahsvOr8BlApkZ0PX0URUISpSaF9iWzqX5y-SfkzomblHpGbzZ58Vi28ihUTgXadchapHhiBDiqdscpwXG057nHB5DJ0WCdU51uUWqC0UI2EXsKkK7kDOAEDGCtGOnc0Wkq_C_Ss7xNafmoLLlQbzd42HI9tPuWsEEG-TdjiyonbfN-ZOgd9S4sLHSTXTjMHoo-xAUSb-BR00LMiFQP7X6NNd_MaYqW-FDaDkjEKv8dxSMrPox8ZRDZnML2o7M4fhQ1mdam8MpxakSoSv2fXbGEBAG6lUCbO_--I-KnofQJI9T67LxbJWn0iZhR-GZm5aPZtlQGte6_EBcpYmSSK8sOtUmy7GEi5V43Q7d-X9qUKMqtccEEPKDqunUEEAO42rWx3JwPyQ0FvcmOa0kxS0FWQP7-Vqzjs-8aHnZG3J0VAV3EyVu8MbF71M4N39UAZkjkSMzMYUBYqVr-hkIIbnXuchvMYaM5HCLiQIooB5s4KfqRM_AtAiePlGPyYfNXY08uPyjfp6U2tvWrqXewEcs4NqYO9gjNWy_dpiC9VBIQ_3tq_p=w467-h108-no" align="middle">
                        <form method="post">
                            <input type="text" name="query" value="%s" size="47"/>
                            <input type="submit" value="Search"/>
                            <br>
                            <br>
                            <label>show
                            <input type="text" name="limit" placeholder="limit" size="5" value="%d"/>
                            </label>
                            <label>documents starting from
                            <input type="text" name="offset" placeholder="offset" size="5" value="%d"/>
                            </label>
                        """ % (query, limit, offset), encoding="UTF-8"))
        self.wfile.write(bytes("<ol>", encoding="UTF-8"))
        if not result:
            self.wfile.write(bytes("Nothing found", encoding="UTF-8"))
        for n, f in enumerate(result):
            if n >= offset and n < limit+offset:
                d_lim = form.getvalue("doc%dlimit" % n)
                d_off = form.getvalue("doc%doffset" % n)
                if not d_lim:
                    d_lim = 3
                else:
                    d_lim = int(d_lim)
                if not d_off:
                    d_off = 0
                else:
                    d_off = int(d_off)
                self.wfile.write(bytes("<li><p>%s</p></li>" % f, encoding="UTF-8"))
                self.wfile.write(bytes("""
                        <label>show
                        <input type="text" name="doc%dlimit" placeholder="limit" value="%d" size="5"/>
                        </label>
                        <label> quotes starting from
                        <input type="text" name="doc%doffset" placeholder="offset" value="%d" size="5"/>
                        </label>
                        """ % (n, d_lim, n, d_off), encoding="UTF-8"))
                self.wfile.write(bytes("<ul>", encoding="UTF-8"))
                for m, window in enumerate(result[f]):
                    if m >= d_off and m < d_off + d_lim:
                        quote = window.cut_and_highlight()
                        self.wfile.write(bytes("<li><p>%s</p></li>" % quote,
                                           encoding="UTF-8"))
                    if m == d_off + d_lim:
                        break
                self.wfile.write(bytes("</ul>", encoding="UTF-8"))
            if n == limit+offset:
                break
        self.wfile.write(bytes("""</ol></form></body></html>""", encoding="UTF-8"))
        

def main():
    server = HTTPServer(('', 80), SearchRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
