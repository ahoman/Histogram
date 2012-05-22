import math

class Histogram(object):
    '''
    Creates a histogram given a list of numeric data.
    
    Parameters include:
      
        list: A list of numeric data.      
        
        bin_count: The number of bins that the resulting histogram should have.
                   If not passed to the constructor, the histogram will use the
                   Freedman-Diaconis rule to estimate bin width and count.
        
        filter_outliers: Boolean indication of whether outliers should be removed.
                         Default is true and uses median +- 3*IQR to filter data.
                         
    Upon instantiation, this class's 'histogram' attribute will contain a 
    dictionary representing the histogram where each key will be an integer bin
    number and each value will be a dictionary containing the following items:
       
        min: The lower bin boundary (inclusive)
        max: The upper bin bounder (inclusive for the last bin, exclusive for others)
        count: The number of observations between min and max.
    '''
    def __init__(self, list, bin_count=None, filter_outliers=True):
        '''
        Constructor
        '''
        # TODO: Validate data in list and bin_count
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
        Populate the histogram attribute.       
        '''                    
        # Map bin numbers to corresponding elements in list.
        indexed_list = zip(map(self._bin_number,self.list),self.list)

        # Aggregate results by bin number
        # TODO: Is there a more effficient way to do this?
        bins = dict()
        for (x,y) in indexed_list:
            if x in bins:
                bins[x].append(y)
            else:
                bins[x] = [y]
  
        # determine min/max values for each bin
        self.bin_min = [r*self.bin_width+self.minimum for r in range(self.bin_count)]
        self.bin_max = map(lambda x: x+self.bin_width,self.bin_min)
        self.bin_min.sort()
        self.bin_max.sort()
         
        # Populate self.histogram based on min, max, and count values
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
    # TODO: The command line interface to this module should be provided
    #       via some other means, so that we can do testing here.
    #
    # At minimum, tests should include:    
    #  1. Verfication of bin widths (i.e. bin_width should be 1, given range(10)
    #      and bin_count = 10
    #  2. Verification of bin counts
    #  3. Verification that outlier removal works correctly.
    #  4. Verification of histograms for various static data with known/expected distributions.
    #     i.e. list=range(10), bin_count=5 should yield 5 bins having count=2
    
    # Implement a command-line interface to the Histogram module.
    import pprint    
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
    
    data = np.genfromtxt(args.input_file, dtype=None, delimiter=',', names=True, invalid_raise=False)
    if (args.column == None):
        for (name) in data.dtype.names:
            print name
            h = Histogram(data[name])
            pprint.pprint(json.dumps(h.histogram, indent=4))
            #pprint.pprint(h.histogram)
    else:
        print args.column
        h = Histogram(data[args.column])
        pprint.pprint(json.dumps(h.histogram, indent=4))
        #pprint.pprint(h.histogram)
        