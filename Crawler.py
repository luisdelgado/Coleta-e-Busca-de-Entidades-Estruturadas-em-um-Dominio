from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import traceback

class LinkParser(HTMLParser):
    inlink = False
    newUrl = "";

    # Verificando tags do HTML
    def handle_starttag(self, tag, attr):
        if tag.lower() == "a":
            for (k, v) in attr:
                if (k.lower() == "href"):
                    self.newUrl = parse.urljoin(self.baseUrl, v)
                    self.inlink = True

    def handle_endtag(self, tag):
        if tag.lower() == "a":
            self.inlink = False


    def handle_data(self, data):
        if self.inlink:
            self.ancoras = self.ancoras + [data]
        else:
            self.ancoras = self.ancoras + [""]

        if self.newUrl != "":
            self.links = self.links + [self.newUrl]

    # Obtendo links que crawler() chamara
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        self.ancoras = []
        print(url)
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        if htmlString.find("text/html"):
            self.feed(htmlString)
            return htmlString, self.links, self.ancoras
        else:
            return "", [], []


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
            data, links, ancoras = parser.getLinks(url)

            # Escrevendo no arquivo
            f = open('arquivos/1/' + str(numberVisited) + ".html", 'w+')
            f.write(str(data))

            # Verificando se o link já está em pagesToVisit para poder adiciona-lo
            if webSearch:
                for idx, link in enumerate(links):

                    if webAnalytics!=[]:

                        # Verificando se as palavras estão no conteudo da página para adicionar links
                        for word in webAnalytics:
                            if link.find(word) > -1:
                                foundWord = True
                            else:
                                if ancoras:
                                    if ancoras[idx] != None:
                                        if ancoras[idx].find(word) > -1:
                                            foundWord = True

                        if foundWord:

                            # Se tiver, não adiciona ele em links
                            if link not in pagesToVisit:
                                pagesToVisit.append(link)

                    else :

                        # Se tiver, não adiciona ele em links
                        if link not in pagesToVisit:
                            pagesToVisit.append(link)

            else:
                pagesToVisit = pagesToVisit + links

        except:
            print(traceback.print_exc())
        print(pagesToVisit)

if __name__ == '__main__':
    crawler("http://www.jobs.com/", 20, True, ["curriculo"]);