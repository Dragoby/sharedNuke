import nuke
import os
import logging

logging.info('Adding nukeDr tool path')
currentDir = os.path.dirname(__file__)
drToolsDir = os.path.join(currentDir, 'nukeDr').replace('\\', '/')

nuke.pluginAddPath(drToolsDir)
logging.info('nukeDr tool path added')
