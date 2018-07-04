import datetime
import traceback


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
            try:

                # Abrindo arquivos coletados pelo crawler
                with open('invertido/{0}/{1}.html'.format(str(selected_file), str(number_visited))) as file:
                    end_word = ""
                    for line in file:
                        for word in line:
                            if word != " " and word != '\n':
                                end_word = end_word + word
                            else:
                                if end_word != "":
                                    print(end_word)
                                    end_word = ""

            except:
                pass

    if __name__ == '__main__':

        inicio = (datetime.datetime.now().time())
        sites = 1
        print("inicio remover html")
        #while (sites < 7):
        #    print(sites, datetime.datetime.now().time())
        #    remover_html(sites)
        #    sites = sites + 1
        criando_arquivo(1)
        fim = (datetime.datetime.now().time())
        print("inicio", inicio, "fim", fim)
