from pylab import *
import datetime
import villa_microtops_csvread
from avoscan.processing import load_columns_file
from scipy.signal import medfilt
from avoscan.processing import load_adv_retrieval_file

##Use this block for advanced retrieved files
#filenames, times, ca, error = load_adv_retrieval_file("/media/FLASHY/Avg_Solar//20130325/26Mar_Solar_Advance.xls")
#ca = medfilt(ca, 5)
#plot(ca[30:100])
#ylim((-1000,6000))

##Use this block for files with SS_to_STD done on them
filenames, times, ca, error = load_columns_file("/media/FLASHY/Solar_28Feb/20130228/solar_28Feb_scan3_column.txt")
#ca = medfilt(ca, 11)
plot(times, ca)
#ylim((-1000,6000))

twinx()
micro_times, aot = microtops_csvread.opencsv("/media/FLASHY/Solar_28Feb/28Feb_beepy.csv")
#aot = medfilt(aot, 5)
plot(micro_times, aot, "r-")

show()