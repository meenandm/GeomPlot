import uproot
#import ROOT
import vtk
import pandas as pd
import os
import random
import sys

def run(args):
    
    colorBackground = [0.0, 0.0, 0.0]
    objFolder = args[1]
    hitsFile = args[2]
    data = []
    
    # Create a rendering window and 2 renderers
    ren = vtk.vtkRenderer()
    ren.SetBackground(colorBackground)
    
    #Set render window inputs
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    
    # Create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    #ObjImporter
    for file in os.listdir(objFolder):
      if file.endswith(".obj"):
        if not(file.__contains__("Endcap")):
        #if (file.__contains__("Strips")):
          objectDataPath  = os.path.join(args[1], file)
          materialDataName = os.path.splitext(objectDataPath)[0]+".mtl"
          materialDataPath = os.path.join(args[1], materialDataName)
          
          importer = vtk.vtkOBJImporter()
          importer.SetFileName(objectDataPath)
          importer.SetFileNameMTL(materialDataPath)

          importer.SetRenderWindow(renWin)
          importer.Update()

    #Get all current actors in scene
    actors = ren.GetActors()
    actors.InitTraversal()
    print("There are " , actors.GetNumberOfItems() , " actors")
    
    #Set their opacity and add glow
    for a in range (actors.GetNumberOfItems()):
      actor = actors.GetNextActor()
      actor.GetProperty().SetOpacity(0.1)
      actor.GetProperty().SetBackfaceCulling(True)

    
    #ObjReader
    for file in os.listdir(objFolder):
      if file.endswith(".obj"):
        if not(file.__contains__("Endcap")):
        #if (file.__contains__("Strips")):
          objectDataPath  = os.path.join(args[1], file)
          reader = vtk.vtkOBJReader()
          reader.SetFileName(objectDataPath)
          reader.Update()
          
          scaleTransform = vtk.vtkTransform()
          scaleTransform.Scale(1.2,1.2,1.2)
          
          scaleFilter = vtk.vtkTransformPolyDataFilter()
          scaleFilter.SetInputConnection(reader.GetOutputPort())
          scaleFilter.SetTransform(scaleTransform)
          scaleFilter.Update()
          
          mapper = vtk.vtkPolyDataMapper()
          mapper.SetInputConnection(scaleFilter.GetOutputPort())
          
          actor = vtk.vtkActor()
          actor.SetMapper(mapper)
          actor.GetProperty().SetColor(0,0,0)
          actor.GetProperty().SetOpacity(0.5)
          actor.GetProperty().SetBackfaceCulling(True)
          
          
          ren.AddActor(actor)

    
    #Get all current actors in scene
    actors = ren.GetActors()
    actors.InitTraversal()
    print("There are " , actors.GetNumberOfItems() , " actors")   
    
    #Read the data csv and add it to a numpy array
    data = pd.read_csv(hitsFile, usecols = ['evt_ID','m_x', 'm_y', 'm_z']).to_numpy()
    currentEvent = 0
    currentRGB = [1,1,1]
    
    for x in range(500):
          point = data[x]
          if (point[0] != currentEvent):
            currentRGB[0] = random.uniform(0,1)
            currentRGB[1] = random.uniform(0,1)
            currentRGB[2] = random.uniform(0,1)
            currentEvent = point[0]
          sphere = vtk.vtkSphereSource()
          sphere.SetCenter(point[1], point[2], point[3])
          sphere.SetRadius(20)
          
          sphereMapper = vtk.vtkPolyDataMapper()
          sphereMapper.SetInputConnection(sphere.GetOutputPort())
          
          sphereActor = vtk.vtkActor()
          sphereActor.SetMapper(sphereMapper)
          sphereActor.GetProperty().SetColor(currentRGB[0], currentRGB[1], currentRGB[2])
          ren.AddActor(sphereActor) 
    
       
    #Create vtkPoints and id set
    dataID = 0
    dataPoints = vtk.vtkPoints()
    dataPoints.SetNumberOfPoints(len(data))
    for point in data:
      dataPoints.InsertPoint(dataID, point[0], point[1], point[2])
      dataID = dataID + 1
    
    #PolyData
    dataPoly = vtk.vtkPolyData()
    dataPoly.SetPoints(dataPoints)
    
    dataPolyMapper = vtk.vtkPolyDataMapper()
    dataPolyActor = vtk.vtkActor()
    
    dataPolyMapper.SetInputData(dataPoly)
    dataPolyActor.SetMapper(dataPolyMapper)
    
    ren.AddActor(dataPolyActor)
    
    # Enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()


def main(args):
  # Load the file
  if len( args ) != 3:
    print( "Please provide detector geometry and data folder as command line arguments" )
    exit()
  
  else:
    run( args )


if __name__ == "__main__":
    main(sys.argv)
    