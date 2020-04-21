import nuke
import os
import logging

currentDir = os.path.dirname(__file__)
nuke.pluginAddPath(os.path.join(currentDir, 'searchReplace').replace('\\', '/'))
