import numpy as np
import traceback
from accessify import protected #Protected method's use @protected
import sys
from itertools import product
import xxhash
import timeit
import multiprocessing as mp
import platform


class History:

    dublicate = 0.0
    history_arr = np.zeros(500)
    scored = 0
    __isInit = False
    __main_dict = []
    def set_history(self,sequence:int,score:float):

        '''Проверяет имеющийся массив history_arr на наличие в нем
        дубликата sequence
        если дубликат найден - проверяет score, и записывает score только
        если оно меньше уже находящегося в данных
        если дубликат не найден записывает входные данные
        и ведет счетчик дубликатов '''

        #Quik hash generated
        hash = self.__hashash(sequence)
        if  not self.__isInit:
            self.__main_dict.append(hash)
            self.__isInit = True
            self.history_arr =sequence

            #if dublicate find
        if  bool(self.__search(hash)):
            
            if score < self.scored:
                self.scored = score
            self.dublicate+=1
        else:
            self.history_arr =np.vstack([self.history_arr,sequence])
            self.__main_dict.append(hash)
   
    def __hashash(self,sequence):
        right = xxhash.xxh32()
        for it in sequence:
            right.update(it)
        return int(right.hexdigest(),16)


    def __search(self,hash:int):
        # искомое число
        self.__main_dict.sort()
        value = hash
        mid = len(self.__main_dict) // 2
        low = 0
        high = len(self.__main_dict) - 1

        while self.__main_dict[mid] != value and low <= high:
            if value > self.__main_dict[mid]:
                low = mid + 1
            else:
                high = mid - 1
            mid = (low + high) // 2

        if low > high:
            return 0
        else:
            return mid
            #print("ID =", mid)

    def is_it_dupe_sequence(self,sequence:int):
        '''Принимает 1 переменную
        sequence - массив длинной 500 (int) положительных чисел)
        проверяет, есть ли такая в истории. Если есть True если нет False
        '''
        if self.__isInit:
            return bool(self.__search(self.__hashash(sequence)))

    def save_history(self,filepath:str):
        ''' Принимает 1 переменную — filepath 
        записывает данные истории на диск'''
        np.save(filepath, self.history_arr )

    def load_history(self,filepath:str):
        '''Принимает 1 переменную — filepath
        загружает данные истории с диска'''
        self.history_arr = np.load(filepath)



if __name__ == "__main__":



    def update_progress(progress):
        #update_progress() : Displays or updates a console progress bar
        ## Accepts a float between 0 and 1. Any int will be converted to a float.
        ## A value under 0 represents a 'halt'.
        ## A value at 1 or bigger represents 100%
        barLength = 40 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1 
            status = "Done...\r\n"
        block = int(round(barLength*progress))
        text = "\rItems: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,2), status)
        sys.stdout.write(text)
        sys.stdout.flush()

    try:
        print("Используемый процессор: ",platform.processor())
        score = np.random.sample()
        test = History()
        maxsize = 1073741824
        memory_exit = 0
        cores =mp.cpu_count()#Intel core i7 740qm (8 cores)
        print('Количество ядер: ',cores)
        pool = mp.Pool(cores)
        jobs = []
        loop = timeit.default_timer()
        score = np.random.sample()
        sequence = np.random.randint(0,10,500)
        sequence1 = np.random.randint(0,10,500)
        sequence2 = np.random.randint(0,10,500)
        
        test.set_history(sequence,score)
        test.set_history(sequence,score)
        test.set_history(sequence1,score)
        test.set_history(sequence1,score)
        test.set_history(sequence2,score)
        test.set_history(sequence1,score)
        test.set_history(sequence2,score)
        test.set_history(sequence2,score)
        
        while(test.history_arr.__sizeof__() < maxsize):
            a = timeit.default_timer()
            jobs.append(test.set_history(np.random.randint(0,10,500),np.random.sample()))
            delta = (timeit.default_timer()-a)*1000
            memory_now = test.history_arr.__sizeof__()
            memory_exit = maxsize - memory_now
            percent_now = memory_now/maxsize
            update_progress(percent_now)
            #print("осталось {} из {} за {} ms ".format(memory_exit,maxsize,round(delta,2)))
        
        for job in jobs:
            try:
                job.get()
            except:
                pass

        pool.close()
        print('дубликатов в истории: {}'.format(test.dublicate))
        fem = (timeit.default_timer()-loop)/60
        print('достигнут предел в {}kb! bytes - {} за {} мин'.format(maxsize/1024,test.history_arr.__sizeof__(),round(fem,2)))
    except:
        print(traceback.format_exc())
