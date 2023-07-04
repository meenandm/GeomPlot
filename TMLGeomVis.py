import uproot
#import ROOT
import vtk
import pandas as pd
import numpy as np
import os
import random
import sys
import argparse


def setupArgparse():
  parser = argparse.ArgumentParser(description="Running Operators For This Program", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--objDetectorF", help="The Object Folder For The Detector", required=False, nargs=1)
  parser.add_argument("--objDetector", help="The Object File For The Detector", required=False, nargs=1)
  parser.add_argument("--csvDetector", help="The CSV File For The Detector", required=False, nargs=1)
  parser.add_argument("--csvEventF", help="The CSV Folder For The Event(s) Data", required=False, nargs=1)
  parser.add_argument("--csvEvent", help="The CSV File For The Event(s) Data", required=False,  nargs='*')
  
  return (parser)


def objDetectorFLoader(config, ren, renWin):
  
  # Get Detector OBJs from argument list
  # It should be the first argument givn after the python programE
  detectorOBJ = config["objDetectorF"][0]
  
  # -------------------------
  # Detector from OBJ Folder
  # -------------------------
  for file in os.listdir(detectorOBJ):
    if file.endswith(".obj"):
      if (file.__contains__("BeamPipe") or file.__contains__("Strips")):
        objectDataPath  = os.path.join(detectorOBJ, file)
        materialDataName = os.path.splitext(objectDataPath)[0]+".mtl"
        materialDataPath = os.path.join(detectorOBJ, materialDataName)
        
        importer = vtk.vtkOBJImporter()
        importer.SetFileName(objectDataPath)
        importer.SetFileNameMTL(materialDataPath)

        importer.SetRenderWindow(renWin)
        importer.Update()

  #Get all current actors in scene
  actors = ren.GetActors()
  actors.InitTraversal()
  
  #Set their opacity and activate backface culling
  for a in range (actors.GetNumberOfItems()):
    actor = actors.GetNextActor()
    actor.GetProperty().SetOpacity(0.05)
    actor.GetProperty().SetBackfaceCulling(True)
      
  print("OBJ DETECTOR FOLDER LOADED")
  
  return (0)


def csvDetectorLoader(config, ren, renWin):
  
  detectorCSV = config["csvDetector"][0]
  
  # ------------------
  # Detector from CSV
  # ------------------
  #Read the data csv and add it to a numpy array
  dataCoordsAll = pd.read_csv(detectorCSV)
  
  dataCoords = dataCoordsAll.loc[:, ["cx", "cy", "cz", "volume_id"]].to_numpy()
  
  dataTransform = dataCoordsAll.loc[:, ['rot_xu', 'rot_xv', 'rot_xw', 'rot_yu', 'rot_yv', 'rot_yw', 'rot_zu', 'rot_zv', 'rot_zw']].to_numpy()
  
  for line in range(len(dataCoords)):
        point = dataCoords[line]
        if (point[3] == 22):
          dataTransformList = dataTransform[line].tolist()
          dataTransformList.insert(3, 0)
          dataTransformList.insert(7, 0)
          dataTransformList.insert(11, 0)
          dataTransformList.extend([0,0,0,1])
          
          #Create disk
          disk = vtk.vtkDiskSource()
          disk.SetInnerRadius(0)
          
          #Craete scale tranform
          scale = vtk.vtkTransform()
          scale.Scale(30, 30, 30)
          
          #Create Transform and set its matrix        
          transform = vtk.vtkTransform()
          transform.SetMatrix(dataTransformList)
          transform.Translate(point[0:3])
          transform.Concatenate(scale)
            
          transformFilter = vtk.vtkTransformPolyDataFilter()
          transformFilter.SetInputConnection(disk.GetOutputPort())
          transformFilter.SetTransform(transform)
          transformFilter.Update()
            
          diskMapper = vtk.vtkPolyDataMapper()
          diskMapper.SetInputConnection(transformFilter.GetOutputPort())
            
          diskActor = vtk.vtkActor()
          diskActor.SetMapper(diskMapper)
          diskActor.GetProperty().SetColor(1,0,0)
          ren.AddActor(diskActor)
          
        if (point[3] == 23):
          dataTransformList = dataTransform[line].tolist()
          dataTransformList.insert(3, 0)
          dataTransformList.insert(7, 0)
          dataTransformList.insert(11, 0)
          dataTransformList.extend([0,0,0,1])
          
          #Create disk
          disk = vtk.vtkDiskSource()
          disk.SetInnerRadius(0)
          
          #Craete scale tranform
          scale = vtk.vtkTransform()
          scale.Scale(30, 30, 30)
          
          #Create Transform and set its matrix        
          transform = vtk.vtkTransform()
          transform.SetMatrix(dataTransformList)
          transform.Translate(point[0:3])
          transform.Concatenate(scale)
            
          transformFilter = vtk.vtkTransformPolyDataFilter()
          transformFilter.SetInputConnection(disk.GetOutputPort())
          transformFilter.SetTransform(transform)
          transformFilter.Update()
            
          diskMapper = vtk.vtkPolyDataMapper()
          diskMapper.SetInputConnection(transformFilter.GetOutputPort())
            
          diskActor = vtk.vtkActor()
          diskActor.SetMapper(diskMapper)
          diskActor.GetProperty().SetColor(0,1,0)
          ren.AddActor(diskActor)
          
        if (point[3] == 24):
          dataTransformList = dataTransform[line].tolist()
          dataTransformList.insert(3, 0)
          dataTransformList.insert(7, 0)
          dataTransformList.insert(11, 0)
          dataTransformList.extend([0,0,0,1])
          
          #Create disk
          disk = vtk.vtkDiskSource()
          disk.SetInnerRadius(0)
          
          #Craete scale tranform
          scale = vtk.vtkTransform()
          scale.Scale(30, 30, 30)
          
          #Create Transform and set its matrix        
          transform = vtk.vtkTransform()
          transform.SetMatrix(dataTransformList)
          transform.Translate(point[0:3])
          transform.Concatenate(scale)
            
          transformFilter = vtk.vtkTransformPolyDataFilter()
          transformFilter.SetInputConnection(disk.GetOutputPort())
          transformFilter.SetTransform(transform)
          transformFilter.Update()
            
          diskMapper = vtk.vtkPolyDataMapper()
          diskMapper.SetInputConnection(transformFilter.GetOutputPort())
            
          diskActor = vtk.vtkActor()
          diskActor.SetMapper(diskMapper)
          diskActor.GetProperty().SetColor(0,0,1)
          ren.AddActor(diskActor)
          
  print("CSV DETECTOR FILE LOADED")
  
  return (0)


def csvEventLoader(csvFile, ren, renWin):
  
  # ----------------------
  # TRACCC DATA from CSV
  # ----------------------
  try:
    tracccCSV_DF = pd.read_csv(csvFile)
    tracccCSVList = tracccCSV_DF.loc[:, ["cx", "cy", "cz", "geometry_id"]].to_numpy()
    
  except:
    tracccCSV_DF = pd.read_csv(csvFile)
    tracccCSVList = tracccCSV_DF.loc[:, ["tx", "ty", "tz", "geometry_id"]].to_numpy()

  for line in range(len(tracccCSVList)):
      coord = tracccCSVList[line]
        
      #Create Sphere actor
      sphere = vtk.vtkSphereSource()
      sphere.SetRadius(10)
      sphere.SetCenter(coord[0], coord[1], coord[2])
      sphere.SetThetaResolution(4)
      sphere.SetPhiResolution(4)
      sphereMapper = vtk.vtkPolyDataMapper()
      sphereMapper.SetInputConnection(sphere.GetOutputPort())
      
      sphereActor = vtk.vtkActor()
      sphereActor.SetMapper(sphereMapper)
      sphereActor.GetProperty().SetColor(1, 0, 0)
            
      ren.AddActor(sphereActor)
      
  print("CSV EVENT FILE LOADED")
  
  return (0)

  
def csvEventFLoader(csvFolder, ren, renWin):
  
  # ----------------------------
  # TRACCC DATA from CSV FOLDER
  # ----------------------------
  for file in os.listdir(csvFolder):
    if file.endswith("cells.csv"):
      tracccCSV_DF = pd.read_csv(os.path.join(csvFolder, file))
      tracccCSVList = tracccCSV_DF.to_numpy()

      for line in range(len(tracccCSVList)):
          coord = tracccCSVList[line]
            
          #Create Sphere actor
          sphere = vtk.vtkSphereSource()
          sphere.SetRadius(10)
          sphere.SetCenter(coord[0], coord[1], coord[2])
          sphereMapper = vtk.vtkPolyDataMapper()
          sphereMapper.SetInputConnection(sphere.GetOutputPort())
          
          sphereActor = vtk.vtkActor()
          sphereActor.SetMapper(sphereMapper)
          sphereActor.GetProperty().SetColor(1, 0, 0)
                
          ren.AddActor(sphereActor)
      
  print("CSV EVENT FOLDER LOADED")
  
  return (0)
 
      
      
def run(args, ren, renWin):
 
    tracccCSV = args[3]
    tracccSeed = args[4]

    # ----------------------
    # TRACCC DATA from CSVs
    # ----------------------
    tracccCSV_DF = pd.read_csv(tracccCSV)
    tracccCSVList = tracccCSV_DF.to_numpy()

    for line in range(len(tracccCSVList)):
        coord = tracccCSVList[line]
        
        #Create Sphere actor
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(10)
        sphere.SetCenter(coord[0], coord[1], coord[2])

        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())
        
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)
        sphereActor.GetProperty().SetColor(1, 0, 0)
              
        ren.AddActor(sphereActor)
        
    tracccSeed_DF = pd.read_csv(tracccSeed)
    tracccCSVSeed = tracccSeed_DF.to_numpy()
    
    
    for line in range(len(tracccCSVSeed)):
        coord = tracccCSVSeed[line]
        
        #Create Sphere actor
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(10)
        sphere.SetCenter(coord[2], coord[3], coord[4])

        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())
        
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)
        sphereActor.GetProperty().SetColor(0, 0, 1)
        sphereActor.GetProperty().SetOpacity(0.5)
              
        ren.AddActor(sphereActor)
  
    #Get all current actors in scene
    actors = ren.GetActors()
    actors.InitTraversal()
    print("There are " , actors.GetNumberOfItems() , " actors")
    
    return (0)


def main(arg):
  
  # ----------------
  # ARGPARSER SETUP
  # ----------------
  parser = setupArgparse()
  args = parser.parse_args()
  config = vars(args)
  print (config)
  
  
  # -------------------
  # VTK RENDERER SETUP
  # -------------------
  # Setup rendering
  colorBackground = [0.0, 0.0, 0.0]
  ren = vtk.vtkRenderer()
  ren.SetBackground(colorBackground)
  #Set render window input
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  # Create a renderwindowinteractor
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)
  
  
  # -----------------------------------
  # LOAD FILES/FOLDERS BASED ON INPUTS
  # -----------------------------------
  # LOAD ARGUMENTS WITH ONLY 1 INSTANCE
  if (config["objDetectorF"] != None):
    objDetectorFLoader( config, ren, renWin)
  if (config["csvDetector"] != None):
    csvDetectorLoader( config, ren, renWin)
  
  #LOAD ARGUMENTS WITH MULTIPLE INSTANCES
  if (config["csvEventF"] != None):
    for folder_index in range (len(config["csvEventF"])):
      csvEventF = config["csvEventF"][folder_index]
      csvEventFLoader (csvEventF, ren, renWin)
      
  if (config["csvEvent"] != None):
    for file_index in range (len(config["csvEvent"])):
      csvEvent = config["csvEvent"][file_index]
      csvEventLoader (csvEvent, ren, renWin)

  
  #run( args, ren, renWin )


  # -----------------
  # RUN VTK RENDERER
  # -----------------
  # Enable user interface interactor
  print("Starting Renderer")
  iren.Initialize()
  renWin.Render()
  iren.Start()

if __name__ == "__main__":
    main(sys.argv)
    