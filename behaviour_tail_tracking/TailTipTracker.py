from __future__ import with_statement

try:
	from ij_util import *
except ImportError:
	from ij.IJ import runMacro
	mssg = "Please install the plugin ij_util !"
	runMacro('showMessage("'+mssg+'")')

from ij_util import *
from os.path import join as pjoin
from csv import writer


delta = [[-1, 0], # go up
		 [ 0,-1], # go left
		 [ 1, 0], # go down
		 [ 0, 1]] # go right



#Returns index of the point, from the list of all points,
#that is closest to the source point
#point: the source point
#allpoints: list of all points
def closestpt(srcpoint,allpoints):
	enumpoints = enumerate(allpoints)
	pt = min(enumpoints, key = lambda pt: euclidean(pt[1], srcpoint))
	point = allpoints[pt[0]]
	return tuple(map(int, point))


def getAStarPath(sliceindex, points, init, goal, heuristic, VIS=False):

	setSlice(sliceindex)

	init = tuple(init)
	goal = tuple(goal)

	# { Point : Value } dictionary
	closed = dict(zip(points, (0,)[:]*len(points)))	#the fish itself as a field to be explored (i.e. "expanded")
	closed[init] = 1	#start expanding at the anterior cell

	x = init[0]
	y = init[1]
	g = 0

	cost = 1

	open_list = [[0, g, x, y]]

	opti_path = [(x,y)]

	found = False  # flag that is set when search is complete
	resign = False # flag set if we can't find expand
	
	while not found and not resign:
		if len(open_list) == 0:
			resign = True
			print "Fail", sliceindex
			wait(5000)
			return "Fail"
		else:
			open_list.sort()
			open_list.reverse()
			next = open_list.pop()
			x = next[2]
			y = next[3]
			g = next[1]

			opti_path.append((x,y))

			if VIS:
				makePoint(x,y)
				wait(10)
			
			if x == goal[0] and y == goal[1]:
				print 'Yippeee!'
				found = True
			else:
				for i in range(len(delta)):
					x2 = x + delta[i][0]
					y2 = y + delta[i][1]
					if closed.has_key((x2,y2)):
						if closed[(x2,y2)] == 0:
							g2 = g + cost
							h = g2 + heuristic[(x2,y2)]
							open_list.append([h, g2, x2, y2])
							closed[(x2,y2)] = 1

	return opti_path


def computeHeuristic(points, init, goal, VIS=False):
	# Derived from the basic search algorithm that uses
	# Expand and g-value logic

	init = tuple(init)
	goal = tuple(goal)
	
	heuristic = {}

	cost = 1
	
	# { Point : Value } dictionary
	closed = dict(zip(points, (0,)[:]*len(points)))	#the fish itself as a field to be explored (i.e. "expanded")
	closed[goal] = 1	#start expanding at the posterior cell

	x = goal[0]
	y = goal[1]
	g = 0

	heuristic[goal] = g

	open_list = [[g, x, y]]

	done = False # flag set if we can't find expand
	
	while not done:

		#We are done :)
		if len(open_list) == 0:
			done = True

		#We are still expanding...
		else:
			open_list.sort()	#sort by g-value
			open_list.reverse()	#descending order
			next = open_list.pop()
			x = next[1]
			y = next[2]
			g = next[0]


		for i in range(len(delta)):
			x2 = x + delta[i][0]
			y2 = y + delta[i][1]
			if closed.has_key((x2,y2)):	#Are we in the fish ?
				if closed[(x2,y2)] == 0:
					g2 = g + cost
					open_list.append([g2, x2, y2])
					closed[(x2,y2)] = 1
					heuristic[(x2,y2)] = g2
					#Visualize
					if VIS:
						x2,y2 = map(int, (x2,y2,))
						makePoint(x2,y2)
						wait(10)
	return heuristic


#Derived from the basic search algorithm that uses
# Expand and g-value logic
def findTailTip(points,init,VIS=False):
	# ----------------------------------------
	# insert code here
	# ----------------------------------------

	cost = 1
	
	# { Point : Value } dictionary
	closed = dict(zip(points, (0,)[:]*len(points)))	#the fish itself as a field to be explored (i.e. "expanded")
	closed[init] = 1	#start expanding at the anterior cell

	x = init[0]
	y = init[1]
	g = 0

	open_list = [[g, x, y]]

	done = False # flag set if we can't find expand
	
	while not done:

		#We are done :)
		if len(open_list) == 0:
			done = True
			x,y = map(int, (x,y,))	#Found our goal -> the fish's tail tip !
			#makePoint(x,y)
			return (x,y)

		#We are still expanding...
		else:
			open_list.sort()	#sort by g-value
			open_list.reverse()	#descending order
			next = open_list.pop()
			x = next[1]
			y = next[2]
			g = next[0]


		for i in range(len(delta)):
			x2 = x + delta[i][0]
			y2 = y + delta[i][1]
			if closed.has_key((x2,y2)):	#Are we in the fish ?
				if closed[(x2,y2)] == 0:
					g2 = g + cost
					open_list.append([g2, x2, y2])
					closed[(x2,y2)] = 1
					#Visualize
					if VIS:
						x2,y2 = map(int, (x2,y2,))
						makePoint(x2,y2)
						wait(10)


#Smoothener, substitutes current value by MEAN over a w-sized window centered on the current value
#arr is a list of 2D points
def smoothenpoints(arr):
	return map(smoothenlist, arr)


#arr is a 1D list of values
def smoothenlist(arr):
	arr = list(arr)
	w = 1
	smootharr = [mean(arr[k-w:k+w+1]) for k in range(w,len(arr)-w)]
	smootharr = map(int, smootharr)
	smootharr = arr[:w] + smootharr
	if len(arr) > 1:
		smootharr += arr[-w:]
	#print "b&a smoothing", len(arr) - len(smootharr)
	return smootharr

#Loop over the entire stack and find and return the [anterior, posterior, allpoints] for each slice
def getTailExtremes(ONSKEL=True, SMOOTH=True, ROIADD=False, SAVE=False):

	anterior = getSelectedPoint()
	print anterior

	#Perform g-value - expand search on a skeletonised single dilated mask
	if ONSKEL:
		duplicate("SKEL")
		bin_skel()
		bin_dilate()
		selectWindow("SKEL")
	
	tailextremes = []	#a list to hold the [anterior, posterior] pair of points for all tail tips
	anteriors = []
	posteriors = []

	allpoints = []
	
	for i in range(getNSlices()):
		#print i
		setSlice(i+1)
		points = zip(*pointsFromMask(noselect=True))
		allpoints.append(points)
		seed = closestpt(anterior, points)
		anteriors.append(seed)
		x,y = findTailTip(points, seed, VIS=False)
		posteriors.append((x,y))

	if SMOOTH:
		#Smoothen out the jitter
		print "Smoothening tail extreme points..."
		anteriors = smoothenpoints(anteriors)
		posteriors = smoothenpoints(posteriors)

	if ROIADD:
		#Add tail-tip points to ROI manager
		k = 0
		for x,y in posteriors:
			setSlice(k+1)
			selectNone()
			makePoint(x,y)
			#wait(1000)
			roiAdd()
			k += 1

	if ONSKEL:
		selectWindow("SKEL")
		close()
	
	#Save tail-tip points to a .CSV file
	if SAVE:
		data = [a+p for a,p in zip(anteriors, posteriors)]
		datapath = "/Users/urvashijha/Desktop/data/"
		with open(pjoin(datapath, "tailextremes.csv"), 'wb') as f:
			w = writer(f, delimiter=",")
			w.writerow(("Ax","Ay","Px","Py",))
			for ax,ay,px,py in data:
				w.writerow([ax,ay,px,py])
	
	print "Done!"
	return [anteriors, posteriors, allpoints]


if __name__ == "__main__":
	#Get Tail Extremes
	#texs = anteriors, posteriors, allpoints = getTailExtremes(ROIADD=True, SMOOTH=False, ONSKEL=False)
	#print len(texs[0]), "tail points"
	#print texs

	#Compute fieldspecs
	#fieldspecs = []
	#for k in range(getNSlices()):
	#	setSlice(k+1)
	#	heuristic = computeHeuristic(allpoints[k], anteriors[k], posteriors[k], VIS=False)
	#	fieldspecs.append([k+1, allpoints[k], anteriors[k], posteriors[k], heuristic])

	#Compute A* Paths
	#for sliceindex, points, init, goal, heuristic in fieldspecs:
	#	print sliceindex, len(points), init, goal, type(heuristic)
	#	getAStarPath(sliceindex, points, init, goal, heuristic, VIS=False)

	
	#Save tail extremes to CSV
	getTailExtremes(ROIADD=True, SMOOTH=True, ONSKEL=False, SAVE=True)
