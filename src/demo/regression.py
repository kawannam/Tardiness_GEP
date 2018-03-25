#!/usr/bin/env python2.5
from pygep import *
from pygep.functions.linkers import sum_linker
from pygep.functions.mathematical.arithmetic import (add_op, subtract_op, 
    multiply_op, divide_op)
import random


# Data points to test against and target function
class DataPoint(object):
    SAMPLE = []
    SAMPLE_SIZE = 10
    RANGE_LOW, RANGE_HIGH = -10.0, 10.0
    RANGE_SIZE = RANGE_HIGH - RANGE_LOW

    def __init__(self, x):
        self.x = float(x)

        # The function we are trying to find
        # f(x) = 4*x^3 + 3x^2 + 2x + 1
        self.y = 4*(x**3) + 3*(x**2) + (2*x) + 1

    @staticmethod
    def populate():
        # Creates a random sample of data points
        DataPoint.SAMPLE = []
        for _ in xrange(DataPoint.SAMPLE_SIZE):
            x = DataPoint.RANGE_LOW + (random.random() * DataPoint.RANGE_SIZE)
            DataPoint.SAMPLE.append(DataPoint(x))


# The chromsomes: fitness is accuracy over the sample
class Regression(Chromosome):
    REWARD = 1000.0
    functions = add_op, subtract_op, multiply_op, divide_op
    terminals = 'x',
    
    def _fitness(self):
        # Fitness function: relative mean squared error
        error = 0.0
        for x in DataPoint.SAMPLE:
            try:
                guess = self(x) # Evaluation of this chromosome
                error += ((guess - x.y) / x.y) ** 2
            
            except AttributeError: # programmer error
                raise
            
            except: # unviable organism
                return 0
        
        return self.REWARD * (1 / (1 + (error / DataPoint.SAMPLE_SIZE)))
    
    def _solved(self):
        return self.fitness >= self.REWARD


if __name__ == '__main__':
    DataPoint.populate()

    # Search for a solution
    p = Population(Regression, 30, 6, 4, sum_linker)
    print p

    for _ in xrange(1000):
        if p.best.solved:
            break
        p.cycle()
        print
        print p
        
    if p.best.solved:
        print
        print 'SOLVED:', p.best
