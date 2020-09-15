import numpy as np 
import matplotlib.pyplot as plt
import sys
import io

def partition(A,p,r):
	global comps
	x = A[r]
	i = p-1
	for j in range(p,r):
		comps+=1
		if A[j] <= x:
			i+=1
			A[j], A[i] = A[i], A[j]
	A[i+1], A[r] = A[r], A[i+1]
	return i+1

def QuickSelect(A,p,r,split):
	if(r-p+1 > 1): 
		k = int(split*len(A))
		q = partition(A,p,r)
		if k == q:
			return q
		elif k < q:
			return QuickSelect(A,p,q-1,split)
		else:
			return QuickSelect(A,q+1,r,split)
	else:
		return r

def QuickSort(A,p,r):
	if p < r:
		k = ((r-p+1) * 0.25) + p
		q = QuickSelect(A,p,r,k/len(A))
		print('A = ' + str(A)+' | p = ' + str(p) + ', r = ' + str(r))
		QuickSort(A,p,(q-1))
		QuickSort(A,(q+1),r)

def test():
	global comps

	# Disable printing so print statements in QuickSort do not 
	# print for our calls with values [2,...,2^10]
	dontPrint = io.StringIO()
	sys.stdout = dontPrint

	results = [0] * 10
	for i in range(1,11):
		comps = 0
		arr = np.array([k for k in range(1,2**i)])
		np.random.shuffle(arr)
		QuickSort(arr,0,len(arr)-1)
		results[i-1] = comps
	x = np.array([2**i for i in range(1,11)])
	y = np.array([(i*np.log(i)) for i in x])
	y2 = np.array([(i**2) for i in x])
	fig, ax = plt.subplots()
	ax.plot(x, results, color='#000000', label = "Comparisons to sort")
	ax.plot(x, y, color='#FF0033', label = "nlog(n)")
	ax.plot(x,y2, color='#3300FF', label = "n*n")
	

	# Enable printing 
	sys.stdout= sys.__stdout__
	
	
	arr = np.array([k for k in range(1,6)])
	np.random.shuffle(arr)
	print("Array, n= 5:" + str(arr))
	QuickSort(arr,0,len(arr)-1)

	arr = np.array([k for k in range(1,11)])
	np.random.shuffle(arr)
	print("\nArray, n= 10:" + str(arr))
	QuickSort(arr,0,len(arr)-1)

	arr = np.array([k for k in range(1,21)])
	np.random.shuffle(arr)
	print("\nArray, n= 20:" + str(arr))
	QuickSort(arr,0,len(arr)-1)


	plt.xlabel('Size of Array(n)',fontsize=12)
	plt.ylabel('Comparisons',fontsize=12)
	plt.title("QuickSelect Comparisons")
	plt.legend()
	plt.show()

test()

