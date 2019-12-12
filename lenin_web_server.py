"""
This module implements an HTTP server for serving Search Engine.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import time
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
                            <input type="submit" name="search" value="Search">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="UTF-8"))

    def do_POST(self):
        """
        Seends search results in response to the search query.
        """
        form = cgi.FieldStorage(fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'})
        print("got form")
        query = str(form.getvalue("query"))
        se = SearchEngine("tolstoy_db")
        print(query)
        limit = form.getvalue("limit")
        if limit:
            limit = int(limit)
        else:
            limit = 10
        quotelimit = []
        for n in range(limit):
            lim = form.getvalue("limit%d" % n)
            if lim:
                lim = int(lim)
            else:
                lim = 3
            quotelimit.append(lim)

        #identifying type of request
        request = find_pressed_button(form, limit)
        if request == "search":
            if form.getvalue("prevsearch") == query:
                docpage, quotepage = get_pages(form, limit)
            else:
                docpage = 0
                quotepage = [0 for i in range(limit)]
            doclo = []
            for i, lim in enumerate(quotelimit):
                doclo.append((lim + 1, lim*quotepage[i]))
            start_time = time.time()
            result = se.search_to_quote_gen(query, limit=limit + 1, doclo=doclo)
            print("time ", (time.time() - start_time))
        else:
            docpage, quotepage = get_pages(form, limit)
            if request.startswith("action"):
                docpage, quotepage = update_pages(form, request, docpage, quotepage)
            doclo = []
            for i, lim in enumerate(quotelimit):
                doclo.append((lim + 1, lim*quotepage[i]))
            start_time = time.time()
            result = se.search_to_quote_gen(query,
                                              limit=limit + 1,
                                              offset=docpage * limit,
                                              doclo=doclo)
            print("time ", (time.time() - start_time))
            
        #response page
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        #top of the page
        self.wfile.write(bytes("""
                <html>
                    <body>
                        <img src="https://lh3.googleusercontent.com/AcCnZOCJ0XGI-7-kClWMbe1vBvYqX8fbkylC3ZRv2e40PKec9VTNlsmh86NZ-G4Mq33Vd97pjX2EIelXT_rBTPbq2fJjJxWWPIX-izGCpAQtieQNxhkCafBbQ_muyz6bgsMTM2V1ahsvOr8BlApkZ0PX0URUISpSaF9iWzqX5y-SfkzomblHpGbzZ58Vi28ihUTgXadchapHhiBDiqdscpwXG057nHB5DJ0WCdU51uUWqC0UI2EXsKkK7kDOAEDGCtGOnc0Wkq_C_Ss7xNafmoLLlQbzd42HI9tPuWsEEG-TdjiyonbfN-ZOgd9S4sLHSTXTjMHoo-xAUSb-BR00LMiFQP7X6NNd_MaYqW-FDaDkjEKv8dxSMrPox8ZRDZnML2o7M4fhQ1mdam8MpxakSoSv2fXbGEBAG6lUCbO_--I-KnofQJI9T67LxbJWn0iZhR-GZm5aPZtlQGte6_EBcpYmSSK8sOtUmy7GEi5V43Q7d-X9qUKMqtccEEPKDqunUEEAO42rWx3JwPyQ0FvcmOa0kxS0FWQP7-Vqzjs-8aHnZG3J0VAV3EyVu8MbF71M4N39UAZkjkSMzMYUBYqVr-hkIIbnXuchvMYaM5HCLiQIooB5s4KfqRM_AtAiePlGPyYfNXY08uPyjfp6U2tvWrqXewEcs4NqYO9gjNWy_dpiC9VBIQ_3tq_p=w467-h108-no" align="middle">
                        <form method="post">
                            <input type="text" name="query" value="%s" size="47"/>
                            <input type="submit" name="search" value="Search"/>
                            <input type="hidden" name="prevsearch" value="%s">
                            <br>
                            <br>
                            """ % (query, query), encoding="UTF-8"))
        if  not docpage:
            self.wfile.write(bytes("""
                            <input type="submit" name="action" value="First" disabled/>
                            <input type="submit" name="action" value="Previous" disabled/>
                            """, encoding="UTF-8"))
        else:
            self.wfile.write(bytes("""
                            <input type="submit" name="action" value="First"/>
                            <input type="submit" name="action" value="Previous"/>
                            """, encoding="UTF-8"))
        if len(result) < limit+1:
            self.wfile.write(bytes("""
                            <input type="submit" name="action" value="Next" disabled/>
                            """, encoding="UTF-8"))
        else:
            self.wfile.write(bytes("""
                            <input type="submit" name="action" value="Next"/>
                            """, encoding="UTF-8"))
        self.wfile.write(bytes("""
                            <label> show
                            <input type="number" min="0" step="1"  name="limit" value="%d" size="5">
                            documents on page</label>
                            <input type="hidden" name="docpage" value="%d">
                        """ % (limit, docpage), encoding="UTF-8"))
        
        self.wfile.write(bytes("""<ol start="%d">""" % (docpage * limit + 1),
                               encoding="UTF-8"))
        if not result:
            self.wfile.write(bytes("Nothing found", encoding="UTF-8"))
            
        #documents with quotes
        for n, f in enumerate(result):
            if n == limit:
                break
            self.wfile.write(bytes("<li><p>%s</p></li>" % f, encoding="UTF-8"))
            if not quotepage[n]:
                self.wfile.write(bytes("""
                    <input type="submit" name="action%d" value="First" disabled/>
                    <input type="submit" name="action%d" value="Previous" disabled/>
                    """ % (n, n), encoding="UTF-8"))
            else:
                self.wfile.write(bytes("""
                    <input type="submit" name="action%d" value="First"/>
                    <input type="submit" name="action%d" value="Previous"/>
                    """ % (n, n), encoding="UTF-8"))
            if len(result[f]) < quotelimit[n] + 1:
                self.wfile.write(bytes("""
                    <input type="submit" name="action%d" value="Next" disabled/>
                    """ % n , encoding="UTF-8"))
            else:
                self.wfile.write(bytes("""
                    <input type="submit" name="action%d" value="Next"/>
                    """ % n , encoding="UTF-8"))
            self.wfile.write(bytes("""
                    <label> show
                    <input type="number" min="0" step="1" name="limit%d" value="%d" size="5"> 
                    quotes for this document</label>
                    <input type="hidden" name="quotepage%d" value="%d">
                    """ % (n, quotelimit[n], n, quotepage[n]), encoding="UTF-8"))
            self.wfile.write(bytes("<ul>", encoding="UTF-8"))
            for m, quote in enumerate(result[f]):
                if m == quotelimit[n]:
                    break
                self.wfile.write(bytes("<li><p>%s</p></li>" % quote,
                                       encoding="UTF-8"))
            self.wfile.write(bytes("</ul>", encoding="UTF-8"))
        self.wfile.write(bytes("""</ol></form></body></html>""", encoding="UTF-8"))
        
def find_pressed_button(form, limit):
    if form.getvalue("search"):
        print("search")
        return "search"
    if form.getvalue("action"):
        return "action"
    for i in range(limit):
        key = "action" + str(i)
        if form.getvalue(key):
            return key
    return "undefined"

def update_pages(form, request, docpage, quotepage):
    #decide what page number to change
    button = form.getvalue(request)
    if request == "action":
        if button == "First":
            docpage = 0
        if button == "Previous":
            docpage -= 1
        if button == "Next":
            docpage += 1
    else:
        n = int(request[-1])
        if button == "First":
            quotepage[n] = 0
        if button == "Previous":
            quotepage[n] -= 1
        if button == "Next":
            quotepage[n] += 1
    return docpage, quotepage

def get_pages(form, limit):
    #collect current page numbers
    docpage = int(form.getvalue("docpage"))
    quotepage = []
    for n in range(limit):
        page = form.getvalue("quotepage%d" % n)
        if page:
            page = int(page)
        else:
            page = 0
        quotepage.append(page)
    return docpage, quotepage
    
def main():
    server = HTTPServer(('', 80), SearchRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()

