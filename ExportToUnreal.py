import maya.cmds as cmds
import maya.mel as mel

class TestUI(object):
    
    WINDOW_NAME = "czTestUi"
    FORM_OFFSET = 2

    @classmethod
    def display(cls):
        cls.delete_window()
        
        main_window = cmds.window(cls.WINDOW_NAME, title=cls.WINDOW_NAME, rtf=True)        
        main_layout = cmds.columnLayout( adjustableColumn=True,parent=main_window,rowSpacing=5,columnWidth=50)
        wrapper_layout = cmds.rowLayout( numberOfColumns=2, columnWidth2=(250, 150), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)],parent=main_layout )
        left_col_layout = cmds.columnLayout( adjustableColumn=True,rowSpacing=5,parent=wrapper_layout)
        cmds.frameLayout( label='Buttons' )
        cmds.columnLayout( adjustableColumn=True,rowSpacing=5,parent=left_col_layout)
        right_col_layout = cmds.columnLayout( adjustableColumn=True,rowSpacing=5,parent=wrapper_layout)
        cmds.frameLayout( label='Buttons' )
        cmds.columnLayout( adjustableColumn=True,rowSpacing=5,parent=right_col_layout)
        cmds.intSlider()

        cmds.showWindow()
    
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
    pass


if __name__ == "__main__":
    TestUI.display()

