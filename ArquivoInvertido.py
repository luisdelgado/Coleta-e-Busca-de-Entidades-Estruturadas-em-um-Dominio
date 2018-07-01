import datetime


class ArquivoInvertido:

    def remover_html(selected_file, number_visited):
        with open('arquivos/' + str(selected_file) + '/otimizado/' + str(number_visited) + ".html") as file:
            data = file.read()
            print(data)

    if __name__ == '__main__':

        inicio = (datetime.datetime.now().time())
        remover_html(1, 1)
        fim = (datetime.datetime.now().time())
        print(inicio, fim)
