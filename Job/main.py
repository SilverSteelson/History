#!/usr/bin/python
from .history import History

import traceback
import sys
import os
from time import process_time
import multiprocessing as mp
import platform
from scipy import interpolate
import numpy as np
from psutil import virtual_memory
from hurry.filesize import size
import datetime

def update_progress(progress,time):
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
        text = "\rItems: [{0}] {1}%  remained {3}m {2}".format( "#"*block + "-"*(barLength-block), round(progress*100,2), status, datetime.timedelta(seconds =time))
        sys.stdout.write(text)
        sys.stdout.flush()

def testing(maxsize,filep, isLoad = False):

        try:
            test = History()
            cores =mp.cpu_count()
            mem = virtual_memory()#RAM
            if isLoad:
                print('Load history and continue...')
                test.load_history(filep)
            else:
                print("Processor: ",platform.processor())
                # my Intel core i7 740qm (8 cores)
                print('Cores: ',cores,end=' ;')
                
                if (mem.total < maxsize):
                    print('\n','''/!\ On the computer does not have enough RAM to good complete the task /!\ ''' )
                    print('Necessary : ',size(maxsize),' Have: ',size(mem.total))

                
                else:
                    print('RAM: {}'.format(size(mem.total)))

            pool = mp.Pool(cores)
            jobs = []
            loop = 0
            memory_exit = 0
            time = list()
            mass = list()
            np.seterr(divide='ignore', invalid='ignore')
            timez_last = 0.0
            while(test.history_arr.__sizeof__() < maxsize):

                a = process_time()
                #Creatae process
                jobs.append(test.set_history(np.random.randint(0,10,500),np.random.sample()))
                b = process_time()
                delta = b-a
                memory_now = sys.getsizeof(test.history_arr)
                loop+=delta
                memory_exit = maxsize - memory_now
                percent_now = memory_now/maxsize

                #Data for extrapolation
                time.append(loop)
                mass.append(memory_now)
                
                if len(time)>8:
                    #Calculate time remaind extrapolation
                    f = interpolate.interp1d(mass,time,fill_value='extrapolate')
                    timez = np.max(f(maxsize))
                    if timez == NaN:
                        timez = timez_last
                    else:
                        timez_last = timez
                    update_progress(percent_now,timez)
                    
                else:
                    update_progress(percent_now,0)

            #Close process
            for job in jobs:
                try:
                    job.get()
                except:
                    pass

            pool.close()
            print('Duplicates found: {}'.format(test.dublicate))

            print('Limit reached in {}! Size - {} in {} '.format(size(maxsize/1024),size(test.history_arr.__sizeof__()),datetime.timedelta(seconds =loop)))
            if not isLoad:
                print('Save history on disc...')
                test.save_history(filep)
        except:
            print(traceback.format_exc())


    #32505856
    #62914560
    #tetsting(1048576000,'history.bin')
    #tetsting(6291456000,'history.bin',True)


