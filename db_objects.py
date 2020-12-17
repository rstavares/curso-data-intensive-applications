from pathlib import Path
from os import rename
import shutil

data_dir = 'data'
temp_data_dir = 'temp'

class Db:
    index = {}
    segment_file = 1
    max_segment_size = 50

    def __init__ (self):
        Path(data_dir).mkdir(exist_ok=True)
        open(data_dir + '/' + str(self.segment_file).zfill(3),'a').close()
        self.segment_file = int(str(sorted(list(Path(data_dir).iterdir()))[-1]).split(data_dir + '/')[1])

    def write(self, key, value):
        curr_segment_size = Path(data_dir + '/' + str(self.segment_file).zfill(3)).stat().st_size
        if curr_segment_size + len(str(key)) + len(str(value)) + 1 > self.max_segment_size:
            self.segment_file += 1
        with open(data_dir + '/' + str(self.segment_file).zfill(3),'a') as f:
            f.write(key + "," + value + "\n")
        size = Path(data_dir + '/' + str(self.segment_file).zfill(3)).stat().st_size
        self.index[key] = [self.segment_file, size - len(value) - 1]
        print('Salvo.')

    def get(self, key):
        try:
            [segment_file, pos] = self.index[key]
        except:
            #print('Chave não encontrada no indice.')
            return None
        with open(data_dir + '/' + str(segment_file).zfill(3),'r') as f:
            f.seek(pos)
            return f.readline()
            #print('Valor: ' + f.readline())

    def populate_index(self):
        for x in sorted(list(Path(data_dir).iterdir())):
            #print(x)
            segment_file = int(str(x).split(data_dir + '/')[1])
            pos = 0
            with open(x,'r') as f:
                while f:
                    line = f.readline()
                    if line == '':
                        break
                    key = line.split(',')[0]
                    value = line.split(',')[1]
                    pos = f.tell() - len(value)
                    self.index[key] = [segment_file, pos]
                    #print(str(pos) + " - " + str(key) + " - " + str(value))

    def set_segment_size(self, size):
        self.max_segment_size = int(size)

    def compact_segments(self):
        print('INICIO')
        self.list_segments()
        for x in sorted(list(Path(data_dir).iterdir())):
            segment_file = int(str(x).split(data_dir + '/')[1])
            self.compact_segment(segment_file)
        print('')
        print('Processo de compactacao concluido')
        self.list_segments()

    def compact_segment(self, segment):
        if Path(temp_data_dir).exists():
            shutil.rmtree(temp_data_dir)
        Path(temp_data_dir).mkdir(exist_ok=True)
        self.populate_index()
        with open(data_dir + '/' + str(segment).zfill(3),'r') as orig_file:
            while orig_file:
                line = orig_file.readline()
                if line == '':
                    break
                key = line.split(',')[0]
                value = line.split(',')[1]
                pos = orig_file.tell() - len(value)
                #print(key + ' - ' + value + ' - ' + str(pos))
                if self.index[key][0] == segment and self.index[key][1] == pos:
                    with open(temp_data_dir + '/' + str(segment).zfill(3),'a') as new_file:
                        new_file.write(key + "," + value)
                    size = Path(temp_data_dir + '/' + str(segment).zfill(3)).stat().st_size
                    self.index[key] = [segment, size - len(value) - 1]
        if Path(temp_data_dir + '/' + str(segment).zfill(3)).is_file():
            shutil.move(temp_data_dir + '/' + str(segment).zfill(3), data_dir + '/' + str(segment).zfill(3))
       
    def merge_segments(self):
        new_index = {}
        curr_segment = 1
        if Path(temp_data_dir).exists():
            shutil.rmtree(temp_data_dir)
        Path(temp_data_dir).mkdir(exist_ok=True)
        open(temp_data_dir + '/' + str(curr_segment).zfill(3),'a').close()
        self.populate_index()
        print('INICIO')
        self.list_segments()
        for key in self.index:
            [segment, pos] = self.index[key]
            value = self.get(key)
            curr_segment_size = Path(temp_data_dir + '/' + str(curr_segment).zfill(3)).stat().st_size
            if curr_segment_size + len(str(key)) + len(str(value)) + 1 > self.max_segment_size:
                curr_segment += 1
            with open(temp_data_dir + '/' + str(curr_segment).zfill(3),'a') as f:
                f.write(key + "," + value)
            size = Path(temp_data_dir + '/' + str(curr_segment).zfill(3)).stat().st_size
            new_index[key] = [curr_segment, size - len(value)]
        #print(new_index)
        shutil.rmtree(data_dir)
        rename(temp_data_dir, data_dir)
        self.segment_file = curr_segment
        self.index = new_index
        print('')
        print('Processo de merge concluido')
        self.list_segments()
    
    def list_segments(self):
        Path(data_dir).mkdir(exist_ok=True)
        print ('Segmento - Tamanho')
        for seg in Path(data_dir).iterdir():
            print(seg.stem + " - " + str(seg.stat().st_size))