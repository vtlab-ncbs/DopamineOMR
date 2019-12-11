try:
	from ij_util import *
except ImportError:
	from ij.IJ import runMacro
	mssg = "Please install the plugin ij_util !"
	runMacro('showMessage("'+mssg+'")')

import sys
sys.path.append('/Users/urvashijha/Desktop/FishTail/')

from TailTipTracker import *



def linspace(start, stop, n):
	indices = []
	chunk_size = (stop-start)/float(n)
	val = 0
	while val <= stop:
		indices.append(int(val))
		val += chunk_size
	return indices
rename(“PROC”)


#1. Find all tail extremes
waitForUser("Before clicking OK, select an anterior point !")
anteriors, posteriors, allpoints = getTailExtremes(ROIADD=True)
#texs = anteriors, posteriors = getTailExtremes(ROIADD=True, ONSKEL=False)

#print posteriors

#NOTE: Anterior point is 'init' and posterior point is 'goal' for every slice

selectWindow("PROC")
print "Specifying fields..."
#points from a fish's tail mask, goal and init represent a fieldspec
fieldspecs = []
for k in range(getNSlices()):
	setSlice(k+1)
	#2. With an init and a goal for every slice compute the heuristic for each slice
	#A heuristic has a value 0 at the goal and increases maximally by the time init is reached
	print "Constructing heuristic...", k
	heuristic = computeHeuristic(allpoints[k], anteriors[k], posteriors[k], VIS=False)
	fieldspecs.append([k+1, allpoints[k], anteriors[k], posteriors[k], heuristic])

roiDeselect()
selectNone()
roiDelete()

#. A* search from init to goal for each slice, store the minimal path thus obatained
# --> This is the minimal, digitised fish tail !
selectWindow("PROC")
print "Fitting splines..."
rawsplines = []
for sliceindex, points, init, goal, heuristic in fieldspecs:
	print sliceindex, len(points), init, goal, type(heuristic)
	rawsplines.append(getAStarPath(sliceindex, points, init, goal, heuristic))
print len(rawsplines)
nsegs = 8
j = 1
print "Making splines..."
for rawspline in rawsplines:
	setSlice(j)
	print rawspline
	print len(rawspline)
	if len(rawspline)<100:
		print rawspline
	indices = linspace(0,len(rawspline)-1,nsegs)
	#spline = [rawspline[k] for k in range(0,len(rawspline),len(rawspline)/nsegs)]
	spline = [rawspline[k] for k in indices]
	makeSpline(*spline)
	roiAdd()
	j += 1
