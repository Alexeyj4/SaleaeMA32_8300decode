# import math
# import numpy
import os

from saleae.range_measurements import DigitalMeasurer

NUM_OF_ITERATIONS='num_of_iters'

path, filename = os.path.split(os.path.abspath(__file__))
f = open(path+u'\log.txt','w')


class MyDigitalMeasurer(DigitalMeasurer):
    supported_measurements = [NUM_OF_ITERATIONS]

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.i=0 #period meas iterator
        self.t_prev=None #prev time
        self.iter_count=0        
        
        

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    def process_data(self, data):
        
        for t, bitstate in data:
            
            if self.i==1:
                if self.t_prev==None:
                    self.t_prev=t
                    return
                self.iter_count=self.iter_count+1
                if self.iter_count>2:
                    #f.write(str(1/float(t-self.t_prev))+"\n\r")
                    f.write(str(float(t-self.t_prev))+"\n")
                self.t_prev=t
                self.i=0
            if bitstate==True:
                self.i=self.i+1

        

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {}
        values[NUM_OF_ITERATIONS]=self.iter_count        
        f.close()
        return values
    

