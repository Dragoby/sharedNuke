import nukescripts
import logging
from nukeDr.searchReplace.interface import main

logging.info('Adding searchReplace panel')
nukescripts.panels.registerWidgetAsPanel('main.Main',
                                         'SearchReplace',
                                         'com.nukedr.searchReplace')

logging.info('searchReplace panel added')
