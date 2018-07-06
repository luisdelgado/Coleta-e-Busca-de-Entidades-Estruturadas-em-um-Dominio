# Coleta-e-Busca-de-Entidades-Estruturadas-em-um-Dominio
O projeto consiste em localizar páginas relevantes, detectar páginas com instâncias e extrair instâncias com seus valores e atributos.

# Execução

  * Para rodar o crawler:
    * Configurações: 
      * Para configurar o crawler, basta configurar a função crawler que é chamada no Main do arquivo Crawler.py.
      * Por padrão, estão as seguintes opções: crawler(inputSite, pasta, proibido, 1000, True, ["location", "salary"], True). 
      * Sendo :
        * inputSite: site inicial. Por padrão, o programa tem 6 sites iniciais e as configurações estão voltadas para eles, mas é possível trocá-los e se alterar as configurações respectivas para eles, o programa funcionará.
        * pasta: pasta de destino nas quais as páginas serão colocadas. Por padrão, o programa tem 6 sites iniciais e suas respectivas páginas destino mapeadas.
        * proibido: contém as configurações de robots.txt. Elas estão especificadas para os sites padrões.
        * 1000: número máximo de páginas a serem visitadas por site.
        * True: ativa ou desativa o WebSearch
        * [“location”, “salary”]: serve para fazer uma simples classificação de relevância sobre as páginas. Coloque palavras que você acredita que sejam relevantes de encontrar na página.
        * True: ativa ou desativa o weight para o crawler. Esse serve para dar um peso maior de relevância para as páginas que são consideradas relevantes.
    * Run Crawler.py

  * Para criar o Arquivo Invertido
    * Já existe um arquivo invertido criado. Se você desejar criar um novo, lembre-se sempre de apagar o conteúdo do arquivo.txt, mas não apague o arquivo, que se encontra na pasta “invertido” antes de executar o próximo passo (Run ArquivoInvertido.py).
    * Run ArquivoInvertido.py

  * Para fazer uma consulta
    * Run ProcessamentoConsulta.py e siga as instruções que aparecerem na tela.

