import maya.cmds as cmds
import maya.mel as mel
import os

class TestUI(object):
    
    WINDOW_NAME = "Export FBX Files"
    WINDOW_HEIGHT=200
    WINDOW_WIDTH=55
    FORM_OFFSET = 2
    
    @classmethod
    def display(cls):
        cls.delete_window()
        
        main_window = cmds.window(cls.WINDOW_NAME, title=cls.WINDOW_NAME, widthHeight=(cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT), rtf=True)
        main_layout = cmds.columnLayout( adjustableColumn=True,parent=main_window,columnWidth=50,rowSpacing=25)
        prepare_fbx_layout = cmds.frameLayout( label=' Prepare Model for Export',collapsable=False,parent=main_layout)
        cmds.text( label='Steps', align='center' )
        cmds.text( label='1. Set Save Directory', align='center' )
        cmds.text( label='2. Prepare File', align='center' )
        cmds.text( label='3. Use Export buttons as necessary', align='center' )
        cmds.separator( height=20, style='out' )
        cmds.setParent( '..' )
        col_1 = cmds.columnLayout( adjustableColumn=True,parent=prepare_fbx_layout,columnWidth=50,rowSpacing=5)
        cmds.button( label='Set Save Directory',w=220,command=lambda *_:SetExportDirectory(),parent=prepare_fbx_layout)
        cmds.button( label='Prepare File',w=220,command=lambda *_:PrepareFile(),parent=prepare_fbx_layout)
         
        export_fbx_layout = cmds.frameLayout( label=' FBX Mesh Export',collapsable=False,parent=main_layout,marginHeight=15)
        
        col_1 = cmds.columnLayout( adjustableColumn=True,parent=prepare_fbx_layout,columnWidth=50,rowSpacing=5)
        cmds.button( label='Export Selected Static Mesh',w=220,command=lambda *_:ExportStaticMeshes(),parent=export_fbx_layout)
        cmds.button( label='Export Selected Skinned Mesh',w=220,command=lambda *_:ExportSkeletalMeshes(),parent=export_fbx_layout)
        cmds.button( label='Export  Character Mesh',w=220,command=lambda *_:ExportCharacterBaseMesh(),parent=export_fbx_layout)
        cmds.button( label='Export  Bicycle Mesh',w=220,command=lambda *_:ExportBicycleMesh(),parent=export_fbx_layout)

    
        cmds.showWindow(main_window)
    
    
    @classmethod
    def delete_window(cls):
        if cmds.window(cls.WINDOW_NAME, exists=True):
            cmds.deleteUI(cls.WINDOW_NAME, window=True)


def BakeHumanIK():
    setCurrentCharacter('Character1')
    mel.eval('hikBakeCharacter 0;')
   
    
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
	charNodes = mel.eval('hikGetSkeletonNodes "'+ char +'"')
	
	# Return Result
	return charNodes




def SetExportDirectory():
    global EXPORT_DIRECTORY
    EXPORT_DIRECTORY = cmds.fileDialog2(dialogStyle=4,fileMode=3,okCaption='Select')[0]
    print("EXPORT_DIRECTORY : %s" % EXPORT_DIRECTORY)
    

def TestGlobal():
    print (exportDirectory)

def PrepareFile():
    saveTempFile()
    BakeHumanIK()
    removeSelectedObject()
    cmds.select(clear=True)
    cmds.file(save=True, type='mayaAscii' )
    

def getFilename():
    path = {}
    currentFilename = cmds.file( query=True,sceneName=True )
    currentFilepath = os.path.dirname(currentFilename)
    baseName = os.path.basename(currentFilename)
    path['filepath'] = currentFilepath
    path['filename'] = baseName
    return path
    
def openFile(filename,imp):
    cmds.file(newFile=True,force=True)
    if imp == False:
        cmds.file(filename, o=True)
    else:
        cmds.file(filename, i=True)

def createDirectory(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

def saveTempFile():
    #pathString = os.path.join(EXPORT_DIRECTORY,"TEMP_EXPORT")
    savePath = EXPORT_DIRECTORY
    gFile = getFilename()
    saveName = gFile['filename'].split(".")[0]
    saveFile = os.path.join(savePath,saveName)
    cmds.file(rename=saveFile)
    cmds.file(save=True,type='mayaAscii')


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
    mel.eval('FBXExportInAscii -v true;')
    mel.eval('FBXExportAnimationOnly -v true;')
    mel.eval('FBXExportCameras -v false;')
    mel.eval('FBXExportLights -v  false;')
    mel.eval('FBXExportSkins -v true;')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExport -f "' + filename + '" -s;')

def ExportFBXStatic(filename):
    mel.eval('FBXExportInAscii -v true;')
    mel.eval('FBXExportCameras -v false;')
    mel.eval('FBXExportLights -v  false;')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExport -f "' + filename + '" -s;')

def RemoveUnwantedMeshes(sel):
    cmds.select('All_Geometry')
    all_Meshes = cmds.ls(sl=True)
    for x in all_Meshes:
        if not x in sel:
            cmds.delete(x)

def RemoveDisplayLayers():
    layers = cmds.ls(type='displayLayer')
    for layer in layers:
        if layer != 'defaultLayer':
            cmds.delete(layer)


def RemoveUnusedMaterialNodes():
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')  
    

def ExportFile(pristineFile):
    result = cmds.promptDialog(
        title='Rename Object',
        message='Enter Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
        
    if result == 'OK':
        saveFilename = cmds.promptDialog(query=True, text=True)
        print(saveFilename)
        ExportFBX(saveFilename)
    openFile(pristineFile,False)


def ExportCharacterBaseMesh():
    sel = cmds.ls(sl=True)
    pristineFile = cmds.file(save=True,type='mayaAscii')
    if len(sel) == 0:
       cmds.confirmDialog( title='Select Required Meshes', message='Please Select Meshes to be Exported', button=['OK'], defaultButton='OK')
    else:    
        currentFilename = cmds.file( query=True,sceneName=True )
        openFile(currentFilename,True)
       
        # Remove Bicycle Meshes
        bi = cmds.ls('Bicycle*',type='mesh')
        cmds.select('All_Geometry')
        all_Meshes = cmds.ls(sl=True)
        for x in all_Meshes:
            if not x in sel:
                cmds.delete(x)
        
        # Remove unwanted Meshes
        RemoveUnwantedMeshes(sel)
                
        # Remove Display Layers
        RemoveDisplayLayers()
            
        # Bake Non Deformer History and Unparent Joints and Meshes
        for node in sel:
            cmds.bakePartialHistory(node,prePostDeformers=True )
            cmds.parent(node,w=True)
        cmds.parent('Joints',w=True)
        
        cmds.delete('Asset')
        cmds.delete('Model')
       
        # Remove Unused Nodes
        RemoveUnusedMaterialNodes()
        cmds.delete('All_Geometry')
        cmds.select(all=True)
        ExportFile(pristineFile)
        
def ExportBicycleMesh():
    sel=cmds.ls('Bicycle*',type='mesh')
    pristineFile = cmds.file(save=True,type='mayaAscii')
    if len(sel) == 0:
       cmds.confirmDialog( title='Select Required Meshes', message='Please Select Meshes to be Exported', button=['OK'], defaultButton='OK')
    else:    
        currentFilename = cmds.file( query=True,sceneName=True )
        openFile(currentFilename,True)
        biCycleArr = []
        for bi in sel:
            mem = cmds.listRelatives(bi,allParents=True)
            biCycleArr.append(mem[0])
        cmds.select('All_Geometry')
        all_Meshes = cmds.ls(sl=True)
        cmds.select(cl=True)
        for x in all_Meshes:
            if not x in biCycleArr:
                cmds.delete(x)
        cmds.select("Bicycle*Wheel")
        cmds.delete()
        
        cmds.parent('Joints',w=True)
        cmds.delete('Asset')
        cmds.delete('Model')

        RemoveDisplayLayers()
        # Remove Unused Nodes
        
        RemoveUnusedMaterialNodes()
        cmds.select(all=True)
        #cmds.delete('All_Geometry')
        cmds.select(all=True)
        ExportFile(pristineFile)


        
def ExportStaticMeshes():
    sel = cmds.ls(sl=True)
    pristineFile = cmds.file(save=True,type='mayaAscii')
    if len(sel) == 0:
       cmds.confirmDialog( title='Select Required Meshes', message='Please Select Meshes to be Exported', button=['OK'], defaultButton='OK')
    else:    
        currentFilename = cmds.file( query=True,sceneName=True )
        openFile(currentFilename,True)

        RemoveUnwantedMeshes(sel)
        cmds.delete('Asset')
        for node in sel:
            cmds.select(node)
            cmds.move( 0, 0, 0, node, absolute=True )
            cmds.xform( r=True, ro=(-90, 0, 0) )
            cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
            cmds.parent(node,w=True)
            cmds.delete('Model')
        
        RemoveDisplayLayers()
            
        # Remove Unused Nodes
        RemoveUnusedMaterialNodes()
        ExportFile(pristineFile)
        

        
def ExportSkeletalMeshes():
    sel = cmds.ls(sl=True)
    pristineFile = cmds.file(save=True,type='mayaAscii')
    if len(sel) == 0:
       cmds.confirmDialog( title='Select Required Meshes', message='Please Select Meshes to be Exported', button=['OK'], defaultButton='OK')
    else:    
        currentFilename = cmds.file( query=True,sceneName=True )
        openFile(currentFilename,True)
        RemoveUnwantedMeshes(sel)
        cmds.bakePartialHistory(sel[0],prePostDeformers=True )
        cmds.parent(sel[0],w=True)
        cmds.parent('Joints',w=True)
        cmds.delete('Asset')
        cmds.delete('Model')
        cmds.delete('All_Geometry')
        # Remove Display Layers
        RemoveDisplayLayers()

        # Remove Unused Nodes
        RemoveUnusedMaterialNodes()
        
        cmds.select(sel[0],r=True)
        
        ExportFile(pristineFile)


def ExportFBX(fileName):
    path = EXPORT_DIRECTORY + "/" + "FBX"
    savePath = createDirectory(path)
    savefile = savePath + "/" + fileName+".fbx"
    print(savefile)
    mel.eval('FBXExportCameras -v false;')
    mel.eval('FBXExportLights -v  false;')
    mel.eval('FBXExportSkins -v true;')
    mel.eval('FBXExportSmoothingGroups -v true;')
    mel.eval('FBXExport -f "'+savefile+'" -s')

        
if __name__ == "__main__":
    TestUI.display()

