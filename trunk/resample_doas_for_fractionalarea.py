import datetime
import calendar
import resample_csvread
from avoscan.processing import load_columns_file, date2secs
import numpy
from std_ops.iter_ import array_multi_sort
from doas.spectrum_loader import SpectrumIO
from doas.spectra_dir import SpectraDirectory

times = resample_csvread.opencsv("/media/FLASHY/MICROTOP/Turrialb/ForInv/GoodINV/Particles_files/Times_For_Resample.csv")
times_tuples = []

for n in range(0, len(times), 3):
    times_tuples.append(times[n:n+3])


loader = SpectrumIO()
doas_spec = numpy.array([f for f in SpectraDirectory("/home/kaylai/Desktop/Avg_Solar/Spectra/")])
doas_spec_times = numpy.array([s.capture_time for s in doas_spec])
doas_spec_times_secs = numpy.array([date2secs(s.capture_time) for s in doas_spec])
count = 0
for t1, t2, t3 in times_tuples:
    index1 = numpy.argmin(numpy.abs(doas_spec_times_secs - date2secs(t1.replace(year=doas_spec_times[0].year, month=doas_spec_times[0].month, day=doas_spec_times[0].day))))
    index2 = numpy.argmin(numpy.abs(doas_spec_times_secs - date2secs(t2.replace(year=doas_spec_times[0].year, month=doas_spec_times[0].month, day=doas_spec_times[0].day))))
    index3 = numpy.argmin(numpy.abs(doas_spec_times_secs - date2secs(t3.replace(year=doas_spec_times[0].year, month=doas_spec_times[0].month, day=doas_spec_times[0].day))))
    assert index1 != index2 and index1 != index3 and index2 != index3
    avg_spec = doas_spec[index1] + doas_spec[index2] + doas_spec[index3]
    loader.save(avg_spec, "/media/FLASHY/MICROTOP/Turrialb/ForInv/GoodINV/Particles_files/Resampled_for_f/resampled_for_f_%05d" %count, "SpectraSuite Tab-delimited")
    count += 1