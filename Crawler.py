from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

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
        self.feed(htmlString)
        return htmlString, self.links


def crawler(url, maxPages, otimizacao):
    pagesToVisit = [url]
    numberVisited = 0
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        try:
            data, links = parser.getLinks(url)

            # Verificando se o link já está em pagesToVisit para poder adiciona-lo
            if (otimizacao):
                for link in links:
                    # Se tiver, remove ele de links
                    if not (link in pagesToVisit):
                        pagesToVisit.append(link)
            else:
                pagesToVisit = pagesToVisit + links

        except:
            print("Erro!")
        print(pagesToVisit)

if __name__ == '__main__':
    crawler("https://www.vagalume.com.br/", 10, True);