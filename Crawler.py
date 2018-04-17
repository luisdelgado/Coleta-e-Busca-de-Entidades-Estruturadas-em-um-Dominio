from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import traceback

class LinkParser(HTMLParser):

    # Verificando tags do HTML
    def handle_starttag(self, tag, attrs):

        # Verificando presenca da tag <a> que serve de ancora para outros sites
        if tag == 'a':
            for (key, value) in attrs:

                # Combinando URL base com nova URL achada
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)

                    # Adicionando aos outros links
                    self.links = self.links + [newUrl]

    # Obtendo links que crawler() chamara
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        if htmlString.find("text/html"):
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "", []


def crawler(url, maxPages, webSearch, webAnalytics):
    pagesToVisit = [url]
    numberVisited = 0
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        foundWord = False
        try:

            # Configurando nome do arquivo
            save = url
            save = save.replace('https://', '')
            save = save.replace('http://', '')
            save = save.replace(':', '')
            if (save[-1:] == "/"):
                save = save.replace(save[-1:], '')
            save = save + ".html"
            data, links = parser.getLinks(url)

            if webAnalytics!=[]:

                # Verificando se as palavras estão no conteudo da página para adicionar links
                for word in webAnalytics:
                    if data.find(word) > -1:
                        foundWord = True

                # Escrevendo no arquivo
                f = open('arquivos/' + str(save), 'w+')
                f.write(str(data))

                # Verificando se o link já está em pagesToVisit para poder adiciona-lo
                if webSearch and foundWord:
                    for idx, link in enumerate(links):

                        # Se tiver, não adiciona ele em links
                        if link not in pagesToVisit:
                            pagesToVisit.append(link)

            else:

                # Escrevendo no arquivo
                f = open('arquivos/' + str(save), 'w+')
                f.write(str(data))

                # Verificando se o link já está em pagesToVisit para poder adiciona-lo
                if webSearch:
                    for idx, link in enumerate(links):

                        # Se tiver, não adiciona ele em links
                        if link not in pagesToVisit:
                            pagesToVisit.append(link)

                else:
                    pagesToVisit = pagesToVisit + links

        except:
            print(traceback.print_exc())
        print(pagesToVisit)

if __name__ == '__main__':
    crawler("http://www.jobs.com/", 20, False, []);