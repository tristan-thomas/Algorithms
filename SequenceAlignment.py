import numpy as np 
import random
import time
import matplotlib.pyplot as plt


def printTable(commonSStrings, song1):
	print(' ____________________________')
	print('|---- Plagarism Results -----|')
	print('|Length |   Common Sub String|') 
	print('|'+'-'*(len(commonSStrings[len(commonSStrings)-1])+10)+'|')
	for i in range(len(commonSStrings)):
		x = str(len(commonSStrings[i]))
		print (x.ljust(10, ' '),end = '') 
		x = commonSStrings[i]
		print(x.rjust(0, ' '))
	print('-'*(len(commonSStrings[len(commonSStrings)-1])+10)+'|')

def printMatrix(S, x, y):
	print('       ' + y[0]+'  ',end = '')
	for i in range(1, len(y),1):
		print(str(y[i])+'  ',end='')
	print()
	i = -1
	for line in S:
		if i > -1:
			print(x[i] + ' ' + str(line))
		else:
			print('  '+str(line))
		i += 1


# _Params_
# x,y := strings
# cInsert, cDelete, cSub := costs of insert, delete, sub operations
# _Return_
# S[] = optimal cost matrix
# := Takes (x,y and costs) and produces cost matrix with optimal costs
#    for all the subproblems aligning the strings x and y
def alignStrings(x, y, cInsert, cDelete, cSub):
	S = np.array([[0] * (len(y) + 1)]* (len(x) + 1))

	for i in range(0,len(y) + 1):
		S[0][i] = i*cInsert

	for i in range(0,len(x) + 1):
		S[i][0] = i*cInsert

	for i in range(1, (len(x) + 1)):
		for j in range(1, (len(y) + 1)):
			if i > 0 or j > 0:
				if x[i-1] != y[j-1]:
					cost1 = (S[(i-1), (j-1)] + cSub )
					cost2 = (S[i, (j-1)] + cInsert )
					cost3 = (S[(i-1), j] + cDelete )
					S[i,j] = min(cost1, cost2, cost3)
				else:
					S[i,j] = S[(i-1), (j-1)]
	return(S)


# _Params_
# S := optimal cost Matrix
# x,y := strings
# cInsert, cDelete, cSub := costs of insert, delete, sub operations
# _Return_
# vector x = optimal sequence of edit ops to convert x -> y
# := Finds a path on the implicict DAG of decisions made by
#    alignStrings() to obtain S(n,n) starting from S[0,0]
def extractAlighnments(S, x, y, cInsert, cDelete, cSub):
	a = []
	i = len(x)
	j = len(y)

	while j > -1 and i > -1:
		ties = []
		cost1 = (S[(i-1), (j-1)])
		cost2 = (S[i, (j-1)])
		cost3 = (S[(i-1), j])
		minSubProb = min(cost1, cost2, cost3)

		if minSubProb == cost1: 
			if S[i][j] == S[(i-1), (j-1)]: # No-Op
				ties.append('no-op')
			else:
				ties.append('sub')
		if minSubProb == cost2:
			ties.append('ins')
		if minSubProb == cost3:
			ties.append('del')

		operation = random.choice(ties)
		a.append(operation)

		# Move indices accordingly
		if operation == 'no-op' or operation == 'sub':
			i -= 1
			j -= 1
		elif operation == 'ins':
			j -= 1
		else: # Del case
			i -= 1
	##########


	######### This works correctly, no random tie breaks
	# a = []
	# i = len(x)
	# j = len(y)
	# operations = [0] * 3 # 1 is sub, 2 is insert, 3 delete
	# while j > -1 and i > -1:
	# 	ties = []
	# 	operations[0] = S[(i-1), (j-1)] #sub
	# 	operations[1] = S[i, (j-1)] #insert
	# 	operations[2] = S[(i-1), j] #delete
	# 	minSubProb = min(operations[0], operations[1], operations[2])
	# 	if minSubProb == operations[0]: # sub/no-op happened
	# 		if S[i][j] == S[(i-1), (j-1)]:
	# 			a.append('no-op')
	# 		else:
	# 			a.append('sub')
	# 		i -= 1
	# 		j -= 1
	# 	elif minSubProb == operations[1]: # insert happened
	# 		a.append('ins')
	# 		j -= 1
	# 	else: # Delete happened
	# 		a.append('del')
	# 		i -= 1
	########## This works correctly

	del a[-1]
	return(a)



# _Params_
# x := string
# L = int, length of substrings 1<=L<=len(x)
# a = vector, optimal sequene of edits to transform(x->y)
# _Return_
# set of substrings that align exactly to a substring in y
# := finds each of the substrings of length >= L in x that 
#    align exactly, via a run of no-ops, to a substring in y
def commonSubstrings(x, L, a):	
	a.reverse()

	commonSubstrings = []
	lenA = len(a) - 1
	lenX = len(x) - 1

	i = 0
	index = 0

	while i < lenA:
		if a[i] != 'ins':
			consecNoOps = 1
			if a[i : i+L] == ['no-op']*L:
				consecNoOps = i
				while a[consecNoOps] == 'no-op' and consecNoOps < lenA:
					consecNoOps += 1
				if consecNoOps == lenA and a[consecNoOps] == 'no-op': # check for last index of a
					consecNoOps += 1
				consecNoOps -= i #this is num of consecNoOps
				commonSubstrings.append(x[index : index+consecNoOps])
			# increment i by consecNoOps, inc index by conseqNoOps
			i += consecNoOps
			index += consecNoOps
		# increment i, do not increment index 
		# this is an insert case	
		else:
			i += 1	

	return commonSubstrings
		


def main():

	############ Testing words
	print('------- TESTING WORDS -------')

	cInsert = 1
	cDelete = 1
	cSub = 1

	x = 'THEIR'
	y = 'THERE'

	print('Source = ' +str(x))
	print('Target = ' +str(y))

	L = 2

	S = alignStrings(x, y, cInsert, cDelete, cSub)
	print(S)
	print()
	a = extractAlighnments(S, x, y, cInsert, cDelete, cSub)
	print(a)
	print()
	commonSStrings = commonSubstrings(x, L, a)
	# print(commonSStrings)
	printTable(commonSStrings,'')
	print()


	print('------- TESTING WORDS -------')

	x = 'EXPONENTIAL'
	y = 'POLYNOMIAL'

	print('Source = ' +str(x))
	print('Target = ' +str(y))

	cInsert = 2
	cDelete = 1
	cSub = 2

	L = 2

	S = alignStrings(x, y, cInsert, cDelete, cSub)
	printMatrix(S,x,y)
	print()
	a = extractAlighnments(S, x, y, cInsert, cDelete, cSub)
	print(a)
	print()
	commonSStrings = commonSubstrings(x, L, a)
	# print(commonSStrings)
	printTable(commonSStrings,'')
	print()
	############ End Testing words


	############ Testing for plagarism
	# cInsert = 1
	# cDelete = 1
	# cSub = 1
	# song1 = open("Song1_Folsom_Prison.txt","r")
	# song2 = open("Song2_Crescent_City_Blues.txt","r")

	# L = 10

	# song1 = song1.read()
	# song2 = song2.read()

	# S = alignStrings(song1, song2, cInsert, cDelete, cSub)

	# print(S)
	# print()
	# a = extractAlighnments(S, song1, song2, cInsert, cDelete, cSub)
	# # print(a)
	# print()
	# commonSStrings = commonSubstrings(song1, L, a)
	# # print(commonSStrings)
	# printTable(commonSStrings,'')
	# print()
	# lenSource = len(song1)
	# plagScore = lenSource - S[len(song1)][len(song2)]
	# print('Length of source: ' + str(lenSource))
	# print('Plagarism Detected: ' + str(plagScore))
	# print('Results = ' + str(plagScore/lenSource))
	############ End testing for plagarism


	############ Part B
	# letters = ['A','B','C','D','E','F','G','H','I','J','K','L',
	# 	'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	# x = []
	# y = []
	# L = 2

	# runtime = []
	# sizeOfInputs = []
	# for i in range(10, 500, 20):
	# 	start = time.perf_counter()
	# 	x = []
	# 	y = []
	# 	for j in range(i):
	# 		x.append([random.choice(letters)])
	# 		y.append([random.choice(letters)])
	# 	soln=commonSubstrings(x, L, extractAlighnments( 
	# 					alignStrings(x, y, cInsert, cDelete, cSub),
	# 					x, y, cInsert, cDelete, cSub
	# 					 ))
	# 	finish = time.perf_counter()
	# 	runtime.append((finish - start)*1000)
	# 	sizeOfInputs.append(i)

	# # to graph runtime against
	# runtime = np.array(runtime)
	# sizeOfInputs = np.array(sizeOfInputs)
	# y1 = np.array([(i*np.log(i)) for i in sizeOfInputs])
	# y2 = np.array([(i**2) for i in sizeOfInputs])

	# fig, ax = plt.subplots()
	# ax.plot(sizeOfInputs, runtime, color='#000000', label = "Time to run")
	# ax.plot(sizeOfInputs, y1, color='#FF0033', label = "nlog(n)")
	# # ax.plot(sizeOfInputs,y2, color='#3300FF', label = "n*n")

	# plt.xlabel('Size of Source Input(n)',fontsize=12)
	# plt.ylabel('Runtime (seconds/1000)',fontsize=12)
	# plt.title("Runtime of Plagarism Checker")
	# plt.legend()
	# plt.show()
	############ End Part B

main()







