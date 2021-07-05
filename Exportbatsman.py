import maya.cmds as cmds
import maya.mel as mel
#bone = cmds.ls("Bone*", type = 'joint')
#cmds.delete( bone)

#nub = cmds.ls("*Nub",type='joint')
#cmds.delete(nub)




def ExportFiles():
    selObjects = cmds.ls(sl=True)
    cmds.select(cl=True)
    SAVE_PATH = cmds.fileDialog2(cap = "Set Export Directory", okCaption="Select",dialogStyle=3,fileMode=3)
    currentFile = cmds.file(q=True,sceneName=True)
    root_bone = cmds.ls("Bip001")
    cmds.select(root_bone[0],hierarchy=True)
    hierarchy = cmds.ls(sl=True)
    cmds.select(cl=True)
    
    for item in selObjects:
        cmds.select(item,add=True)
        cmds.select(hierarchy,add=True)
        saveFileName = SAVE_PATH[0]+"/"+item+".FBX"
        ExportFBX(saveFileName)
        
        
        
def RemoveMeshes(meshName):
    geometry = cmds.ls(geometry=True)
    transforms = cmds.listRelatives(geometry, p=True, path=True)
    if meshName in transforms:
        transforms.remove(meshName)
        cmds.delete(transforms)
        
    
def ExportFBX(filename):
    mel.eval('FBXExport -f "' + filename + '" -s;')
    cmds.select(cl=True)
ExportFiles()

  