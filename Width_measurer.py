# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 01:49:33 2022

@author: BelmontLab
"""

import numpy as np
from scipy import spatial
import time
import arcpy
import os

arcpy.env.overwriteOutput=True

#%%-------------User Inputs----------------------------------------

#Set Workspace
arcpy.env.workspace = out_folder_path = r'C:\Users\BelmontLab\Documents\Alec\Research\ErrorAnalysis\Valley Bottom Width'

# Shapefile with Channel and/or Valley Bottom Segments
Widths=r'C:\Users\BelmontLab\Documents\Alec\Research\Analysis\ErrorAnalysis\Valley Bottom Width\vb_error_sj.shp'

# get unique feature IDs from shapefile and add to list for iteration
ilist=[]
with arcpy.da.SearchCursor(in_table=Widths, field_names=['Snippet']) as searcher:
    for row in searcher:
        i=row[0]
        ilist.append(i)

# Split features in shapefile into individual shapefiles
arcpy.analysis.SplitByAttributes(Widths, out_folder_path, 'Snippet')

# Iterate through each feature
#
for i in ilist:
    print(i)
    #input polygon
    infcpol=fr'C:\Users\BelmontLab\Documents\Alec\Research\Analysis\ErrorAnalysis\Valley Bottom Width\{i}.shp'  #Valley Bottom
    centerline=fr'C:\Users\BelmontLab\Documents\Alec\Research\Analysis\ErrorAnalysis\Valley Bottom Width\ce.gdb\ce{i}' #Centerline
    dis=fr'C:\Users\BelmontLab\Documents\Alec\Research\Analysis\ErrorAnalysis\Valley Bottom Width\dis{i}.shp' #Dissolved feature 
    
    #Dissolve Feature
    arcpy.management.Dissolve(infcpol, dis)
    #Get Area in meters of feature
    with arcpy.da.SearchCursor(in_table=dis, field_names=['SHAPE@AREA']) as searcher:
        for row in searcher:
            area=row[0]
    print(area)
    
    #Create Centerline
    # GDB for Centerlines
    arcpy.CreateFileGDB_management(out_folder_path, "ce.gdb") 
    ##SNIPPET 19 will not correctly produce a centerline
    arcpy.topographic.PolygonToCenterline(dis, centerline, None)
    #Get Feature Length
    with arcpy.da.SearchCursor(in_table=centerline, field_names=['SHAPE@LENGTH']) as searcher:
        for row in searcher:
            length=row[0]
    print(length)
    
    # Calculate Width
    width=area/length
    print(width)
    where_clause=f"\"Snippet\"='{i}'"
    print(where_clause)
    #Add Width Measurement to Original Shapefile
    with arcpy.da.UpdateCursor(in_table=Widths, field_names=['VB_meas'], where_clause=where_clause) as inserter:
        for row in inserter:
            row[0]=width
            inserter.updateRow(row)
            
