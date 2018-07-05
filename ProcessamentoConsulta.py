class ProcessamentoConsulta:

    def processamento_consulta(self):
        pass

    def tratar_resposta(resposta):

        if resposta == "":
            resposta = "Infelizmente não foi encontrado nenhum documento para a sua consulta."
            documentos = resposta
        else:
            resposta = resposta.split(' ', 1)
            documentos = resposta[1]

        return documentos

    if __name__ == '__main__':

        # Iteração com linha de comando
        consulta = input("Digite sua consulta: ")

        # Realizando consulta no arquivo invertido
        resposta = ""
        with open('invertido/arquivo.txt') as file:
            for line in file:
                if line.find(consulta) > -1:
                    resposta = line
                    break

        # Retornar apenas documentos que tem o termo
        resposta = tratar_resposta(resposta)

        print("\n" + consulta, "foi encontrado nos seguintes documentos:")
        print(resposta)
