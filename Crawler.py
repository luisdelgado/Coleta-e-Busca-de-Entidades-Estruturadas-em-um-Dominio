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
        has = False
        if self.newUrl != "":
            for link in self.links:
                if link == self.newUrl:
                    has = True

            if not has:
                if self.inlink:
                    self.ancoras = self.ancoras + [data]
                else:
                    self.ancoras = self.ancoras + [""]

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


def crawler(urlInicial, maxPages, webSearch, webAnalytics, weight):
    if weight:
        pagesToVisit = [(urlInicial,0)]
    else:
        pagesToVisit = [urlInicial]

    numberVisited = 0
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited +1
        if weight:
            url, linkWeight = pagesToVisit[0]
        else:
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

                        # Verificando se weight está ativado
                        if weight:
                            wordCount = 0

                            # Verificando se as palavras estão no conteudo da página para adicionar links
                            for word in webAnalytics:
                                if link.find(word) > -1:
                                    wordCount = wordCount + 1
                                else:
                                    if ancoras:
                                        if ancoras[idx] != None:
                                            if ancoras[idx].find(word) > -1:
                                                wordCount = wordCount + 1

                            pagesToVisit = weightLinkInsert(link, wordCount, pagesToVisit, urlInicial)

                        else:

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

                                # Se tiver e não pertencer ao link inicial, não adiciona ele em links
                                if link not in pagesToVisit and link.find(urlInicial)>-1:
                                    pagesToVisit.append(link)

                    else :

                        # Se tiver e não pertencer ao link inicial, não adiciona ele em links
                        if link not in pagesToVisit and link.find(urlInicial)>-1:
                            pagesToVisit.append(link)

            else:
                for link in links:

                    # Se pertencer ao link inicial
                    if link.find(urlInicial)>-1:
                        pagesToVisit = pagesToVisit + links

        except:
            print(traceback.print_exc())
        print(pagesToVisit)

def  weightLinkInsert(link, wordCount, pagesToVisit, urlInicial):

    # Verificando se pagesToVisit está vazia
    if len(pagesToVisit):

        for idx, page in enumerate(pagesToVisit):
            url, urlWeight = pagesToVisit[idx]

            # Verificando se o peso do novo link é maior que o link atual
            if wordCount > urlWeight:

                # Se pertencer ao link inicial, adiciona link em pagesToVisit
                if link.find(urlInicial)>-1:
                    pagesToVisit.insert(0, (link,wordCount))
                    break

            # Para último elemento da lista
            if len(pagesToVisit) == idx+1:

                # Se pertencer ao link inicial, adiciona link em links
                if link.find(urlInicial)>-1:
                    pagesToVisit = pagesToVisit + [(link,wordCount)]

    else:

        if link.find(urlInicial)>-1:
            pagesToVisit = pagesToVisit + [(link,wordCount)]

    return pagesToVisit


if __name__ == '__main__':
    crawler("http://www.jobs.com/", 20, True, ["jobs","indiana"], True);