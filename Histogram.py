import math

class Histogram(object):
    '''
    Creates a histogram given a list of numeric data.    
    '''
    def __init__(self, list, bin_count=None, filter_outliers=True):
        '''
        Constructor
        '''
        self.median = np.median(list)
        self.list = list
        self.iqr = self._iqr()
        if (filter_outliers):
            self.list = filter(self._outlier_filter,list)
            self.iqr = self._iqr()
            self.median = np.median(list)
            
        self.minimum = min(self.list)
        self.maximum = max(self.list)
        if (bin_count == None):
            self.bin_width = self._suggested_bin_width()
        else:
            self.bin_width = (self.maximum - self.minimum) / float(max(1,bin_count))
        
        self.bin_count = int(math.ceil((self.maximum - self.minimum)/self.bin_width))   
        self._build_histogram()
        
    
    def _build_histogram(self):
        '''
        Build the histogram
        
        
        '''                    
        indexed_list = zip(map(self._bin_number,self.list),self.list)

        # Probably a better way to do this in python
        bins = dict()
        for (x,y) in indexed_list:
            if x in bins:
                bins[x].append(y)
            else:
                bins[x] = [y]
        
  
        self.bin_min = [r*self.bin_width+self.minimum for r in range(self.bin_count)]
        self.bin_max = map(lambda x: x+self.bin_width,self.bin_min) 
        self.bin_min.sort()
        self.bin_max.sort()
         
        i = 0
        self.histogram = dict()
        for x in range(self.bin_count):
            if (bins.has_key(x)):
                count = len(bins[x])
            else: 
                count = 0
                
            self.histogram[i] = {'min':self.bin_min[x], 
                                 'max':self.bin_max[x], 
                                 'count': count}
            i += 1
        
            
    def _outlier_filter(self, x): 
        ''' 
        Filter outliers using median +- 3*IQR
        '''
        return (x >= self.median - 3 * self.iqr and x <= self.median + 3 * self.iqr)
    

    def _bin_number(self, x):
        '''
        Get the bin number that x belongs to.
        ''' 
        return int(min(math.floor((x - self.minimum)/self.bin_width),self.bin_count-1))


    def percentile(self, p):
      """
      Returns the number at percentile p of list.
      Interpolates between adjacent points when necessary.
      """
      l_sort = self.list[:]
      l_sort.sort()
      n = len(self.list)
      r = 1 + ((n - 1) * p)
      i = int(r)
      f = r - i
      if i < n:
        result = (1 - f) * l_sort[i - 1] + f * l_sort[i]
      else:
        result = l_sort[i - 1]
      return result
    
    
    def _iqr(self):
      """ 
      Returns the inter-quartile range for the distribution.
      """
      q3 = self.percentile(0.75)
      q1 = self.percentile(0.25)
      return q3 - q1
    
    
    def _suggested_bin_width(self):
      """
      Use the Freedman-Diaconis rule for bin size.
      """
      return 2.0 * self.iqr / (np.size(self.list) ** (1/3.0))
    

if __name__ == "__main__":
    import pprint
    #import random
    import json
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser(description='Build histograms for numeric data.')
    parser.add_argument('input_file', metavar='input_file',
                       help='CSV input file comtaining numeric data.')
    parser.add_argument('--column', dest='column', default=None,
                       help='Name of the column to process.  All columns will be processed '
                            'if this parameter is not provided.')
    args = parser.parse_args()
    #h = Histogram(range(100,200))
    #l = [random.randint(0,100)/10.0 for r in xrange(500)]
    #l.sort()
    #l = [0.1,2,0.510034,100]
    #h = Histogram(l,10)
    #pprint.pprint(vars(h))
    #pprint.pprint(h.histogram)
    
    #json.dumps(h.histogram,indent=4)
    data = np.genfromtxt(args.input_file, dtype=None, delimiter=',', names=True, invalid_raise=False)
    if (args.column == None):
        for (name) in data.dtype.names:
            print name
            h = Histogram(data[name])
            json.dumps(h.histogram, indent=4)
            pprint.pprint(h.histogram)
    else:
        print args.column
        h = Histogram(data[args.column])
        json.dumps(h.histogram, indent=4)
        pprint.pprint(h.histogram)
        
    
    #if (args.column == None):
        #for x in data.func_dict.keys():
        #  print x
    #print 'Median college GPA ' 
    #college_hist.median



  
