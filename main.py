from db_objects import Db

db = Db()
db.populate_index()

while True:
    print('Qual operação deseja realizar?')
    print(' * set           - Inserir ou atualizar um dado')
    print(' * get           - Retorna um dado dado uma chave')
    print(' * show index    - Exibe a tabela hash de indice (chave, segmento, posicao)')
    print(' * show segments - Exibe os arquivos de segmento e seus respectivos tamanhos')
    print(' * segment size  - Seta o valor maximo de tamanho dos segmentos')
    print(' * compact       - Executa processo de compactacão dos segmentos')
    print(' * merge         - Execute processo de merge de segmentos')
    print(' * quit          - Sair')
    action = input('Operação: ')

    if action == 'set':
        key = input('Qual a chave? ')
        value = input('Qual o valor? ')
        db.write(key, value)

    if action == 'get':
        key = input('Qual a chave? ')
        val = db.get(key)
        if val is not None:
            print('Valor: ' + val)
        else:
            print('Chave nao encontrada no indice.')

    if action == 'show index':
        print(db.index)

    if action == 'show segments':
        db.list_segments()

    if action == 'segment size':
        print('Tamanho maximo atual de um segmento: ' + str(db.max_segment_size))
        size = input('Qual o novo valor maximo de tamanho de um segmento? ')
        db.set_segment_size(size)

    if action == 'compact':
        db.compact_segments()

    if action == 'merge':
        db.merge_segments()

    if action == 'quit' :
        break

    print()