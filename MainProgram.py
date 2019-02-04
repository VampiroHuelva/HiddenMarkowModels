#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The main program of HMM.

This script serves as the main program to implement HMM by calling other
modules.
"""

import BaumWelch
import Viterbi
import AEMatrices
import Sequences
import argparse
import sys
import os


def viterbiAlgorithm(seq, a, e):
	"""Run the Viterbi algorithm and saves the Viterbi Matrix and the Back Trace Matrix in an output folder.
	"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Perform the Viterbi algorithm on the first sequence of the set setX
	# and store the viterbi matrix in the variable vi and the back trace matrix in variable backTrace
	(vi, backTrace, probability) = Viterbi.viterbi(setX[0])

	# Print the output matrices of Viterbi algorithm
	Viterbi.writePathMatrix(vi, setX[0], "output/ViterbiMatrix.tsv")
	Viterbi.writePathMatrix(backTrace, setX[0], "output/BackTraceMatrix.tsv")
	#Print the vitervi path instead of the vitervi backtrace
	with open('ViterbiPath.txt', 'w') as text_file:
		print('Path: {}.'.format(Viterbi.generateStateSeq(backTrace, setX[0])), file = text_file)

	# Print the most likely sequence path of x according to the viterbi algorithm
	print('Most likely state is {0}, with probability of {1}'.format(''.join(Viterbi.generateStateSeq(backTrace, setX[0])), probability))


def forwardAlgorithm(seq, a, e):
	"""Prints the forward probability for a given sequence"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Obtain the forward matrix
	f = BaumWelch.forward(setX[0], len(setX[0]) - 2)
	AEMatrices.writeForwardMatrix(f, 'output/forward_matrix.tsv')
	print('\nForward probability for sequence {0}:\n{1}'.format(''.join(setX[0]).strip(), BaumWelch.getProbabilityForwardX(f, len(setX[0]) - 2)))


def backwardAlgorithm(seq, a, e):
	"""Prints the backward probability for a given sequence"""
	# Read the A and E matrices
	AEMatrices.init(e, a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")

	# Obtain the backward matrix
	b = BaumWelch.backward(setX[0], len(setX[0]) - 2)
	AEMatrices.writeBackwardMatrix(b, 'output/backward_matrix.tsv')
	print('\nBackward probability for sequence {0}:\n{1}'.format(''.join(setX[0]).strip(), b['B'][0]))


def baum_welchAlgorithm(seq, a, e, convergence):
	"""Performe the Baum Welch algorithm. If convergence is true, then it should perform the training (for you to code)"""
	# Read the A and E matrices
	AEMatrices.init(e, a)
	print(a)

	# Read the input sequence(s) and store them into setX
	setX = Sequences.readSeq(seq, "X")



	w = BaumWelch.baumWelch(setX, convergence)

	print("\n SummLL is")
	print(w[2])
	# Number of iterations, at this point there is already one iteration
	max_i = 1
	AEMatrices.writeAMatrix(w[0], 'output/NewA.tsv')
	AEMatrices.writeEMatrix(w[1], 'output/NewE.tsv')

### Iterate the training until convergence or until max iter nº

	while (convergence) and (max_i < 15):
		#Uses the new transition and emision probabilities calculated in the last B-W training
		print("\n Iteration number")
		print(max_i)
		prev_sum_LL = w[2]
		AEMatrices.init('output/NewE.tsv', 'output/NewA.tsv')
		w = BaumWelch.baumWelch(setX, convergence)
		print("\n New A and E")
		sum_LL = w[2]
		print(w[0])
		print("\n")
		print(w[1])
		print("\n SummLL is")
		print(w[2])
		max_i = max_i + 1
		AEMatrices.writeAMatrix(w[0], 'output/NewA.tsv')
		AEMatrices.writeEMatrix(w[1], 'output/NewE.tsv')
		# Set the stop criterium
		converg_num = sum_LL - prev_sum_LL
		print(converg_num)
		#if (converg_num == 0.0):
			#convergence = False





def parser():
	"""Retrieves the arguments from the command line.
	"""

	parser = argparse.ArgumentParser(description='A program to run HMM algorithms.')

	parser.add_argument('-v', dest='viterbi', action='store_true', help='[-v] to run the Viterbi algorithm')
	parser.add_argument('-f', dest='forward', action='store_true', help='[-f] to run the Forward algorithm')
	parser.add_argument('-b', dest='backward', action='store_true', help='[-b] to run the Backward algorithm')
	parser.add_argument('-w', dest='baum_welch', action='store_true', help='[-w] to run the Baum-Welch algorithm')
	parser.add_argument('-c', dest='convergence', action='store_true',
						help='[-c] to reach convergence, leave empty for doing only 1 iteration', default=False)
	parser.add_argument('-am', required=True, metavar='transmission_matrix_file', dest='transitionMatrix',
						help='[-am] to select transmission matrix file')
	parser.add_argument('-em', required=True, metavar='emission_matrix_file', dest='emissionMatrix',
						help='[-em] to select emission matrixfile ')
	parser.add_argument('-s', required=True, metavar='sequence_file', dest='sequence',
						help='[-s] to select sequence file')


	arguments = parser.parse_args()  # takes the arguments

	if arguments.viterbi == True:  # Do the Viterbi algorithm
		algorithm = 'viterbi'
	elif arguments.forward == True:  # Do the forward_backward algorithm
		algorithm = 'forward'
	elif arguments.backward == True:  # Do the forward_backward algorithm
		algorithm = 'backward'
	elif arguments.baum_welch == True:  # Do the Baum-Welch algorithm
		algorithm = 'baum_welch'

	# Kept here just in case
	else:
		print('This shouldn\'t happen')
		sys.exit()

	return [algorithm, arguments]


def main():
	"""Main function. This function checks the chosen arguments and files and calls the right function.
	"""
	if not os.path.exists('output'):
		os.makedirs('output')

	algorithm, args = parser()

	input_sequence = args.sequence
	a_matrix = args.transitionMatrix
	e_matrix = args.emissionMatrix

	if algorithm == 'viterbi':
		viterbiAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'forward':
		forwardAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'backward':
		backwardAlgorithm(input_sequence, a_matrix, e_matrix)
	elif algorithm == 'baum_welch':
		baum_welchAlgorithm(input_sequence, a_matrix, e_matrix, args.convergence)


if __name__ == "__main__":
	main()

print('\n"A hidden connection is stronger than an obvious one."\n-Heraclitus of Ephesus\n')
