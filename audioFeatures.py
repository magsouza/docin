import librosa.display
import numpy as np
import pygame
import math
import random

class AudioFeatures:
    
    def __init__(self):

        '''
        Construtor de um objeto AudioFeatures, não toma parâmetros de entrada.

        Inicializa os atributos frequencies_index_ratio e time_index_ratio ambos
        do tipo inteiro com o valor 0, pois ainda não carregou nenhum arquivo
        de audio. 
        
        Atributo spectogram -> tipo numpy array
        Atributo spec_lines -> dicionário de numpy arrays, chaves são os espectros
                               de audio, conteúdo são numpy arrays de cada faixa desses
                               espectros
        '''

        self.frequencies_index_ratio = 0 
        self.time_index_ratio = 0
        self.spectrogram = None
        self.spec_lines = {}

    def load(self, filename):
        time_series, sample_rate = librosa.load(filename)
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
        self.frequencies = librosa.core.fft_frequencies(n_fft=2048*4)
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
        self.time_index_ratio = len(times)/times[len(times) - 1]
        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]
    
    def ger_spec_lines(self):
        limits = {'sub_bass': {'start': 0, 'stop': 60},
                  'bass': {'start': 60, 'stop': 250},
                  'low_midrange': {'start': 250, 'stop': 500},
                  'midrange': {'start': 500, 'stop': 2000},
                  'upper_midrange': {'start': 2000, 'stop': 4000},
                  'presence': {'start': 4000, 'stop': 6000},
                  'brilliance': {'start': 6000, 'stop': 20000}}
        
        for l in limits:
            aux = [(i >= limits[l]['start'] and i < limits[l]['stop']) for i in self.frequencies]
            self.spec_lines[l] = self.spectrogram[aux]

    def get_decibel(self, target_time, spectro, freq):
        #freq
        #return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]
        return self.spec_lines[spectro][freq][int(target_time*self.time_index_ratio)]

    def get_decibels(self, target_time, spectro, freqs):
        decibels = []
        for f in freqs:
            decibels.append(self.get_decibel(target_time, spectro, f))

        return decibels

    def get_random_freq(self, spectro):
        s = self.spec_lines[spectro]
        l = len(s)
        r = random.randint(0, l-1)
        return r

    def get_freqs(self, n, spectro):
        freqs = []
        for i in range(n):
            freq = self.get_random_freq(spectro)
            freqs.append(freq)
        return freqs


def main():
    filename = "musics/Kiss Me More.wav"
    extractor = AudioFeatures()
    extractor.load(filename)
    
    m = []
    for f in extractor.spectrogram:
        m.append(max(f))
    print(max(m))
    #teste = extractor.spectrogram[:3]
    #teste = teste[[True, False, True]]
    extractor.ger_spec_lines()
    for r in extractor.spec_lines:
        print(f"Nº de faixas do tipo {r.upper()}: {len(extractor.spec_lines[r])}")
        aux = extractor.get_random_freq(r)
        print(aux)



    '''pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)
    i = 0
    aux = 0
    
    while True:
        j = extractor.get_decibel(pygame.mixer.music.get_pos() / 1000.0, 'midrange', 1)
        if j != aux:
            print(j)
        aux = j
        i += 1
'''
if __name__ == '__main__':
    main()