import maya.cmds as cmds
import maya.mel as mel
searchToken="FBXASC032"
root_Bones = ["Bip001","Bip_bowler"]


def RemoveUnwantedBones():
    try:
        bone = cmds.ls("Bone*", type = 'joint')
        cmds.delete( bone)
        nub = cmds.ls("*Nub",type='joint')
        cmds.delete(nub)
        footSteps = cmds.ls("Footsteps",type ='joint')
        cmds.delete(footSteps)
    except:
        print ("Bones Not Found")

def RemoveDisplayLayers():
    displayLayers = cmds.ls(type = 'displayLayer')
    for layer in displayLayers:
        if layer != 'defaultLayer':
            cmds.delete(layer)

def clearKeyFrames():
    root = getSelectedHierarchyRoot()
    cmds.select(root,hierarchy=True)
    mySel = cmds.ls(sl=True)
    for sel in mySel:
        cmds.select(sel)
        cmds.cutKey(sel, s=True)

def getSelectedHierarchyRoot():
    selectedJointName = cmds.ls("Bip*", type='joint')
    parentList = cmds.listRelatives(selectedJointName, ap=True, f=True)[0].split('|') if selectedJointName else []
    jointList = [p for p in parentList if p and cmds.nodeType(p) == 'joint']
    rootJoint = jointList[0] if jointList else None
    return rootJoint


def addFBXASCII ():
    root = getSelectedHierarchyRoot()
    prefix = cmds.joint(root,query=True,name=True)
    cmds.select(root,hierarchy=True)
    skeleton = cmds.ls(sl=True,type='joint')

    for bone in skeleton:
        boneName = cmds.joint(bone,q=True,name=True)
        if prefix in boneName:
            tempName = boneName.replace(prefix,"")
            suffix = tempName.replace("_",searchToken)
            newName = prefix+suffix
            cmds.rename(bone,newName)

def cleanupJointNames (self, searchToken, replaceToken):
    selectedJoint = cmds.ls(sl=True, type="joint")
    if len(selectedJoint) != 1:
        cmds.confirmDialog( title='Cleanup Joints', message='Please Select the Skeleton Root Joint')
        return
    cmds.select(selectedJoint, hierarchy=True)  
    #cmds.select(selected_joint, hierarchy=True)
    joint_hierarchy = cmds.ls(sl=True, type="joint")
    if len(joint_hierarchy) > 0:
        for _joint in joint_hierarchy:
            if searchToken in _joint:
                newName = _joint.replace(searchToken,replaceToken)
                cmds.rename(_joint, newName)
        cmds.select( clear=True )
        print ("Joint names are fixed")
    else:
        print ("Please select the Skeleton")
        
        
        
def ExportFiles(savePath,selObjects):
    rootJnt = getSelectedHierarchyRoot()
    cmds.select(rootJnt,hierarchy=True)
    jntHierarchy = cmds.ls(sl=True)
    for item in selObjects:
        cmds.select(item,add=True)
        cmds.select(jntHierarchy,add=True)
        saveFileName = savePath +"/"+item+".FBX"
        ExportFBX(saveFileName)
        
def ExportFBX(filename):
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExportSkins -v true;')
    mel.eval('FBXExport -f "' + filename + '" -s;')
    cmds.select(cl=True)

def Main():
    # SELECT OBJECTS FOR EXPORT
    selObjects = cmds.ls(sl=True)
    if len(selObjects) < 1 :
        cmds.confirmDialog( title='Select Models', message='Please Select Objects For Export')
        return
        
    cmds.select(cl=True)
    SAVE_PATH = cmds.fileDialog2(cap = "Set Export Directory", okCaption="Select",dialogStyle=3,fileMode=2)
    
    # REMOVE DISPLAY LAYERS
    RemoveDisplayLayers()

    #REMOVE UNWANTED BONES
    RemoveUnwantedBones()

    # CLEAR KEYFRAMES
    clearKeyFrames()

    #RENAME JOINTS WITH ASCII
    addFBXASCII()

    #EXPORT FILES
    ExportFiles(SAVE_PATH[0],selObjects)

Main()