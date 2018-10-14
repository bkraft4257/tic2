#!/usr/bin/env python3

"""

"""

import sys      
import os                                               # system functions
import shutil
import distutils

import argparse
import subprocess
import _qa_utilities as qa_util
import _utilities as util
import glob
import csv


def create_roi(inRoi, in_image_basename, inPoint, inLabelNumber=1, inRadius=3, inCoordinatesFlag=False, inVerboseFlag=False, inDebugFlag=False):

   
    from nipype.interfaces import fsl
    import glob
    import os

    if inVerboseFlag:
        print((">>>>> create_roi", in_image_basename, inRoi, inPoint, inLabelNumber, inRadius, inCoordinatesFlag, inDebugFlag))

    if inCoordinatesFlag:
        imageMathBoolean = "1"   # World / Physical coordinates
    else:
        imageMathBoolean = "0"   # Index

    # Create image filled with 0
    callCommand = ["ImageMath", "3", "step_1."+ inRoi, "m", in_image_basename, "0"]

    util.iw_subprocess( callCommand, inArgs.verbose, inArgs.debug )

    # Set Desired Pixel to 1
    callCommand = ["ImageMath", "3", "step_2."+inRoi, "SetOrGetPixel",  "step_1."+inRoi, "1", str(inPoint[0]), 
                            str(inPoint[1]), str(inPoint[2]), imageMathBoolean ];

    util.iw_subprocess( callCommand, inArgs.verbose, inArgs.debug )

    if inRadius>0:

        if inDebugFlag:
            print("inRadius>0")

        pipe = subprocess.call(["ImageMath", "3", "step_3."+inRoi, "MD",  "step_2."+inRoi, str(inRadius) ])
        pipe = subprocess.call(["ImageMath", "3", "step_4."+inRoi, "m",   "step_3."+inRoi,  str(inLabelNumber) ])

        pipe = subprocess.call(["ImageMath", "3", "step_5."+inRoi, "Neg", "step_2."+inRoi ])
        pipe = subprocess.call(["ImageMath", "3", "step_6."+inRoi, "m",   "step_4."+inRoi,  "step_5."+inRoi ])

        if os.path.isfile(inRoi): 
            print("Adding Spherical ROIs")
            pipe = subprocess.call(["ImageMath", "3",      inRoi, "+",  inRoi,  "step_6."+inRoi ])
        else:
            shutil.copy("step_6."+inRoi, inRoi)

    else:
        
        callCommand = ["ImageMath", "3", "step_3."+inRoi, "m",   "step_2."+inRoi,  str(inLabelNumber) ]
        util.iw_subprocess( callCommand, inArgs.verbose, inArgs.debug )

        if os.path.isfile(inRoi): 
            print("Adding Point ROIs")
            pipe = subprocess.call(["ImageMath", "3",      inRoi, "+",  inRoi,  "step_3."+inRoi ])
        else:
            shutil.copy("step_3."+inRoi, inRoi)


    if not inDebugFlag:
        globSearch = str("step_[0-9]."+ inRoi)
        list(map(os.remove, glob.glob(globSearch)))



#
# Main Function
#
if __name__ == "__main__":

     ## Parsing Arguments
     #

     usage = "usage: %prog [options] arg1 arg2"

     class MyParser(argparse.ArgumentParser):
         def error(self, message):
             sys.stderr.write('error: %s\n' % message)
             self.print_help()
             sys.exit(2)

     parser = argparse.ArgumentParser(prog='iwCreateRoi')
     parser.add_argument("--image",             help="Image", required=True)
     parser.add_argument("--label",             help="Label number", type=int, default=1000)
     parser.add_argument("--radius",            help="Radius of ROI", type=int, default=5)
     parser.add_argument("--roi_prefix",        help="ROI prefix added to --image", default="roi.")
     parser.add_argument("--roi_add",           help="Display Results", action="store_true", default=False )
     parser.add_argument("--roi_type",          help="ROI Type (sphere, point)", choices=['sphere', 'point'], default='sphere' )
     parser.add_argument("--merge",             help="Merge ROIs", action="store_true", default=True)
     parser.add_argument("--collapse",          help="Collapse ROIs", action="store_true", default=True)
     parser.add_argument("-d","--display",      help="Display Results", action="store_true", default=False )
     parser.add_argument("-v","--verbose",      help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",             help="Debug flag",      action="store_true", default=False )
     parser.add_argument("--clean",             help="Clean directory by deleting intermediate files",      action="store_true", default=False )
     parser.add_argument("--qi",                help="QA inputs",      action="store_true", default=False )
     parser.add_argument("--qo",                help="QA outputs",      action="store_true", default=False )
     parser.add_argument("-r", "--run",         help="Run processing pipeline",      action="store_true", default=False )
     parser.add_argument("--world",             help="MRI Viewer CTF Index coordinates", action="store_true", default=True)
     parser.add_argument("--scale",             help="Scale coordinates", type=float,  default=1.0 )


#     group = parser.add_mutually_exclusive_group(required=True)
     parser.add_argument("--csv",            help="CSV file containing coordinates", default = None)
     parser.add_argument("--point",          help="Input a single point", nargs=3, type=float, default = None)

     inArgs = parser.parse_args()

     input_files = [[ inArgs.image, ':colormap=grayscale']]

#     output_files = [[ inArgs.image, ':colormap=grayscale'],
#                     [ roiImage, ':colormap=jet']]

     if inArgs.roi_type == 'sphere':
         radius=inArgs.radius
     else:
         radius=0


     if inArgs.debug:
         print("inArgs.image       = " +  str(inArgs.image))
         print("inArgs.label       = " +  str(inArgs.label))
         print("inArgs.radius      = " +  str(inArgs.radius))
         print("ROI type           = " +  inArgs.roi_type)
         print("ROI radius         = " +  str(radius))
         print()
         print("inArgs.display     = " +  str(inArgs.display))
         print("inArgs.debug       = " +  str(inArgs.debug))
         print("inArgs.verbose     = " +  str(inArgs.verbose))
         print()
#         print "ROI image          = " +  roiImage
         print()
         
     if  inArgs.qi:
         qa_util.qa_input_files( input_files, inArgs.verbose, False )

     if  inArgs.run:


         if not inArgs.csv == None:

             # Create ROIs from file (x,y,z,t,label, radius )
             try:

                 roi_filenames = []

                 with open(inArgs.csv, 'r') as csvfile:

                     next(csvfile, None)  # Skip header

                     csvPoints = csv.reader(csvfile, delimiter=',', quotechar='|')

                     print(csvPoints)

                     for iiPoint in csvPoints:
             
                         print(iiPoint)

                         point = list(map(float, iiPoint[0:3]))

                         print(point)

                         for ii in [0, 1, 2]:
                             point[ii] = inArgs.scale * point[ii]
                         
                         label = int(iiPoint[4])

                         if inArgs.debug:
                             print(point, label, radius)
                             
                         roiImage= str(label).zfill(6) + "." + inArgs.roi_prefix + os.path.basename(inArgs.image)

                         roi_filenames = roi_filenames + [ roiImage ] 

                         if not inArgs.roi_add and os.path.isfile(roiImage):
                             os.remove(roiImage)             

                         create_roi(roiImage, inArgs.image, point, label, radius, 
                                    inArgs.world, inArgs.verbose, inArgs.debug)

                 
                     if inArgs.merge or inArgs.collapse:

                         roi_4d = inArgs.roi_prefix + '4d.'+ os.path.basename(inArgs.image)

                         util.iw_subprocess( ['fslmerge', '-t', roi_4d ] 
                                                    + roi_filenames, 
                                                    inArgs.verbose, inArgs.debug)

                     if inArgs.collapse:

                         util.iw_subprocess( ['fslmaths', roi_4d, 
                                                     '-Tmean', '-mul', str(len(roi_filenames)), 
                                                     inArgs.roi_prefix + os.path.basename(inArgs.image) ],
                                                    inArgs.verbose, inArgs.debug)

                         util.iw_subprocess( ['fslmaths', roi_4d, '-bin',
                                                      '-Tmean', '-mul', str(len(roi_filenames)), 
                                                     '-thr', 1,
                                                     'overlap.' + inArgs.roi_prefix + os.path.basename(inArgs.image) ],
                                                    inArgs.verbose, inArgs.debug)


                     if inArgs.clean and (inArgs.merge or inArgs.collapse):

                         for ii in roi_filenames:
                             os.remove( ii )

             except IOError:
                 print("Error: can\'t find file or read data")
         
         # Create ROIs from single point

         elif not inArgs.point == None:

             point = inArgs.point

             roiImage= str(0).zfill(6) + "." + inArgs.roi_prefix + inArgs.image

             create_roi(roiImage, inArgs.image, point, inArgs.label, 
                        inArgs.radius, inArgs.world, inArgs.debug)

         else:
             print("inArgs.csv or inArgs.point not set properly")


#     if  inArgs.qo:

#         if inArgs.debug:
#             print output_files

#         qa_util.freeview( output_files, inArgs.display, inArgs.verbose ) 


