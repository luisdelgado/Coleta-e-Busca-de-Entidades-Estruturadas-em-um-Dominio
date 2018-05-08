from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import traceback
import datetime
import time


class LinkParser(HTMLParser):
    inlink = False
    newUrl = ""

    # Verificando tags do HTML
    def handle_starttag(self, tag, attr):
        if tag.lower() == "a":
            for (k, v) in attr:
                if k.lower() == "href":
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
        #print(url)
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        if htmlString.find("text/html"):
            self.feed(htmlString)
            return htmlString, self.links, self.ancoras
        else:
            return "", [], []


def crawler(url_inicial, selectedfile, prohibition, maxpages, websearch, webanalytics, weight):
    if weight:
        pagesToVisit = [(url_inicial, 0)]
    else:
        pagesToVisit = [url_inicial]

    numberVisited = 0
    new_link = True
    corretos = 0

    # Timer
    old_time = 0
    while numberVisited < maxpages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        if weight:
            url, linkweight = pagesToVisit[0]
        else:
            url = pagesToVisit[0]

        pagesToVisit = pagesToVisit[1:]

        # Removendo páginas que nunca serão visitadas
        if (maxpages - numberVisited) < len(pagesToVisit):
            new_link = False
            not_used = len(pagesToVisit) - (maxpages - numberVisited)
            pagesToVisit = pagesToVisit[:-not_used]

        # progresso
        print(numberVisited*100 / maxpages, "%")
        #print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        found_word = False

        # Verificando o robots
        linkproibido = False
        for prohibitionWord in prohibition:
            if url.find(prohibitionWord) > -1:
                linkproibido = True

        if not linkproibido:
            try:

                # Setando para esperar pelo menos 1 segundo entre cada consulta ao  site
                current_time = datetime.datetime.now().strftime('%S.%f')[:-4]
                if float(current_time) - float(old_time) < 1:
                    time.sleep(1)

                data, links, ancoras = parser.getLinks(url)
                old_time = datetime.datetime.now().strftime('%S.%f')[:-4]

                # Verificando se é baseline
                if websearch:

                    # Escrevendo no arquivo
                    f = open('arquivos/' + str(selectedfile) + '/otimizado/' + str(numberVisited) + ".html", 'w+')
                    f.write(str(data))
                else:

                    # Escrevendo no arquivo
                    f = open('arquivos/' + str(selectedfile) + '/' + str(numberVisited) + ".html", 'w+')
                    f.write(str(data))

                # Verificando relevancoa do site
                if data.find(webanalytics[0]) > -1:
                    if data.find(webanalytics[1]) > -1:
                        corretos = corretos + 1

                # Verificando se o link já está em pagesToVisit para poder adiciona-lo
                if websearch:
                    for idx, link in enumerate(links):

                        if webanalytics:

                            # Verificando se weight está ativado
                            if weight:
                                word_count = 0

                                # Verificando se as palavras estão no conteudo da página para adicionar links
                                for word in webanalytics:
                                    if link.find(word) > -1:
                                        word_count = word_count + 1
                                    else:
                                        if ancoras:
                                            if ancoras[idx] != None:
                                                if ancoras[idx].find(word) > -1:
                                                    word_count = word_count + 1

                                pagesToVisit = weight_link_insert(link, word_count, pagesToVisit, url_inicial)

                            else:

                                # Verificando se as palavras estão no conteudo da página para adicionar links
                                for word in webanalytics:
                                    if link.find(word) > -1:
                                        found_word = True
                                    else:
                                        if ancoras:
                                            if ancoras[idx] != None:
                                                if ancoras[idx].find(word) > -1:
                                                    found_word = True

                                if found_word:

                                    # Se tiver e não pertencer ao link inicial, não adiciona ele em links
                                    if link not in pagesToVisit and link.find(url_inicial) > -1:
                                        pagesToVisit.append(link)

                        else:

                            # Se tiver e não pertencer ao link inicial, não adiciona ele em links
                            if link not in pagesToVisit and link.find(url_inicial) > -1:
                                pagesToVisit.append(link)

                else:

                    # Verificando se ainda deve adicionar links
                    if new_link:
                        for link in links:

                            # Se pertencer ao link inicial
                            if link.find(url_inicial) > -1:
                                pagesToVisit = pagesToVisit + links

            except:
                pass
                #print(traceback.print_exc())

        #print(pagesToVisit)

    print(corretos)


def weight_link_insert(link, word_count, pages_to_visit, url_inicial):

    # Verificando se pagesToVisit está vazia
    if len(pages_to_visit):

        for idx, page in enumerate(pages_to_visit):
            url, url_weight = pages_to_visit[idx]

            # Verificando se o peso do novo link é maior que o link atual
            if word_count > url_weight:

                # Se pertencer ao link inicial, adiciona link em pagesToVisit
                if link.find(url_inicial) > -1:
                    pages_to_visit.insert(0, (link, word_count))
                    break

            # Para último elemento da lista
            if len(pages_to_visit) == idx+1:

                # Se pertencer ao link inicial, adiciona link em links
                if link.find(url_inicial) > -1:
                    pages_to_visit = pages_to_visit + [(link, word_count)]

    else:

        if link.find(url_inicial) > -1:
            pages_to_visit = pages_to_visit + [(link, word_count)]

    return pages_to_visit


def verificando_site(site):

    # Verificando pasta do site
    if site == "https://www.usajobs.gov/":
        return 1
    if site == "https://www.ziprecruiter.com/":
        return 2
    if site == "https://www.indeed.co.uk/":
        return 3
    if site == "http://www.jobs.ac.uk/":
        return 4
    if site == "https://www.reed.co.uk/":
        return 5
    if site == "https://www.totaljobs.com/":
        return 6
    return 0


def robots(filenumber):

    # Lendo robots do site selecionado
    f = open('robots/' + str(filenumber) + '.txt', 'r')
    strings = list(f)
    robotsstrings = list(map(lambda x: x.strip(), strings))
    return robotsstrings


if __name__ == '__main__':
    inicio = (datetime.datetime.now().time())
    print("inicio total", inicio)

    # sites = ["https://www.usajobs.gov/", 'https://www.ziprecruiter.com/', "https://www.indeed.co.uk/",
    #          "http://www.jobs.ac.uk/", "https://www.reed.co.uk/", "https://www.totaljobs.com/"]
    sites = ["https://www.totaljobs.com/"]

    for site in sites:
        inicioSite = (datetime.datetime.now().time())
        print("inicio site", inicioSite)
        print(site)
        inputSite = site
        pasta = verificando_site(inputSite)
        proibido = robots(pasta)
        crawler(inputSite, pasta, proibido, 1000, True, ["location", "salary"], True)
        fimSite = (datetime.datetime.now().time())
        print(site, inicioSite, fimSite)

    fim = (datetime.datetime.now().time())
    print(inicio, fim)
