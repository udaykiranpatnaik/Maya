import maya.cmds as mc
import maya.mel as mel
import os
import json

effectorPivotNodes = ['Ctrl_LeftAnkleEffector','Ctrl_RightAnkleEffector']
effectorAttributeList = ['pinning','reachTranslation','reachRotation','pivotOffsetX','pivotOffsetY','pivotOffsetZ','look','radius','translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','translateOffsetX','translateOffsetY','translateOffsetZ','rotateOffsetX','rotateOffsetY','rotateOffsetZ','scaleOffsetX','scaleOffsetY','scaleOffsetZ','pull','stiffness']
jointAttributeList = ['look','radius']
customAttributeList =['Finger01_Roll','Finger02_Roll','Fist_Roll','Thumb_Roll']
attributes = {}
attributes["effector"] = []

def createWindow():
    windowID = 'window'

    if mc.window(windowID, exists = True):
         mc.deleteUI('window')

    window = mc.window(windowID, title="Copy Rig", iconName='Copy Rig', widthHeight=(400, 200) )
    mc.frameLayout( label='')

    mc.button( label='Copy Rig Data' ,command=getEffectorAttributes)
    mc.button( label='Import Rig Data' ,command=importRigData)

    mc.showWindow( window )

def addCustomAttribute(node):
    mc.select(cl=True)
    selectedControl = mc.ls(node)[0]
    for attr in customAttributeList:
        mc.addAttr(selectedControl, shortName=attr, longName=attr, defaultValue=0,minValue=-10, maxValue=10, keyable=True)


def getCurrentCharacter():
    	char = mel.eval('hikGetCurrentCharacter()')
	return char

def setCurrentCharacter(char):
	mel.eval('hikSetCurrentCharacter("'+char+'")')
	mel.eval('hikUpdateCharacterList()')
	mel.eval('hikSetCurrentSourceFromCharacter("'+char+'")')
	mel.eval('hikUpdateSourceList()')

def createEffectorPivots(index) :
    char = getCurrentCharacter()
    effector = char+'_'+effectorPivotNodes[index]
    mc.select(effector)
    mel.eval('hikCreateAuxPivot ' + effector)
    mel.eval('hikCreateAuxPivot ' + effector)

def addSetDrivenKeys():
    obj = mc.ls(selection = True)
    effector = obj[0]
    driver = effector + '.' + customAttributeList[0]
    mc.setAttr(driver,0)
    # driven = 
    mc.setDrivenKeyframe(driven, cd=driver, value=0, driverValue=0)
    mc.setAttr(driver,10)
    mc.setDrivenKeyframe(driven, cd=driver, value=10, driverValue=10)

def getEffectorAttributes (*args) :
    effectorList = mc.ls(type = 'hikIKEffector')
    for i in range(0,len(effectorList)):
        data ={}
        data["index"] = effectorList.index(effectorList[i])
        data["name"] = effectorList[i].encode("utf-8")
        data["attributes"] = {}
        for prop in effectorAttributeList:
            _property = effectorList[i] + "." + prop
            data["attributes"][_property] = mc.getAttr(effectorList[i] + '.' + prop)
        attributes["effector"].append(data)
    exportJsonData(attributes)
    print "Attributes exported successfully"

def setEffectorAttributes () :
    data = loadJsonData()
    effectorList = data['effector']
    for index in range(0, len(effectorList)):
        effector = effectorList[index]
        node=effector['name']
        attributes = effector['attributes']
        mc.select(node)
        for key, value in attributes.items():
            mc.setAttr(key, value)
        
def exportJsonData (data) :
    scriptPath = getScriptPath()
    savePath = os.path.join(scriptPath,'attibuteData.json')
    json_object = json.dumps(data, indent = 4) 
    with open(savePath, "w") as outfile: 
        outfile.write(json_object)

def loadJsonData () :
    scriptPath = getScriptPath()
    savePath = os.path.join(scriptPath,'attibuteData.json')
    with open(savePath) as f:
        data = json.load(f)
    return data

def getScriptPath () :
    maya_root = os.environ['MAYA_APP_DIR']
    script_path = os.path.join(maya_root,'scripts')
    return script_path

def importRigData (*args):
    createEffectorPivots(0)
    createEffectorPivots(1)
    setEffectorAttributes()

def importRigData (*args) :
    createWindow()
    createEffectorPivots(0)
    createEffectorPivots(1)
    setEffectorAttributes()
    addCustomAttribute('Character1_Ctrl_LeftWristEffector')
    addCustomAttribute('Character1_Ctrl_LeftWristEffector')

createWindow()