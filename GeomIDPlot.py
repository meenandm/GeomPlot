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
    
    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    ren.SetBackground(colorBackground)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    
    
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
    
    #Set them as wireframes
    for a in range (actors.GetNumberOfItems()):
      actors.GetItemAsObject(a).GetProperty().SetOpacity(0.05)
    
    #Read the data csv and add it to a numpy array
    data = pd.read_csv(hitsFile, usecols = ['evt_ID','m_x', 'm_y', 'm_z']).to_numpy()
    currentEvent = 0
    currentRGB = [1,0,0]
    
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
          print(point[0], point[1], point[2], point[3])
          
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
      
    print(dataPoints)
    
    #PolyData
    dataPoly = vtk.vtkPolyData()
    dataPoly.SetPoints(dataPoints)
    
    dataPolyMapper = vtk.vtkPolyDataMapper()
    dataPolyActor = vtk.vtkActor()
    
    dataPolyMapper.SetInputData(dataPoly)
    dataPolyActor.SetMapper(dataPolyMapper)
    
    ren.AddActor(dataPolyActor)
    
    
    # Create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
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
    