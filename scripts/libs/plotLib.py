import os
import numpy as np
from scipy.spatial import distance
import math
from math import pi


def moveSpike(pos1, pos2, spikePos, speed, deltaTime):
    '''
    Move a spike between two nodes. Here, pos1, pos2 are 2-tuples of the two nodal positions. 
    spikePos is the current position of the spike as a float between 0, 1.
    speed is the tangental speed, and deltaTime is the time-step.
    Returns the new spike position as a new float.
    '''
    
    # Compute distance between the two positions:
    totalDist = distance.Euclidean(pos1, pos2)
    travelFloat = speed * deltaTime / totalDist
    
    return spikePos + travelFloat


def floatToTuple(pos1, pos2, posFloat):
    '''
    Converts a float position of the spike to a tuple. 
    Here, pos1, pos2 are 2-tuples of the two nodal positions.
    posFloat is a float between 0, 1
    '''
    
    tuplePos = posFloat * pos1 + (1 - posFloat) * pos2
    return tuplePos


def tupleToFloat(pos1, pos2, posTuple):
    '''
    Converts a tuple position of a spike to a float.
    Here, pos1, pos2 are 2-tuples of the two nodal positions.
    posTuple is a 2-tuple of the spike.
    '''
    
    float1 = (posTuple[0] - pos1[0]) / (pos2[0] - pos1[0])
    float2 = (posTuple[1] - pos1[1]) / (pos2[1] - pos1[1])
    
    # float1 and float2 should agree, but we take the average here.
    return (float1 + float2) / 2


    
# TEST
if __name__ == "__main__":
    pass
