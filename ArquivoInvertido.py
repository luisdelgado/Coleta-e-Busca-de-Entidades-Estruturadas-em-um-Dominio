import datetime


class ArquivoInvertido:

    def remover_html(selected_file, number_visited):

        # Abrindo arquivos coletados pelo crawler
        with open('arquivos/' + str(selected_file) + '/otimizado/' + str(number_visited) + ".html") as file:
            for line in file:

                # Verificando a existência de tags para removê-las dos arquivos finais
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
                print(line)

    if __name__ == '__main__':

        inicio = (datetime.datetime.now().time())
        remover_html(1, 1)
        fim = (datetime.datetime.now().time())
        print(inicio, fim)
