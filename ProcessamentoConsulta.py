class ProcessamentoConsulta:

    def processamento_consulta(self):
        pass

    def tratar_resposta(consulta, resposta):

        documentos = ""
        if resposta == "":
            resposta = "Infelizmente não foi encontrado nenhum documento para a sua consulta."
            documentos = resposta
        else:
            for line in resposta.splitlines():
                if line.find(consulta) > -1:
                    line = line.split(' ', 1)
                    documentos = documentos + line[1] + " - "

        return documentos

    if __name__ == '__main__':

        # Iteração com linha de comando
        consulta = input("Digite sua consulta: ")

        # Realizando consulta no arquivo invertido
        resposta = ""
        with open('invertido/arquivo.txt') as file:
            for line in file:
                if line.find(consulta) > -1:
                    resposta = resposta + line

        # Retornar apenas documentos que tem o termo
        resposta = tratar_resposta(consulta, resposta)

        print("\n" + consulta, "foi encontrado nos seguintes documentos:")
        print(resposta)
