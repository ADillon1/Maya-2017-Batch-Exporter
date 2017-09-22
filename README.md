# Maya 2017 Batch Exporter

This project is a batch model exporter for Maya 2017 written in Python, using Qt and PyMel. It currently supports the following file types:

1. OBJ
2. FBX
3. Maya Binary
4. Maya ASCII

The tool is designed to allow the user to quickly export everything currently selected in Maya's outliner into the selected folder with the given file type. The tool also respects outliner groups, exporting grouped objects together in the same file automatically. The resuling output files will share the name of the outliner object/group name. 

See Use for more details.

# Installation
Simply download/copy the code in the [batch-exporter.py](https://github.com/ADillon1/Maya-2017-Batch-Exporter/blob/master/batch-exporter.py) file. You can either run the code in the [script editor](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-7C861047-C7E0-4780-ACB5-752CD22AB02E-htm.html) or add it to a maya [shelf](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/Maya/files/GUID-70DA24D9-26C1-4ADD-8B5E-4AF26AB3A43B-htm.html) of your choice.

# Use

1. Run the tool. The exporter will automatically enable any necessary plugins.
2. Press the browse button at the top right of the window. This will bring up a file dialog allowing you to select a location to export to. It should show up in the box marked "Location." The default will always be the root C:\ directory.
3. Select an export file type from the File Type dropdown on the bottom right of the window.
4. Open the outliner and select all the objects/groups you would like to export. Be wary of object and group names, as these names are used for the names of the output files.
5. Press the Export button. Info/errors will show up in the output window in the middle.
6. Your files will show up in the target directory.

# Coming soon

1. Option to auto freeze transforms
2. Fix default location issue. 'C:\' changed to 'C:'
3. Move objects to origin and back while exporting
