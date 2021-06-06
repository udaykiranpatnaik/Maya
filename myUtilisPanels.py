import maya.cmds as cmds

def createCustomWorkspaceControlUI(*args):
  masterLayout = cmds.columnLayout(adjustableColumn=True,rowSpacing=5)
  prepare_fbx_layout = cmds.frameLayout( label=' Prepare Model for Export',collapsable=False,parent=masterLayout)


if cmds.workspaceControl("myCustomWorkspaceControl",tabToControl=('Attribute Editor', -1),uiScript="createCustomWorkspaceControlUI()",exists =True):
    cmds.deleteUI("myCustomWorkspaceControl")

cmds.workspaceControl("myCustomWorkspaceControl", retain=False, floating=False,tabToControl=('Attribute Editor', -1),uiScript="createCustomWorkspaceControlUI()");

