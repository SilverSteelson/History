#!/usr/bin/python
import numpy as np
#import ctypes
from xxhash import xxh32
from functools import lru_cache
#import tables as tb
#from my_c_search import lib


class History:
    dublicate = -1#Ignor init sequence
    history_arr = 0
    score = 0
    __isInit = False
    __main_dict = 0

    def set_history(self,sequence:int):
        '''Проверяет имеющийся массив history_arr на наличие в нем
        дубликата sequence
        если дубликат найден - проверяет score, и записывает score только
        если оно меньше уже находящегося в данных
        если дубликат не найден записывает входные данные
        и ведет счетчик дубликатов '''
        #Quik hash generated
        hash = self.__hashash(sequence)
        if not self.__isInit:
            self.history_arr = sequence
            self.__main_dict=np.append(self.__main_dict,hash)
            #self.__main_dict.append(hash)
            self.__isInit = True

            #if dublicate find
        if self.__search(hash):
            
            if score < self.score:
                self.score = score
            self.dublicate+=1

        else:
            #self.__main_dict.sort()
            #self.__main_dict.append(hash)
            self.history_arr =np.append(self.history_arr,sequence)
            self.__main_dict=np.append(self.__main_dict,hash)

    def __hashash(self,sequence:int):
        cops = sequence.copy()
        right =  xxh32()
        for it in cops:
            right.update(it)
        return right.intdigest()

    @lru_cache()
    def __search(self,hash:int):

        #a = process_time()
        # искомое число
        dict = self.__main_dict.copy()
        #print(hash)
        #result = lib.search(dict.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),0,dict.size,hash)
        #last = dict.tolist()
        #dict = (ctypes.c_int * len(last))(*last)
        #result = lib.search(dict,0,len(last),hash)
        result = np.where(dict == hash, True, False).any()
        #b = process_time()
        #delta = b-a
        #print('\rsearch',delta)
        return result

    def is_it_dupe_sequence(self,sequence:int):
        '''Принимает 1 переменную
        sequence - массив длинной 500 (int) положительных чисел)
        проверяет, есть ли такая в истории. Если есть True если нет False
        '''
        if self.__isInit:
            return self.__search(self.__hashash(sequence))
        else:
            return False

    def save_history(self,filepath:str):
        ''' Принимает 1 переменную — filepath 
        записывает данные истории на диск'''
        with open(filepath,"wb") as f:
            np.save(f,self.history_arr)
            np.save(f,self.score)
            np.save(f,self.__main_dict)
        f.close()

    def load_history(self,filepath:str):
        '''Принимает 1 переменную — filepath
        загружает данные истории с диска'''
        with open(filepath,"rb") as f:
            self.history_arr = np.load(f)
            self.score = np.load(f)
            self.__main_dict= np.load(f)
        f.close()
