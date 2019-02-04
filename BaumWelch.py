#s!/usr/bin/python
# -*- coding: utf-8 -*-

import AEMatrices
import math
from AEMatrices import A, E, allStates, emittingStates, emissionSymbols

# Forward algorithm, takes a sequence X and the nr. of symbols in of the sequence (L) as inputs
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: forward matrix (in form of dictionary)
# usage example: f = forward(sequence, L)
# f[k][i], forward of state k, at sequence position i
# note that we count from 0,1,2...,L,L+1
# where 0 indicates the begin state and L+1 the end state
def forward(X,L):
	f = dict()

	# initialise f to '0'
	for k in allStates:
		f[k] = [0]*(L+2)

	# initialise begin state
	f["B"][0]=1

	#############################
	### INSERT YOUR CODE HERE ###
	#############################


	# iterate over sequence
	## Modidied from viterbi
	for i in range(1, L + 1):
		for l in AEMatrices.emittingStates:
			# do the sum of all the possible paths
			sum_init = 0
			# statePointer = -1  --> Do not need and statepointer
			for k in AEMatrices.allStates:
				index = f[k][i - 1] * A[k][l]
				sum_init = sum_init + index

			f[l][i] = sum_init * E[l][X[i]]

	# calculate f for End state at position L-1
	sum_init = 0
	for l in AEMatrices.emittingStates:
		index = f[l][L] * A[l]['E']
		sum_init = sum_init + index

	f['E'][L + 1] = sum_init

	##########################
	### END YOUR CODE HERE ###
	##########################

	# return forward matrix
	return f


# Backward algorithm, takes a sequence X and the nr. of symbols in of the sequence (L) as inputs
# It uses  A, E, allStates, emittingStates, emissionSymbols from AEMatrices
# Output: backward matrix (in form of dictionary)
# usage example: b = backward(sequence, L)
# b[k][i], backward of state k, at sequence position i
# note that we count from L+1,L,....,2,1,0
# where 0 indicates the begin state and L+1 the end state
def backward(X,L):
	b= dict()
	# initialise b to '0'
	for k in allStates:
		b[k] = [0]*(L+2)

	# initialise end state
	for k in allStates:
		b[k][L] = A[k]['E']

	#############################
	### INSERT YOUR CODE HERE ###
	#############################
		# iterate over sequence
		for i in range(L - 1, 0, -1):
			for k in AEMatrices.emittingStates:
				sum_init = 0
				for l in AEMatrices.emittingStates:
					index = A[k][l] * E[l][X[i + 1]] * b[k][i + 1]
					sum_init = sum_init + index
				b[k][i] = sum_init
		# calculate probability
		# Finalice begining state
		sum_init = 0
		for l in AEMatrices.emittingStates:
			index = A["B"][l] * E[l][X[1]] * b[l][1]
			sum_init = sum_init + index

		b['B'][0] = sum_init
	##########################
	### END YOUR CODE HERE ###
	##########################

	# return backward matrix
	return b

#Calculate the transition probability from state k to state l given the training sequence X and forward and backward matrix of this sequence.
#Output: Transition probability matrix (in form of dictionary)
def transitionP(f,b,X,L):
	aP=dict()

	# initialise aP
	for k in AEMatrices.allStates:
		aP[k] = dict()
		for l in allStates:
			aP[k][l]=0

	# iterate over sequence
	for k in AEMatrices.allStates:
		for l in AEMatrices.emittingStates:

			# calculate probability of transition k->l at position i
			z = 0
			for i in range(0,L):
				z += f[k][i]*A[k][l]*E[l][X[i+1]]*b[l][i+1]
			aP[k][l] = z

	# add transition to end state
	for k in AEMatrices.allStates:
		aP[k]['E'] = aP[k]['E'] + f[k][L]*A[k]['E']
	# print aP
	return aP

#Calculate the emission probability of symbol s from state k given the training sequence X and forward and backward matrix of this sequence.
#Output: Emission probability matrix (in form of dictionary)

def emissionP(f,b,X,L):
	eP=dict()
	# initialise tP
	for l in emittingStates:
		eP[l] = dict()
		for s in emissionSymbols:
			eP[l][s]=0

	# iterate over sequence
	for l in emittingStates:
		for s in emissionSymbols:
			z = 0
			for i in range(1,L+1):

			# calculate probability symbol s at state k
				if s == X[i]:
					z += f[l][i]*b[l][i]
			eP[l][s] = z
	return eP



# returns probability given the forward matrix
def getProbabilityForwardX(f,L):
	return (f['E'][L+1])

# Baum-Welch algorithm, takes a set of training sequences setX as input
# Output: the new A matrix, new E matrix and the total sum of the log likelyhood, all in a single list
# usage example: (newA, newE, sumLL) = baumWelch(setX)

def baumWelch(setX, conv):
	# initialise emission counts matrix
	# eC[k][s] is the expected number of counts for emission symbol s
	# at state k
	eC = dict()
	for k in allStates:
		eC[k] = dict()
		for s in emissionSymbols:
			# DO NOT add pseudo counts
			# add a pseudocounts so p(x) would never be 0 and the would not be a division by 0
			eC[k][s] = 0 + 0.001;

	# initials transition count matrix
	# aC[k][l] is the expected number of transitions from
	# state k to state l
	aC = dict()
	for k in allStates:
		aC[k] = dict()
		for l in allStates:
			# DO NOT add pseudo counts 
			aC[k][l] = 0;
			if (l != "E" and l != "B"):
				aC[k][l] = 0 + 0.001;
	# sum over log likelihood
	sumLL = 0.0

	# iterate over training sequences
	for X in setX:
		L = len(X) - 2


	#############################
	### INSERT YOUR CODE HERE ###
	#############################

	# you may use the following functions defined above:
	# forward, backward, getProbabilityX, emissionP, transitionP
		f = forward(X, L)
		b = backward(X, L)
	# here you should calculate eC and aC,
	# the matrices for the number of expected counts
	# also calculate your sumLL, the sum over the logodds
	# of all the sequences in the training set.
		pX = getProbabilityForwardX(f, L)
	# add emission counts
		aP = transitionP(f, b, X, L)
	# add transition counts
		eP = emissionP(f, b, X, L)
	# add sum over log likelihood
		sumLL += math.log10(pX)
		# add transition counts
		for k in allStates:
			for l in allStates:
				aC[k][l] += (aP[k][l])/(pX)

		# add emission counts
		for l in emittingStates:
			for s in emissionSymbols:
				eC[l][s] += (eP[l][s]/(pX))
	##########################
	### END YOUR CODE HERE ###
	##########################

	# finish iteration

	# calculate new transitions
	# initialisie new transition matrix newA
	newA = dict()
	for k in allStates:
		newA[k] = dict()
		sum_l = 0

	#############################
	### INSERT YOUR CODE HERE ###
	#############################

		for l in allStates:
			newA[k][l] = 0
			sum_l += aC[k][l]

		for l in allStates:
			if (k != "E"):
				newA[k][l] = (aC[k][l]) / sum_l

	##########################
	### END YOUR CODE HERE ###
	##########################

	# calculate new emissions
	# initialise new emission matrix newE
	newE = dict()
	for k in emittingStates:
		newE[k] = dict()
		sum_s = 0

		#############################
		### INSERT YOUR CODE HERE ###
		#############################

		for s in emissionSymbols:
			newE[k][s]= 0
			#sum of the probaility of all the simbls trhough a state
			sum_s += eC[k][s]



		### here you should calculate your new emission
		for s in emissionSymbols:
			newE[k][s] = (eC[k][s]) / sum_s


		##########################
		### END YOUR CODE HERE ###
		##########################

	return (newA, newE, sumLL)

# finish BaumWelch
