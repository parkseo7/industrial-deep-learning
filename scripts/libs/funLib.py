import os
import numpy as np
import math
from math import pi
from scipy import stats

# Function to categorize:
def obtainCollection(listNames):
    '''
    Function for obtaining a collection of groups (sublists) with indices that correspond to common names.
    '''
    
    N = len(list(listNames))
    collectionNames = []
    collectionInds = []
    
    for i in range(N):
        name = listNames[i]
        if name in collectionNames:
            ind = collectionNames.index(name)
            collectionInds[ind].append(i)
        
        else:
            collectionNames.append(name)
            collectionInds.append([i])
    
    return (collectionNames, collectionInds)


# Function to obtain KS statistics:
def getKsStatistics(arrStructs, indsStructs, cdf, sizeThresh=25):
    '''
    Produce a table of K-S statistics with p-values (mean + std), 
    comparing the entries of arrStructs with a distribution cdf 
    (string from scipy.stats). The arguments are the following:
     - arrStructs: An M x N x N array, where M is the number of patients.
     - indsStructs: A list partitioning range(N).
     - cdf: The distribution to compare (known distribution from scipy).

    Only non-zero values are considered. Ignores any pairs with less than
    sizeThresh non-zero entries.

    Returns the mean K-S statistic and p-value, along with the std and
    min/max over all pairs of groups from indsStructs. Pairs are formed
    directionally (i.e. i-j is not counted as the same pair group as j-i).
    '''

    numGroups = len(indsStructs)
    indsAll = np.arange(numGroups)
    listKS = []
    listPval = []

    for i in range(numGroups):
        for j in range(numGroups):
        
            inds1 = indsStructs[i]
            inds2 = indsStructs[j]
            subStructs = arrStructs[np.ix_(indsAll, inds1, inds2)]
            rvs = np.reshape(subStructs, -1)

            # Filter out all zero entries:
            rvs = rvs[rvs > 0]
            if rvs.size < sizeThresh:
                continue

            # Compute the K-S statistic over all entries in subStructs:
            KS, pvalue = stats.kstest(rvs, cdf)
            listKS.append(KS)
            listPval.append(pvalue)

    arrKS = np.array(listKS)
    arrPval = np.array(listPval)

    # Post-loop calculations
    dictKS = {
        'mean': np.mean(arrKS),
        'var': np.var(arrKS),
        'min': np.min(arrKS),
        'max': np.max(arrKS)
        }
    
    dictP = {
        'mean': np.mean(arrPval),
        'var': np.var(arrPval),
        'min': np.min(arrPval),
        'max': np.max(arrPval)
    }

    return dictKS, dictP







    return None


def getNodeDegree(connMat):
    '''
    Returns a vector of node degrees k, where k[i] is the number of edges a_ij > = connected to node i.
    '''

    adjMat = (connMat > 0).astype('int64')
    return np.sum(adjMat, axis=1)


def getClusteringCoeff(connMat):
    '''
    Returns a vector of clustering coefficients.
    '''

    return None
    

# TEST
if __name__ == "__main__":
    pass
