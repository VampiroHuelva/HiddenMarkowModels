#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for operations on matrices.

This module includes all the necessary matrix operations for HMM.
"""

import sys
from decimal import Decimal

# GLOBAL Variable

# Emission matrix
# contains two-dimensional dictionary E[i][j]
# describing transition probability from state i to j
E = dict()
# Transition matrix
# contains two-dimensional dictionary A[i][j]
# describing transition probability from state i of symbol j
A = dict()

# list of all emission symbols in E
emissionSymbols = []

# list of all states in A
allStates = []

# list of all states excluding "B" and "E"
emittingStates = []


def readMatrix(filename, flag):
    """Read emission or transition matrix from a file.

    flag should be either "A" or "E"
    """
    # check if the correct flag is used
    if flag not in ("A", "E"):
        sys.exit("The flag for readMatrix should either be \"A\" or \"E\"")

    matrixFile = open(filename)
    firstLine = True
    # the columns in the E matrix should be the symbols and the rows should
    # be the states
    for line in matrixFile:
        # cols: are the columns in the matrix
        cols = line.split()
        if firstLine:
            # start reading the header of the matrix
            header = cols
            firstLine = False
        else:
            if len(cols) == len(header)+1:
                # Read each row of the matrix and store each row temporariliy
                # in probs
                probs = {}
                for i in range(1, len(cols)):
                    probs[header[i-1]] = float(cols[i])
                # store each row in the correct matrix, according to the flag
                if flag == "E":
                    E[cols[0]] = probs
                elif flag == "A":
                    A[cols[0]] = probs
            else:
                # we are no longer reading the rows of the matrix,
                # so finish reading.
                break


def init(EMatrixFilename, AMatrixFilename):
    """Initialize the A and E matrices.

    by reading them from files and storing the content of the file into the
    correct variables.
    """
    global A, E, emittingStates, emissionSymbols, allStates

    # reinitialise the variables each time init is performed
    E.clear()
    A.clear()
    emittingStates[:] = []
    allStates[:] = []
    emissionSymbols[:] = []

    # read both matrices
    readMatrix(AMatrixFilename, "A")
    readMatrix(EMatrixFilename, "E")

    # check if begin and end state defined, and remove from list
    for x in A.keys():
        emittingStates.append(x)
    if('B' not in emittingStates or 'E' not in emittingStates):
        print("no begin or end state defined")
        exit(1)
    emittingStates.remove('E')
    emittingStates.remove('B')
    # make a deepcopy
    for x in emittingStates:
        allStates.append(x)
    allStates.append('E')
    allStates.insert(0, 'B')
    # get emitting symbols, from first row of E
    for x in E[emittingStates[0]].keys():
        emissionSymbols.append(x)

    # Checks whether all states in E correspond to states in A, terminate the
    # programme if this is not the case.
    for x in E.keys():
        if x not in allStates:
            print("the states in the E matrix do not correspond to states in"
                  " A matrix")
            exit(1)


def writeEMatrix(M, filename):
    """Write emission matrix M to a file.

    (in tab-separated manner)
    """
    f = open(filename, "w")
    header = ['']
    for s in emissionSymbols:
        header.append(s)
    print('\t'.join(sorted(header)), file=f)

    for l in sorted(emittingStates):
        to_print = []
        to_print.append(l)
        for s in sorted(header)[1:]:
            to_print.append('{:.4E}'.format(Decimal(M[l][s])))
        print('\t'.join(map(str, to_print)), file=f)

    f.close()
    print('New E matrix saved in file')


def writeAMatrix(M, filename):
    """Write transition (A) matrix M to a file.

    (in tab-separated manner)
    """
    f = open(filename, "w")

    # writing the header
    header = ['']
    header.append('B')
    for l in sorted(emittingStates):
        header.append(l)
    header.append('E')
    print('\t'.join(header), file=f)

    # writing rows (notice rows and columns have the same indexes for A)
    for l in header[1:]:
        to_print = [l]
        for k in header[1:]:
            to_print.append('{:.4E}'.format(Decimal(M[l][k])))
        print('\t'.join(map(str, to_print)), file=f)

    f.close()
    print('New A matrix saved in file')


def writeForwardMatrix(forward_matrix, filename):
    """Write forward matrix to a file.

    (in tab-separated manner)
    """
    f = open(filename, "w")
    position=['']
    for i in range(len(forward_matrix['E'])):
        position.append(str(i))
    print('\t'.join(position), file=f)
    for l in ['B', 'D', 'L', 'E']:
        to_print = [l]
        for i in forward_matrix[l]:
            to_print.append('{:.2E}'.format(Decimal(i)))
        print('\t'.join(map(str, to_print)), file=f)
        
    f.close()
    print('New Forward matrix saved in file')


def writeBackwardMatrix(backward_matrix, filename):
    """Write backward matrix to a file.

    (in tab-separated manner)
    """
    f = open(filename, "w")

    position=['']
    for i in range(len(backward_matrix['E'])):
        position.append(str(i))
    print('\t'.join(position), file=f)
    for l in ['B', 'D', 'L', 'E']:
        to_print = [l]
        for i in backward_matrix[l]:
            to_print.append('{:.2E}'.format(Decimal(i)))
        print('\t'.join(map(str, to_print)), file=f)
    
    f.close()
    print('New Backward matrix saved in file')


def setNewA(newA):
    """Copy the value from newA to the current A matrix.

    assuming that both of them have the same states
    """
    for l in allStates:
        A[l] = dict()
        for k in allStates:
            A[l][k] = newA[l][k]
    return A


def setNewE(newE):
    """Copy the value from newE to the current E matrix.

    assuming that both of them have the same states and emission symbols
    """
    for l in emittingStates:
        E[l] = dict()
        for s in emissionSymbols:
            E[l][s] = newE[l][s]
    return E
