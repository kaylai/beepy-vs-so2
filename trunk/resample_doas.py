import datetime
import microtops_csvread
from avoscan.processing import load_columns_file
import numpy
from std_ops.iter_ import array_multi_sort
from doas.spectrum_loader import SpectrumIO
from doas.spectra_dir import SpectraDirectory

micro_times, aot = microtops_csvread.opencsv("/media/FLASHY/MICROTOP/Turrialb/25Mar.csv")

loader = SpectrumIO()
doas_spec = [f for f in SpectraDirectory("/media/FLASHY/Solar DOAS/Turrialba/25Mar/Solar Doas/", recursive = True)]
def spec_time_cmp(s1, s2):
    return cmp(s1.capture_time, s2.capture_time)
doas_spec.sort(cmp = spec_time_cmp)

count = 0
for t_micro_start in micro_times:
    t_micro_end = t_micro_start + datetime.timedelta(seconds = 32/3.0)
    
    doas_to_avg = [s for s in doas_spec if s.capture_time >= t_micro_start and s.capture_time < t_micro_end]
    if not doas_to_avg:
        continue
    spec_avg = doas_to_avg[0]
    for p in doas_to_avg[1:]:
        spec_avg += p
    loader.save(spec_avg, "/home/kaylai/Desktop/Avg_Solar/avg_solar_%05d" %count, "SpectraSuite Tab-delimited") 
    count += 1
    
    print [s.filename for s in doas_to_avg]