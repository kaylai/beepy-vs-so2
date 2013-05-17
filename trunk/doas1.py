import os.path
import csv
import numpy
import calendar
import datetime
import scipy.signal
from scipy.interpolate import interp1d
from pylab import *


def load_ratios_from_csv(filename, excel_file=True):
    """
    Returns a tuple of arrays: (times,ratios).
    """
    
    print "Loading data from "+filename
    if not os.path.exists(filename):
        raise IOError, "Cannot open "+filename+" for reading. No such file."
    
    ifp = open(filename,"rb")
    
    if not excel_file:
        dialect = csv.Sniffer().sniff(ifp.read(3000))
        ifp.seek(0)
        file_reader = csv.reader(ifp,dialect)
    else:
        file_reader = csv.reader(ifp)
    
    #read the header data and extract the date
    i=0
    date = None
    while i<6:
        row = file_reader.next()
        if (row[0].startswith("Date")):
            date = datetime.datetime.strptime(row[0],"Date : %d/%m/%Y")       
        i+=1
    
    if date is None:
        raise IOError, "Failed to read the date from the file"
        
    #skip the next 4 rows
    file_reader.next()
    file_reader.next()
    file_reader.next()
    file_reader.next()
    
    times = []
    ratios = []
    #read the lines of data
    while True:
        try:
            row = file_reader.next()
        except StopIteration:
            break
        
        if len(row) < 4:
            continue
        
        if row[3] == '':
            continue
        
        time = datetime.datetime.strptime(row[3],"%H:%M:%S")
        
        if times and (time.time() < times[-1].time()):
            #either we have passed midnight or there is some horrible jump in the data
            if times[-1].time().hour == 23 and time.time().hour == 0:
                #then we have just passed midnight and need to add an extra day
                print times[-1].time()," -> ",time.time()," :passed midnight - added an extra day to the date."
                date = date + datetime.timedelta(days=1)
            else:
                print "Warning! Time skip in data between ",times[-1].time()," -> ",time.time()
        
        times.append(datetime.datetime.combine(date.date(),time.time()))
        ratios.append(float(row[6]))
    
    return numpy.array(times),numpy.array(ratios)
        

def fix_time_skip(times, correct_origin='start'):
    
    if correct_origin not in ('start','end'):
        raise ValueError, "Unknown value for correct_origin, expected either \'start\' or \'end\'."
    
    #convert times to seconds
    times = numpy.array([calendar.timegm(t.timetuple()) + t.microsecond/1e6 for t in times])
    
    #look for skips
    i=1
    n=0
    gap=0
    skips = []
    while i<len(times):
        d_t = times[i]-times[i-1]
        if d_t < 0:
            skips.append(i)
        else:
            n+=1
            gap += d_t
        i+=1
    
    mean_gap = gap/float(n)
    print "Mean data interval = ",mean_gap
    
    for skip in skips:
        skip_length = times[skip] - times[skip-1]
        correction = -(skip_length + mean_gap)
        
        times[skip:] = times[skip:]+correction
    
    return numpy.array([datetime.datetime.fromtimestamp(t) for t in times])
        
    


def align_in_time(data1, times1, data2, times2, resolution):
    """
    Linear interpolates data to have points at the desired time resolution and
    at the same times in both datasets. 
    
    * data1/2: array of data points.
    * resolution: desired number of seconds between data points.    
    * times1/2: array of datetime objects.
    
    Returns a tuple of interpolated data arrays and corresponding times
    (data1,data2,times).
    
    """
    #convert times to seconds from the epoch              
    times1 = numpy.array([calendar.timegm(t.timetuple()) + t.microsecond/1e6 for t in times1])
    times2 = numpy.array([calendar.timegm(t.timetuple()) + t.microsecond/1e6 for t in times2])
    
    #take the latest start to be the start time (otherwise have to interpolate
    #off the end of one signal) and the earliest end time for the same reason
    start_time = max(times1[0],times2[0])
    end_time = min(times1[-1], times2[-1])
    num_of_interp_samples = round((end_time - start_time) / float(resolution))
    
    #create array of datetimes that will relate to the interpolated data points
    interp_times_secs = numpy.linspace(start_time, end_time, num_of_interp_samples)
    interp_times = numpy.array([datetime.datetime.utcfromtimestamp(x) for x in interp_times_secs])
    
    #do the interpolation on the two data sets
    interpolator = interp1d(times1, data1)
    interp_data1 = interpolator(interp_times_secs)    
    interpolator = interp1d(times2, data2)
    interp_data2 = interpolator(interp_times_secs)
    
    return interp_data1, interp_data2, interp_times


def normalise(data):
    return (data - numpy.mean(data))/numpy.std(data)


def correlate(data1, data2, start_idx, window_length, max_lag, draw_plot=False):
    
    #chop out window from data1 array
    window = normalise(numpy.array(data1[start_idx:start_idx + window_length]))
    
    #chop out the relevant section of data (from the start index up to the max lag)
    data = numpy.array(data2[start_idx: start_idx + max_lag+ window_length]) #will break if max_lag>array dim
   
    corr = numpy.zeros(max_lag)
    #do the correlation
    i = 0
    while i<max_lag:
        d = normalise(data[i:i+window_length])
        corr[i] = (1.0/(float(window_length)-1))*numpy.sum(window * d)
        
        i+=1   
    
    if draw_plot:
        subplot(311)
        plot(data1[start_idx:start_idx+max_lag+ window_length])
        plot(data1[start_idx:start_idx+window_length],'r-')
        title("data1")
        
        subplot(312)
        plot(data2[start_idx:start_idx+max_lag+ window_length])
        title("data2")
        
        subplot(313)
        plot(corr)
        title("correlation")
        
        #TODO - use line.setvalues rather than clearing the plot.
        draw()
          
    return corr
