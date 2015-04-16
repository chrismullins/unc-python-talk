# - Introduction: Image processing in the 3D Slicer environment with python
# - Why give this talk?
# - Explain what Slicer is.
# - Built on top of VTK (visualization), ITK (medical image processing)
# - SimpleITK provides easy access to powerful processing tools in ITK
# - Explain segmentation

# Download MRHead
nImage = sitkUtils.PullFromSlicer('MRHead')
n = getNode('MRHead')

# Mark some fiducials
f = getNode('F')
ijkfids = GetIJKCoordsFromFiducial(f, n)
# These should be ints, also don't need the extra ones
ijkcoords = [[int(i) for i in j[0:3]] for j in ijkfids]
# Do the segmentation
imgWhiteMatter = sitk.ConnectedThreshold(image1=nImage, seedList=ijkcoords, lower=80, upper=100, replaceValue=1)
# Push it back to slicer
sitkUtils.PushLabel(imgWhiteMatter, 'whiteMatter')
# Not bad eh?

# Download CTChest
nImage = sitkUtils.PullFromSlicer('CTChest')
n = getNode('CTChest')
# Mark two fiducials
g = getNode('G')
ijkfids = GetIJKCoordsFromFiducial(g, n)
ijkcoords = [[int(i) for i in j[0:3]] for j in ijkfids]
lungs = sitk.ConfidenceConnected(nImage, ijkcoords)
sitkUtils.PushLabel(lungs, 'lungs')





################################################################################
Convenience functions
################################################################################

def GetIJKCoordsFromFiducial(fnode, volnode):
  numfids = fnode.GetNumberOfFiducials()
  ijkfids = []
  rasfids = []
  for i in range(numfids):
    ras = [0,0,0]
    fnode.GetNthFiducialPosition(i, ras)
    rasfids.append(ras)
  rasToIJK = vtk.vtkMatrix4x4()
  volnode.GetRASToIJKMatrix(rasToIJK)
  for i in range(numfids):
    rasc = rasfids[i]
    rasc.append(1)
    ijkc = rasToIJK.MultiplyPoint(rasc)
    ijkfids.append(ijkc)
  return ijkfids