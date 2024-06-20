import string
import math
import random
import time
from copy import deepcopy

class Vigenere:
    frequence_lang={
        'french':'EAISNRTOLUDCMPGBVHFQYXJKWZ',
        'english':'ETAINOSHRDLUCMFWYGPBVKQJXZ',
    }
    def __init__(self, key:str = None):
        self.key = key.upper()

    @staticmethod
    def generate_frequence_lang(text:str, name):
        return ''.join(reversed(sorted({k:text.count(k) for k in string.ascii_uppercase}, lambda x :x[1])).keys())

    def _carre(self, char):
        index=string.ascii_uppercase.index(char)
        return string.ascii_uppercase[index:]+string.ascii_uppercase[0:index]

    def _cipher(self, key, index, char):
        return self._carre(key[index])[string.ascii_uppercase.index(char)]

    def _decipher(self, key, index, char):
        return string.ascii_uppercase[self._carre(key[index]).index(char)]

    def _process(self, payload, function):
        payload=payload.upper()
        index=0
        ret=''
        for char in payload:
            if char not in string.ascii_uppercase:
                ret+=char
            else:
                ret+=function(self.key, index, char)
                index = (index + 1)%len(self.key)
        return ret

    def cipher(self, payload):
        return self._process(payload, self._cipher)

    def decipher(self, payload):
        return self._process(payload, self._decipher)

    @staticmethod
    def generate_key(size)->str:
        return ''.join([random.choice(string.ascii_uppercase) for i in range(size)])

    @staticmethod
    def _occurences(payload:str, max_occurences=10, max_block_size = 8)->dict:
        occurences:dict = {}
        dones = []
        for i in range(max_block_size, 0, -1): # test blocks of different size
            k=0
            while k*i+i < len(payload):
                block=payload[k*i:k*i+i]
                if not block in dones:
                    dones.append(block)
                    count = payload.count(block)
                    if count > 2: # found at least two occurences of 1 block
                        occurences[block] = count
                k+=1
        occurences = sorted(occurences.items(),key = lambda x : str(len(x[0])) + str(x[1]))
        occurences.reverse()
        return dict(occurences[0:min(max_occurences, len(occurences))]) # only keep the 10 best occurences

    @staticmethod
    def _distances(payload:str,occurences:dict)->dict:
        distances = {}
        for block, count in occurences.items():
            distances[block] = []
            index=index2=0
            for i in range(count-1):
                if index == 0:
                    index=payload.find(block,index)
                index2=payload.find(block,index+1)
                distances[block].append(index2-index)
                index=index2
        return distances

    @staticmethod
    def _divisors(occurences:dict, distances:dict, max_divisors=5)->dict:
        def divisors(n):
            ret=[]
            for i in range(1,n):
                if n%i==0:
                    ret.append(i)
            return ret
        dist_divisors={}
        for val in distances.values():
            for i in val:
                for j in divisors(i):
                    if j not in dist_divisors.keys():
                        dist_divisors[j]=0
                    dist_divisors[j]+=1

        dist_divisors = {k:v for k,v in dist_divisors.items() if v>1 }
        dist_divisors = sorted(dist_divisors.items(),key = lambda x : x[1])
        dist_divisors.reverse()
        dist_divisors=dict(dist_divisors[0:max_divisors])
        return dist_divisors

    @staticmethod
    def _frequencies(payload:str, key_len:int)->[]:
        splits=[''.join([payload[j] for j in range(i, len(payload), key_len)]) for i in range(key_len)]
        frequencies=[{} for i in range(len(splits))]
        for i, split in enumerate(splits):
            for j in split:
                if j in frequencies[i].keys():
                    continue
                frequencies[i][j]=split.count(j) 
            frequencies[i]=sorted(frequencies[i].items(),key = lambda x : x[1])
            frequencies[i].reverse()
            frequencies[i]=dict(frequencies[i])
        return frequencies

    @staticmethod
    def crack(payload, lang=frequence_lang['french'], max_occurences = 10, max_block_size = 8, max_divisors = 10, deep = 1):
        occurences = Vigenere._occurences(payload, max_occurences, max_block_size)
        distances = Vigenere._distances(payload, occurences)
        divisors = Vigenere._divisors(occurences, distances, max_divisors)
        keys=[]
        def index_vigenere(items_list, x) : 
            return string.ascii_uppercase.index(items_list[x][0])-string.ascii_uppercase.index(lang[0])
        for length in divisors.keys():
            frequencies = Vigenere._frequencies(payload, length)
            deltass = [[index_vigenere(list(frequency.items()),0) for frequency in frequencies]]
            if deep > 0:
                for i,frequency in enumerate(frequencies):
                    items = list(frequency.items())
                    deltass_len = len(deltass)
                    for k in range(deep):
                        if items[0][1] - items[k+1][1] <= 3:
                            for j in range(deltass_len):
                                deltass.append(deepcopy(deltass[j]))
                                deltass[-1][i] = index_vigenere(items, k+1)
            keys += [''.join([string.ascii_uppercase[i] for i in d]) for d in deltass]
        return keys

      

