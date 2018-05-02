This program enables the user to digitize fish position and count the number of fish in different regions of interest in a video provided. MainProgram.py contains the main function. 

Flags available to be set in the config file:
	MANUAL - changes the behaviour of the application. If set to true the manual tracking is performed, if false automated.
	DEBUGGING - allows outputting more information during runtime for debugging purposed

Flags available to be passed in through terminal:
    	"-a" or "--min_contour_area" (type=int) - minimum area size for contours used in background subtraction
    	"-f" or "--waiting-frames" (type=int) - number of frames used to calculate background model
   	"-t" or "--threshold" (type=float) - threshold used in background subtraction average calculation

Depending on the flag MANUAL, user will be able to perform a manual or automated detection and counting of the fish. 
User first is prompt to select the video file and then has to either:
	wait for the background subtraction to automatically perform the task, or
	click on all of the fish in the frame and press 'n' to go to the next frame. 

Once finished, program outputs two files: one containing all fish coordinates and one containing the number of fish in each region

The csv files can be passed in to the GraphFrames.py file which plots the data.

All code was written by Oliwia Marek unless clearly specified.

////////////////////////////////////////////////////////
REQUIREMENTS:
OpenCV (used version 3.4.0)
Python 2.7.0
Python Standard Library
NumPy Library

////////////////////////////////////////////////////////
STRUCTURE:

MainProgram.py - contains the main function
config.py - configurations and globals
BackgroundSubtractor.py - contains the automated tracking code
FishTracker.py - contains the manual tracking code 

DataAnalysing folder contains two files used for creation of graphs:
	GraphFrames.py - takes number of files specified in globals and plot a graph of all frames in seconds. 
	GraphMaxNumber.py - plots graph of hard coded manually recorded maximum values of the fish.
ExampleVid folder contains example videos that can be used in the program. 
Testing folder containg files used for unit testing.
Outputs folder is where the program writes the output files to.
