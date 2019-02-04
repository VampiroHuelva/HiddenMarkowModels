#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""The module for operations on sequence data.

This script serves as the module that includes the operations on sequence data.
"""

import string

# List of training sequences, note space at beginning and end in each sequence,
# this makes the counting more straight forward
setX = list()

# SetPi contains the state sequences of all training sequences
SetPi = list()


# Read sequences from a file (fasta format) and then store them in either list
# setX  or list setP depending on the flag
# The flag should either be "X" or "Pi" which indicate the type of sequence
# being read,
# Flag: "X" for symbol sequence and "Pi" for State sequence
# Output: either setPi or setX, depending on the flag
# Usage example: sequences = readSeq("sequences.txt", "X")
def readSeq(filename, flag):
    # Check if the correct flag is used
    if flag not in ("X", "Pi"):
        print("The Flag for readSeq should either be \"X\" or \"Pi\"")
        exit(1)
    if flag == "X":
        clearSetX()
    elif flag == "Pi":
        clearSetPi()
    seqFile = open(filename)
    startReading = False
    for line in seqFile:
        if line[0] == ">":
            startReading = True
        elif startReading and line != "":
            if flag == "X":
                x = list(" " + line.strip() + " ")
                setX.append(x)
            if flag == "Pi":
                SetPi.append(list("B" + line.strip() + "E"))
            startReading = False
    if flag == "X":
        return setX
    elif flag == "Pi":
        return SetPi


# Write sequences in setX into a file (in fasta format)
def writeAllSeq(filename, setX):
    i = 0
    f = open(filename, "w")
    for x in setX:
        i += 1
        # print>>f, ">seq", i
        print(">seq", i, file=f)
        to_print = []
        for i in range(1, len(x)-2):
            to_print.append(str(x[i]))
            # print>>f, x[i]
            # print(x[i], file=f)
        # print>>f
        print(''.join(to_print), file=f)
        # print(file=f)
    f.close()


def clearSetX():
    setX[:] = []


def clearSetPi():
    setPi[:] = []
