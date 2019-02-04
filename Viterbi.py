#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module for Viterbi algorithm.

This script serves as the module that implements Viterbi algorithm.
This module will be called in the 'MainProgram.py'; before that, you need to
complete it.
"""

import AEMatrices
from AEMatrices import A, E, allStates, emittingStates, emissionSymbols


# viterbi algorithm takes a sequence X as input
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: vi matrix and backtrace matrix (as a tuple),
# and the probability of most likely state sequence
# usage example: (vi,backtrace, probability) = viterbi(sequence)
# note: vi[k][i], viterbi of state k, at sequence position i
# note: that we count from 0,1,2...,L,L+1
# where 0 indicates the begin state and L+1 the end state
def viterbi(X):
    # initialise vi to '0' and backTrace to ""
    L = len(X)-2
    vi = dict()
    backTrace = dict()
    for k in AEMatrices.allStates:
        vi[k] = [0]*(L+2)
        backTrace[k] = ["-"]*(L+2)
    # initialise begin state
    vi['B'][0] = 1
    backTrace['B'][0] = "*"
    # iterate over sequence
    for i in range(1, L+1):
        for l in AEMatrices.emittingStates:
            # find maximum of vi[k][i-1]*A[k][l]
            maximum = 0
            statePointer = -1
            for k in AEMatrices.allStates:
                result = vi[k][i-1]*A[k][l]
                if(result > maximum):
                    maximum = result
                    statePointer = k
            vi[l][i] = maximum * E[l][X[i]]
            backTrace[l][i] = statePointer
    # calculate vi for End state at position L-1
    maximum = 0
    statePointer = -1
    for l in AEMatrices.emittingStates:
        result = vi[l][L]*A[l]['E']
        if(result > maximum):
            maximum = result
            statePointer = l
    vi['E'][L+1] = maximum
    backTrace['E'][L+1] = statePointer
    return (vi, backTrace, vi['E'][L+1])


# should be done tab separated, and with only 3 significant numbers
def writePathMatrix(M, X, filename):
    f = open(filename, "w")

    to_print = ['']
    for n in range(0, len(X)):
        to_print.append(str(n))
    print('\t'.join(to_print), file=f)
    to_print = ['']

    for i in X:
        if i == " ":
            to_print.append('-')
        else:
            to_print.append(str(i))
    print('\t'.join(to_print), file=f)

    for state in ['B', 'D', 'L', 'E']:
    # for state in allStates:
        to_print = []
        to_print.append(state)
        for i in range(0, len(X)):
            to_print.append(str(M[state][i]))
        print('\t'.join(to_print), file=f)

    print("written ", filename)


# Generate the most likely state sequence given according to the output of
# viterbi algorithm.
def generateStateSeq(backTrace, x):
    L = len(x)-2
    pi = [""]*(L+2)
    pi[L+1] = "E"
    pi[L] = backTrace["E"][L+1]
    for i in range(L, 0, -1):
        pi[i-1] = backTrace[pi[i]][i]
    # return the state sequence
    return pi
