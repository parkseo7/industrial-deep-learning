import os
import numpy as np
from scipy.spatial import distance
import math
from math import pi


class SpikingNetwork:
    
    def __init__(self, nodes, dists, speeds, rad):
        
        # Static parameters:
        self.nodes = nodes # Nodes is an N by 2 array of 2-dim coordinates of the neuron positions
        self.allDists = dists
        self.allSpeeds = speeds
        self.rad = rad # rad parameter of Arc3 bezier curve option
        
        # Action potential spike positions:
        self.edges = -1*np.ones((3,2), dtype='int16') # Rows indicating source and target index of spike
        self.positions = np.zeros(3) # Position as a float between 0 and 1
        self.dists = np.ones(3) # Edge lengths
        self.speeds = np.zeros(3) # Average speed across the edge. This can be expanded upon as an M-dim array with M myelin segments.
        self.centerNodes = -1*np.ones((3,2)) # Center node to be used to plot spike along bezier curve.
        self.numSpikes = 0
        
    
    def removeSpikes(self, inds):
        '''
        Remove a spike at indices inds.
        '''
        
        self.edges = np.delete(self.edges, inds, axis=0).astype('int16')
        self.positions = np.delete(self.positions, inds)
        self.dists = np.delete(self.dists, inds)
        self.speeds = np.delete(self.speeds, inds)
        self.centerNodes = np.delete(self.centerNodes, inds, axis=0)
        self.numSpikes -= inds.size
    
    
    def padSpikes(self, num):
        '''
        Concatenate new entries for edges, positions, and speeds for more spikes.
        Use when numSpikes > positions.size
        '''
        
        self.edges = np.concatenate((self.edges, -1*np.ones((num, 2))), axis=0).astype('int16')
        self.positions = np.concatenate((self.positions, np.zeros(num)))
        self.dists = np.concatenate((self.dists, np.ones(num)))
        self.speeds = np.concatenate((self.speeds, np.zeros(num)))
        self.centerNodes = np.concatenate((self.centerNodes, -1*np.ones((num, 2))), axis=0)
        
        
    def addSpike(self, edge):
        '''
        Add a spike at edge, which is a 2-tuple given by (source, target).
        '''
    
        # Check if there are enough entries:
        if self.numSpikes >= self.positions.size:
            self.padSpikes(10)


        N = self.numSpikes
        self.edges[N] = np.asarray(edge)
        self.positions[N] = 0
        self.dists[N] = self.allDists[edge]
        self.speeds[N] = self.allSpeeds[edge]
        
        # Compute bezier center:
        indS, indT = edge
        nodeS = self.nodes[indS]
        nodeT = self.nodes[indT]
        
        x1, y1 = nodeS[0], nodeS[1]
        x2, y2 = nodeT[0], nodeT[1]
        
        xC, yC = 0.5*(x1+x2), 0.5*(y1+y2)
        dx, dy = x2-x1, y2-y1
        
        self.centerNodes[N] = np.array([xC, yC]) + self.rad * np.array([dy, -dx])
        

        self.numSpikes += 1

    
    def moveSpikes(self, dt):
        '''
        Move all spikes in accordance to dt. If a spike position exceeds 1, then remove the spike.
        '''
        
        moveDists = dt * self.speeds
        movePos = moveDists / self.dists
        
        self.positions = self.positions + movePos
        
        # Remove spikes that have reached target:
        inds = np.argwhere(self.positions >= 1.0)
        self.removeSpikes(inds)
        
    
    def getSpikeCoord(self, i):
        '''
        Returns the coordinate of spike i.
        '''
        
        edge = self.edges[i]
        indS = edge[0]
        indT = edge[1]
        nodeS = self.nodes[indS]
        nodeT = self.nodes[indT]
        nodeC = self.centerNodes[i]
        
        # Bezier curve:
        t = self.positions[i]
        inter1 = (1-t)*nodeS + t*nodeC
        inter2 = (1-t)*nodeC + t*nodeT
        coord = (1-t)*inter1 + t*inter2 # Note: Bezier curve does not go through center node!
        
        return coord
        
    
    def getSpikeCoords(self):
        '''
        Returns all spike coordinates as an N by 2 array, where N is the number of spikes.
        '''
        
        N = self.numSpikes
        coords = np.zeros((N,2))
        
        for i in range(N):
            coords[i] = self.getSpikeCoord(i)
        
        return coords


    
# TEST
if __name__ == "__main__":
    pass
