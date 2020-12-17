# Pré-requisitos
- [Python 3](https://www.python.org/downloads/)

# Como utilizar
1) Clonar o repositório localmente para sua máquina ```git clone ...```
2) Acessar a pasta onde o repositório foi clonado
3) Inicializar a aplicação usando o comando:
    ```
    python3 main.py
    ```
4) Um menu com as opções serão exibidas. 
   
   Por exemplo, para salvar um dado, escolher a opção:
   ``` 
   set
   ```
   Em seguida, digite o valor da chave e logo depois o valor do dado que deseja salvar

# Arquitetura
Os dados do banco de dados ficam salvos em arquivos de segmento do tipo append-only que ficam salvos no diretório ```data```. O tamanho máximo de um segmento é definido por um paramêtro alteravel dentro da aplicação pelo menu (o valor default é 50 bytes).

Os processos de compactação dos segmentos e merge podem ser inciados por dentro do menu da aplicação e são exibidos sempre o antes e o depois dos processos.

Para algumas operações, uma pasta ```temp``` é criada no diretório.