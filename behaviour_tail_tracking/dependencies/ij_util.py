'''
Library Usage: Include the following code at the beginning of your Jython plugin code

-----------------------------------------
try:
	from ij_util import *
except ImportError:
	from ij.IJ import runMacro
	mssg = "Please install the plugin ij_util !"
	runMacro('showMessage("'+mssg+'")')
-----------------------------------------

'''


from ij.measure import ResultsTable as RT
from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi, PolygonRoi
from ij.plugin import ImageCalculator as IC, Duplicator
from os.path import join as pjoin
import pickle
from ij.gui import Line
from math import sqrt
from ij.IJ import open as imopen
from ij import WindowManager as WM
from os import listdir, walk
from os.path import isfile
from ij.io import DirectoryChooser as DirCh
from ij.io import OpenDialog as OD



def closeAllImgs():
	imids = WM.getIDList()
	if imids:
		[WM.getImage(imid).close() for imid in imids]

def dirchooser():
	dc = DirCh("Choose data folder...")
	return dc.getDirectory()

def filechooser():
	od = OD("Choose image data file...")
	return (od.getPath(), od.getFileName(), od.getDirectory())


def despeckle():
	run("Despeckle", "stack")


def makeBBox():
	run("To Bounding Box")


def findModulePath(module_name, codebase):
    name = module_name + ".py"
    for root, dirs, files in walk(codebase):
        if name in files:
            return root
    raise ImportError(module_name)


def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5


def getImage():
	return IJ.getImage()

def listFiles(path, ext):
	return [pjoin(path,filename) for filename in listdir(path)
			if isfile(pjoin(path,filename))
			and filename.endswith(ext)
		]


def removeScale():
	run("Set Scale...", "distance=0 known=0 pixel=1 unit=pixel")


def clearOutside():
	#run("Clear Outside")
	run("Clear Outside", "stack");


def fill():
	run("Fill", "slice")

def draw():
	run("Draw", "slice")



#Logging functions
#-----------------------------------------------------
def log(stuff):
	IJ.log(stuff)


#Image Calculator functions
#------------------------------------------------------

def getPixelValue(x,y):
	imp = getImage()
	if img.getType() == ImagePlus.GRAY8:
		return imp.getPixel(x,y)[0]


def calculate(str_comm,imp1,imp2):
	ic = IC()
	ic.run(str_comm,imp1,imp2)


#Math functions
def mean(arr):
	return sum(arr)/float(len(arr))


#Euclidean distance
#p1,p2 are points in 2D
def euclidean(p1,p2):
	return sqrt(float((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2))


#"Metadata" functions - applicable to TIFF format files
#------------------------------------------------------
def setMetadata(dictobj):
	namespace = "CUSTOM_INFO"
	


def ImageJDirPath():
	return IJ.getDirectory("imagej")


#user input / dialog Functions
#-------------------------------

"""
	Get and return user specified String input
"""
def getString(mssg,default):
	return IJ.getString(mssg,default)


"""
	 Delays 'msecs' milliseconds.
"""
def wait(msecs):
	IJ.runMacro('wait('+str(msecs)+')')



"""
	 Waits for user input and shows non-modal mssg.
"""
def waitForUser(mssg):
	IJ.runMacro('waitForUser("'+mssg+'")')

"""
	 Shows modal mssg.
"""
def showMessage(mssg):
	IJ.runMacro('showMessage("'+mssg+'")')


"""
	Saves the image to path
"""
def save(path):
	IJ.save(path)


def setAutoThreshold(darkbg=False):
	imp = IJ.getImage()
	args = "Default"
	if darkbg:		args += " dark"
	IJ.setAutoThreshold(imp, args)


def setThreshold(lt, ut):
	IJ.setThreshold(lt,ut)


def to8bit():
	run("8-bit", "")


def loadROI(path,roiname):
	IJ.open(pjoin(path,roiname))


"""
	Load the images stack
"""
def loadStack(path,count,start):
	run("Image Sequence...", "open=["+path+"] number="+str(count)+" starting="+str(start)+" increment=1 scale=100 file=[] sort")


"""
	Load FULL video stack
"""
def loadMovieFull(path):
	IJ.open(path)


"""
	Load the video stack
"""
def loadMovie(path,start,end):
	run("AVI...", "select=["+path+"] first="+str(start)+" last="+str(end))
	run("In")


"""
	Load the video stack in 8-bit mode
"""
def loadMovie8bit(path,start,end):
	run("AVI...", "select=["+path+"] first="+str(start)+" last="+str(end)+" convert")
	run("In")
	rename("Source")



#Results table Functions
#----------------------

def getNResults():
	return RT.getResultsTable().getCounter()


"""
	Save Results
"""
def saveResults(path):
	IJ.saveAs("Results", path);


"""
	Clears the Results table
"""
def clearResults():
	#RT.getResultsTable().reset()
	run("Clear Results", "")
	#Close the Results window
	reswin = WM.getWindow("Results")
	if reswin:	reswin.close()


"""
	Update results table
"""
def updateResults():
	rt = RT.getResultsTable()
	rt.updateResults()


"""
	Get result by column and row
"""
def getResult(col_name,row):
	rt = RT.getResultsTable()
	return rt.getValue(col_name,row)


"""
	set result by column and row
"""
def setResultRow(col_names,results):
	rt = RT.getResultsTable()
	rt.incrementCounter()
	[rt.addValue(col_name,res) for col_name, res in zip(col_names,results)]
	rt.show("Results")

def measure():
	run("Measure")


#Selection Functions
#---------------------

def watershed():
	run("Watershed")

def createMask():
	run("Create Mask")


def areatoline():
	run("Area to Line")

"""
To shrink the selection specify negative value
To enlarge the selection specify positive value
"""
def scaleSelection(pixels):
	run("Enlarge...", "enlarge="+str(pixels))


def crop():
	run("Crop")


def rotSelection(degrees):
	run("Rotate...", "angle="+str(degrees))


def makeBand(band):
	run("Make Band...", "band="+str(band));


"""
	makeEllipse(x,y,w,h)	:	Makes an ellipse selection
	makes a centered ellipse by default
"""
def makeEllipse(x,y,w,h,centered=True):
	if centered:
		x = x - w/2
		y = y - h/2
	IJ.makeOval(x,y,w,h)


"""
	makeRectangle(x,y,w,h)	:	Makes a rectangle selection
"""
def makeRectangle(x,y,w,h,centered=True):
	if centered:
		x = x - w/2
		y = y - h/2
	IJ.makeRectangle(x,y,w,h)



"""
	makeArrow(x1,y1,x2,y2)	:	Makes an arrow selection
"""
def makeArrow(x1,y1,x2,y2):
	IJ.setTool("arrow")
	imp = IJ.getImage()
	imp.setRoi(Line(x1,y1,x2,y2))

"""
	makeSpline(pt1,pt2,pt3,...)	:	Makes a spline selection
"""
def makeSpline(*points):
	macrocode = 'makeLine('
	for x,y in points:	macrocode += str(int(x)) + ", " + str(int(y)) + ", "
	macrocode = macrocode[:-2] + ');'
	#print macrocode
	IJ.runMacro(macrocode)


"""
	makeLine(x1,y1,x2,y2)	:	Makes a line selection
"""
def makeLine(x1,y1,x2,y2):
	IJ.makeLine(x1,y1,x2,y2)


"""
	makePoint(x,y)	:	Makes a point selection
"""
def makePoint(x,y):
	IJ.makePoint(x,y)


SELECTION_TYPES = {
					0 : 'rectangle',
					1 : 'oval',
					2 : 'polygon',
					3 : 'freehand',
					4 : 'traced',
					5 : 'straight line',
					6 : 'segmented line',
					7 : 'freehand line',
					8 : 'angle',
					9 : 'composite',
					10 : 'point',
					-1 : 'no selection',
				}

def selectionType(named=False):
	i = int(IJ.runMacro("return toString(selectionType());"))
	if not named:
		return i
	else:
		return SELECTION_TYPES[i]


def createSelection():
	run("Create Selection")

def selectNone():
	run("Select None")

def makePolygon(xs,ys):
	imp = IJ.getImage()
	imp.setRoi(PolygonRoi(xs,ys,len(xs),Roi.POLYGON));

def convexHull():
	run("Convex Hull")

def fitEllipse():
	run("Fit Ellipse")

def getSelectedPoint():
	return zip(*getSelectionCoordinates())[0]


#returns [Xs,Ys]
def getSelectionCoordinates():
	c = []
	if selectionType() != -1:
		c.append(IJ.getImage().getRoi().getFloatPolygon().xpoints)
		c.append(IJ.getImage().getRoi().getFloatPolygon().ypoints)
	return c

#returns [Xs,Ys]
#i.e. List of list of Xs and list of ys
def pointsFromMask(noselect=False):
	run("Points from Mask")
	XY = getSelectionCoordinates()
	if noselect:
		selectNone()
	return XY


#ROI Manager Functions
#----------------------

def roiShowAll():
	roiRun("Show All")

def roiShowAllLabels():
	roiRun("Show All with labels")


def roiSetSave(path,roisetname):
	roiRun("Save", pjoin(path, roisetname))


def roiSave(path,roiname):
	IJ.saveAs("Selection", pjoin(path,roiname))


def roiCentroid(i):
	selectNone()
	roiDeselect()
	roiSelect(i)
	points = getSelectionCoordinates()	#X,Y
	return map(mean,points)


"""
	Clears the ROI Manager
"""
def roiReset():
	if roiCount() > 0:
		roiRun("Deselect")
		roiRun("Delete")


"""
	Updates the currenty selected ROI
"""
def roiUpdate():
	roiRun("Update")


"""
	Returns the slice number of the specified ROI name
	ROI name should be original ImageJ generated name.
"""
def roiSlice(roiname):
	return RM().getSliceNumber(roiname)


"""
	Returns the name of the ROI with specified index
"""
def roiName(index):
	return RM().getName(index)


"""
	Sets the new name of the ROI
"""
def roiSetName(name):
	return RM().runCommand("Rename",name)


"""
	Delete the selected ROI
"""
def roiDelete():
	roiRun("Delete")


"""
	Split the composite ROI in to component ROIs
"""
def roiSplit():
	roiRun("Split")


"""
	Sort ROIs in the ROI Manager
"""
def roiSort():
	roiRun("Sort")


"""
	Execute ROI Manager OR (Combine) Function on ROIs
"""
def roiOR():
	roiRun("Combine")

"""
	Execute ROI Manager XOR Function on ROIs
"""
def roiXOR():
	roiRun("XOR")


"""
	Execute ROI Manager AND Function on ROIs
"""
def roiAND():
	roiRun("AND")

"""
	Measure over selected ROI
"""
def roiMeasure():
	rm = RM()
	rm.runCommand("Measure")


def roiMultiMeasure(append=True):
	if append:
		roiRun("Multi Measure append")
	else:
		roiRun("Multi Measure")


"""
	Deselect the selected ROI from the ROI Manager
"""
def roiDeselect():
	rm = RM()
	rm.runCommand("Deselect")


def roiOpen(path):
	imopen(path)
	#roiAdd()


"""
	Add the ROI to the ROI Manager
"""
def roiAdd():
	rm = RM()
	rm.runCommand("Add")


"""
	Rename the name of the selected ROI in the ROI Manager
"""
def roiRename(name):
	roiRun("Rename",name)


"""
	Run specified comm with (optional) arg on the ROI Manager
"""
def roiRun(comm,*arg):
	rm = RM()
	rm.runCommand(comm,*arg)


"""
	Select specified indices in the ROI Manager
	indices is a list of integers
"""
def roiSelectMany(indices):
	rm = RM()
	rm.setSelectedIndexes(indices)


"""
	Select all indices in the ROI Manager
"""
def roiSelectAll():
	rm = RM()
	roiRun("Select All")


"""
	Select index ROI in the ROI Manager
"""
def roiSelect(index):
	rm = RM()
	rm.select(index)


"""
	Return the count of ROis in the ROI Manager
"""
def roiCount():
	rm = RM()
	return rm.getCount()

	
def getRM():
	return RM()


def RM():
	return RoiManager.getInstance()


#Base Image/Stack Functions
#----------------------

def reset():
	print "calling RESET..."
	roiReset()
	clearResults()


def bin_skel():
	run("Skeletonize", "stack")


def bin_dilate():
	run("Dilate", "stack")


def bin_fillholes():
	run("Fill Holes")


def bin_erode():
	run("Erode")


def bin_open(mode="slice"):
	run("Open", mode)

def bin_close(mode="slice"):
	run("Close-", mode)


def setBackgroundColor(r,g,b):
	IJ.setBackgroundColor(r,g,b)


def delSlice():
	run("Delete Slice")


def addSlice():
	run("Add Slice")


def getSlice():
	return IJ.getImage().getSlice()


#1<=j<=k
#j<=k<=nSlices
def substack(j,k):
	run("Make Substack...", "  slices="+str(j)+"-"+str(k))


def concat(s1,s2):
	run("Concatenate...", "  title="+s1+" image1="+s1+" image2="+s2+" image3=[-- None --]")


"""
	Returns the number of slices in the current image.

	Note: An image has to be open in order for this function to work.
"""
def getNSlices():
	imp = IJ.getImage()
	return imp.getStackSize()

"""
	Returns the number of slices in the current image.

	Note: An image has to be open in order for this function to work.
"""
def getStackSize():
	imp = IJ.getImage()
	return imp.getStackSize()



"""
	Returns the list of statistics as:
	(area, mean, mode, min and max)

	Note: An image has to be open in order for this function to work.
"""
def getStatistics():
	imp = IJ.getImage()
	return imp.getStatistics()


"""
	Returns the list of dimensions as:
	(width, height, nChannels, nSlices, nFrames)

	Note: An image has to be open in order for this function to work.
"""
def getDimensions():
	imp = IJ.getImage()
	return imp.getDimensions()

	
"""
	Returns the pixel value
	Note: An image has to be open in order for this function to work.
"""
def getPixel(x,y):
	imp = IJ.getImage()
	v = imp.getPixel(x,y)
	return v


"""
	Duplicate the entire Image/Stack
"""
def duplicate(name):
	imp = IJ.getImage()
	run("Duplicate...", "title="+name+" duplicate range=1-"+str(imp.getNSlices()));


"""
	Duplicate a slice
"""
def dupFrame(name):
	imp = IJ.getImage()
	run("Duplicate...", "title="+name);


"""
	setForegroundColor(r,g,b)	:	Sets the foreground color
	0 <= r,g,b <= 255
"""
def setForegroundColor(r,g,b):
	IJ.setForegroundColor(r,g,b)


"""
	close()	:	Closes the current image window
"""
def close():
	IJ.runMacro("close()")


"""
	setSlice(index)	:	Sets the current slice in the stack to index
	1 <= index <= stack_size
"""
def setSlice(index):
	IJ.setSlice(index)


"""
	rename(newname)	:	Rename the current image
"""
def rename(newname):
	IJ.runMacro('rename("'+newname+'")')


"""
	selectWindow(name)	:	Select the specified window
"""
def selectWindow(name):
	IJ.runMacro('selectWindow("'+name+'")')


"""
	run(command_string)	:	Execute ImageJ "run" command string
"""
def run(*comm):
	IJ.run(*comm)




if __name__ == '__main__':
	print euclidean([1,1],[2,2])
	print filechooser()

