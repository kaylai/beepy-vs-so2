from pylab import *
import microtops_csvread
import datetime
from avoscan.processing import load_columns_file
from doas1 import align_in_time
import numpy
from scipy.signal import medfilt
from scipy.stats import pearsonr
from avoscan.processing import load_adv_retrieval_file

filenames, times, ca, error = load_adv_retrieval_file("/home/kaylai/Desktop/Turrialba MTOPS/Avg_Solar/20130325/avg_solar_26Mar_Adv.xls")
ca = medfilt(ca, 5)

#filenames, times, ca, error = load_columns_file("/home/kaylai/Desktop/Turrialba MTOPS/20130325/solar2__column.txt")
#filenames, times, ca, error = load_columns_file("/media/FLASHY/Solar_28Feb/20130228/solar_28Feb_scan3_column.txt")

#times_both = numpy.concatenate((times, times2))
#ca_both = numpy.concatenate((ca, ca2))

micro_times, aot, aot_440, aot_675, aot_870, aot_1020 = microtops_csvread.opencsv("/media/FLASHY/MICROTOP/Turrialb/25Mar.csv")
#micro_times, aot = microtops_csvread.opencsv("/media/FLASHY/Solar_28Feb/28Feb_beepy.csv")
aot = medfilt(aot, 5)

plot(ca[30:100], numpy.log(aot[30:100]), "r.")
xlim((0,3000))
#plot(ca, numpy.log(aot), "r.")

plot(ca[30:100], numpy.log(aot_440[30:100]), "g.")

plot(ca[30:100], numpy.log(aot_675[30:100]), "b.")

plot(ca[30:100], numpy.log(aot_870[30:100]), "k.")

plot(ca[30:100], numpy.log(aot_1020[30:100]),'y.')

print "AOT 380 gives (%f,%f) pearson number"%pearsonr(ca[30:100], numpy.log(aot[30:100]))
print "AOT 440 gives (%f,%f) pearson number"%pearsonr(ca[30:100], numpy.log(aot_440[30:100]))
print "AOT 675 gives (%f,%f) pearson number"%pearsonr(ca[30:100], numpy.log(aot_675[30:100]))
print "AOT 870 gives (%f,%f) pearson number"%pearsonr(ca[30:100], numpy.log(aot_870[30:100]))
print "AOT 1020 gives (%f,%f) pearson number"%pearsonr(ca[30:100], numpy.log(aot_1020[30:100]))

show()

        