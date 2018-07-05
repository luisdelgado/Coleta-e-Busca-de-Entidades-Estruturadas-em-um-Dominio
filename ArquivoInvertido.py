import datetime
from collections import OrderedDict
import threading


def my_thread1():
    criando_arquivo(1)


def my_thread3():
    criando_arquivo(3)


def my_thread4():
    criando_arquivo(4)


def my_thread5():
    criando_arquivo(5)


def my_thread6():
    criando_arquivo(6)


def verificar_palavra(selected_file, number_visited, end_word):
    searched = False
    end_file = ""
    number_document = str(selected_file) + str(number_visited)
    with open('invertido/' + str(selected_file) + '/arquivo.txt') as file:
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
    f = open('invertido/' + str(selected_file) + '/arquivo.txt', 'w+')
    f.write(str(end_file))
    f.close()


class ArquivoInvertido:

    def arquivo_invertido(self):
        pass

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
            print(selected_file, number_visited / 10, "%")

def ordenar_arquivo(selected_file):
        end_file = ""

        # Ordendando arquivo
        with open('invertido/' + str(selected_file) + 'arquivo.txt') as file:
            lines = sorted(file.readlines())

            # Transformando de lista para um modo melhor de visualização
            contador = 1
            while contador < len(lines):
                end_file = end_file + lines[contador]
                contador = contador + 1

        # Escrevendo no arquivo
        f = open('invertido/' + str(selected_file) + 'arquivo.txt', 'w+')
        f.write(str(end_file))
        f.close()

if __name__ == '__main__':

        inicio = (datetime.datetime.now().time())
        sites = 1
        print("inicio remover html")
        while sites < 7:
            print("site:", sites, datetime.datetime.now().time())
            remover_html(sites)
            sites = sites + 1

        print("inicio criando arquivo invertido", datetime.datetime.now().time())
        t1 = threading.Thread(target=my_thread1, args=[])
        t3 = threading.Thread(target=my_thread3, args=[])
        t4 = threading.Thread(target=my_thread4, args=[])
        t5 = threading.Thread(target=my_thread5, args=[])
        t6 = threading.Thread(target=my_thread6, args=[])
        t1.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        print("inicio ordenando arquivo invertido", datetime.datetime.now().time())
        #ordenar_arquivo(selected_file)

        fim = (datetime.datetime.now().time())
        print("inicio", inicio, "fim", fim)
