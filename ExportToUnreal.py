import maya.cmds as cmds
import maya.mel as mel
import os,sys

class TestUI(object):
    
    WINDOW_NAME = "czTestUi"
    WINDOW_HEIGHT=200
    WINDOW_WIDTH=55
    FORM_OFFSET = 2
    
    @classmethod
    def display(cls):
        cls.delete_window()
        
        main_window = cmds.window(cls.WINDOW_NAME, title=cls.WINDOW_NAME, widthHeight=(cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT), rtf=True)        
        main_layout = cmds.columnLayout( adjustableColumn=True,parent=main_window,columnWidth=50,rowSpacing=25)
        
        prepare_fbx_layout = cmds.frameLayout( label=' Prepare Model for Export',collapsable=True,parent=main_layout)
        cmds.columnLayout( adjustableColumn=True,parent=prepare_fbx_layout,columnWidth=50)
        cmds.button( label='Prepare File',w=220,command=lambda *_:PrepareFile())
        cmds.columnLayout( adjustableColumn=True,parent=prepare_fbx_layout,columnWidth=50)
        cmds.button( label='Remove Nodes',w=220,command=lambda *_:removeJoints())
        
        export_fbx_layour = cmds.frameLayout( label=' FBX Mesh Export',collapsable=True,parent=main_layout)
        cmds.button( label='Export Selected Static Mesh',w=220,command='')
        cmds.button( label='Export Selected Skinned Mesh',w=220,command='')
        cmds.button( label='Export  Character Mesh',w=220,command='')
        cmds.button( label='Export  Bicycle Mesh',w=220,command='')
    
        cmds.showWindow(main_window)
    
    
    @classmethod
    def delete_window(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)


def ExportStaticMeshes():
    pass

def ExportSkeletalMeshes():
    pass

def ExportSelectedMeshes():
    pass

def CreateExportSets():
    pass

def BakeHumanIK():
    char = getCurrentCharacter()
    bakeAnim(char)
   
    
def getCurrentCharacter():
    char = mel.eval('hikGetCurrentCharacter()')
    return char
    
def setCurrentCharacter(char):
	mel.eval('hikSetCurrentCharacter("'+char+'")')
	mel.eval('hikUpdateCharacterList()')
	mel.eval('hikSetCurrentSourceFromCharacter("'+char+'")')
	mel.eval('hikUpdateSourceList()')

def isCharacterDefinition(char):
	# Check Node Exists
	if not cmds.objExists(char): return False
	
	# Check Node Type
	if cmds.objectType(char) != 'HIKCharacterNode': return False
	
	# Return Result
	return True

def getCharacterNodes(char):
	# Check Node
	if not isCharacterDefinition(char):
		raise Exception('Invalid character definition node! Object "'+char+'" does not exist or is not a valid HIKCharacterNode!')
	
	# Get Character Nodes
	charNodes = mel.eval('hikGetSkeletonNodes "'+char+'"')
	
	# Return Result
	return charNodes

def bakeAnim(char):

	# Get Character Bones
	bones = getCharacterNodes(char)
	
	# Bake Animation
	cmds.bakeResults(bones,
					simulation=True,
					t=(0,1),
					sampleBy=1,
					disableImplicitControl=True,
					preserveOutsideKeys=False,
					sparseAnimCurveBake=False,
					removeBakedAttributeFromLayer=False,
					bakeOnOverrideLayer=False,
					minimizeRotation=False,
					at=['tx','ty','tz','rx','ry','rz'] )
	
	# Return Result
	return bones


def PrepareFile():
    filename = saveTempFile()
    openFile(filename)
    BakeHumanIK()
    removeSelectedObject()

def getFilename():
    currentFilename = cmds.file( query=True,sceneName=True )
    baseName = os.path.basename(currentFilename)
    return baseName
    
def openFile(filename):
    cmds.file(newFile=True)
    cmds.file(filename, open=True)

def saveTempFile():
    savePath= "C:/Users/BOXX/Desktop/EXPORT_TEST"
    saveName = getFilename()
    saveFile = os.path.join(savePath,saveName)
    cmds.file(rename=saveFile)
    cmds.file(save=True,type='mayaAscii')
    return saveFile

def removeJoints():
    endJointsList = ['HeadTop_End','LeftHandThumb4','LeftHandIndex4','LeftHandRing4','RightHandThumb4','RightHandIndex4','RightHandRing4','LeftToe_End','RightToe_End']
    for i in range(len(endJointsList)):
        endBone = cmds.ls(endJointsList[i],type='joint')
        cmds.delete(endBone)
        
def removeSelectedObject():
    char = getCurrentCharacter()
    cmds.delete(char)
    controls = cmds.ls('Ctrls')
    cmds.delete(controls)
    removeJoints()
    

def ExportFBXSkinned(filename):
    mel.eval('FBXExportAnimationOnly -v true;')
    mel.eval('FBXExportCameras -v false;')
    mel.eval('FBXExportLights -v  false;')
    mel.eval('FBXExportSkins -v true;')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExport -f' + filename + '-s;')

def ExportCharacterBaseMesh():
    models = ['sk_male_jersey_G_AvShape','sk_male_body_G_AvShape']
    for mesh in models:
        cmds.select(mesh,add=True)
    rootJoint = cmds.ls('Joints')
    sel = cmds.select(rootJoint,hierarchy=True)
    bicycle = cmds.ls('Bicycle*',type='mesh') 
    cmds.select(bicycle,deselect=True)

        
    


if __name__ == "__main__":
    TestUI.display()

