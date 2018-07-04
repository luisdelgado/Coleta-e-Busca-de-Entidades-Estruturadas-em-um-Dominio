import datetime
from collections import OrderedDict


def verificar_palavra(selected_file, number_visited, end_word):
    searched = False
    end_file = ""
    number_document = str(selected_file) + str(number_visited)
    with open('invertido/arquivo.txt') as file:
        for line in file:

            # Verificando se a palavra já existe no aqruivo invertido
            if not searched:
                if line.find(end_word) > -1:

                    # Verificando se ela o documento atual já foi adicionando no aqruivo invertido
                    if line.find(str(number_document)) == -1:
                        line = (line.rsplit(' ', 1))
                        line[0] = line[0] + str(" - " + str(selected_file) + str(number_visited) + " \n")
                        line = line[0]
                    searched = True

            end_file = end_file + line

        if searched:
            pass

        # Palavra não foi encontrada, adicionando ela pela primeira vez
        else:
            end_file = end_file + end_word + ': ' + str(selected_file) + str(number_visited) + " \n"

        # Removendo linhas duplicatas
        end_file = "\n".join(list(OrderedDict.fromkeys(end_file.split("\n"))))

    # Escrevendo no arquivo
    f = open('invertido/arquivo.txt', 'w+')
    f.write(str(end_file))
    f.close()


class ArquivoInvertido:

    def remover_html(selected_file):
        number_visited = 1
        while number_visited < 1000:
            try:

                # Abrindo arquivos coletados pelo crawler
                with open('arquivos/' + str(selected_file) + '/otimizado/' + str(number_visited) + ".html") as file:
                    end_file = ""
                    for line in file:

                        # Verificando a existência de tags para removê-las dos arquivos finais
                        repetition_number = 0
                        while line.find("<") > -1:
                            if line.find("<") > -1:
                                if line.find(">") > -1:
                                    new_substring = line[line.find("<"):line.find(">")+1]
                                    new_line = line.replace(new_substring, "")
                                    line = new_line
                                else:
                                    line = ""
                            else:
                                if line.find(">") > -1:
                                    line = ""
                            repetition_number = repetition_number + 1
                            if repetition_number >= 50:
                                line = ""
                        end_file = end_file + line

                    # Escrevendo no arquivo
                    f = open('invertido/' + str(selected_file) + "/" + str(number_visited) + ".html", 'w+')
                    f.write(str(end_file))

            except:
                pass

            print(number_visited / 10, "%")
            number_visited = number_visited + 1

    def criando_arquivo(selected_file):
        number_visited = 1
        while number_visited < 1000:
            word_list = []
            try:

                # Abrindo arquivos sem HTML
                with open('invertido/{0}/{1}.html'.format(str(selected_file), str(number_visited))) as file:

                    # Adicionando palavras no arquivo invertido
                    end_word = ""
                    for line in file:
                        for word in line:
                            if word != " " and word != '\n':
                                end_word = end_word + word
                            else:
                                if end_word != "":

                                    # Verificando se a palavra já apareceu nesse documento
                                    if word_list:
                                        for word_saw in word_list:
                                            if word_saw.find(end_word) == -1:
                                                verificar_palavra(selected_file, number_visited, end_word)
                                                word_list.append(end_word)
                                                break
                                    else:
                                        verificar_palavra(selected_file, number_visited, end_word)
                                        word_list.append(end_word)

                                    end_word = ""

            except:
                pass

            # Verificando andamento do programa
            number_visited = number_visited + 1
            print(number_visited / 10, "%")

    def ordenar_arquivo(end_file):

        # Ordendando arquivo
        with open('invertido/arquivo.txt') as file:
            lines = sorted(file.readlines())

        # Transformando de lista para um modo melhor de visualização
        contador = 1
        while lines[0][contador] != "]":
            if lines[0][contador] == "," and lines[0][contador - 1] != "\n":
                end_file = end_file + "\n"
            else:
                if lines[0][contador] != "'":
                    end_file = end_file + str(lines[0][contador])
            contador = contador + 1

        # Escrevendo no arquivo
        f = open('invertido/arquivo.txt', 'w+')
        f.write(str(end_file))
        f.close()

    if __name__ == '__main__':

        inicio = (datetime.datetime.now().time())
        sites = 1
        print("inicio remover html")
        while sites < 7:
            print(sites, datetime.datetime.now().time())
            remover_html(sites)
            sites = sites + 1

        sites = 1
        print("inicio criando arquivo invertido", datetime.datetime.now().time())
        while sites < 7:
            print(sites, datetime.datetime.now().time())
            criando_arquivo(sites)
            sites = sites + 1

        print("inicio ordenando arquivo invertido", datetime.datetime.now().time())
        ordenar_arquivo("")
        fim = (datetime.datetime.now().time())
        print("inicio", inicio, "fim", fim)
