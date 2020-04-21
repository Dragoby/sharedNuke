import re
import sre_constants
import copy
import nuke
import traceback

from string import ascii_lowercase

HEX_COLOURS = {'lightGreen': '#03CC00',
               'lightBlue': '#00B3CC',
               'lightRed': '#ff5e5e'}

SEARCH_FOR_COLOUR = HEX_COLOURS.get('lightGreen')
REPLACE_WITH_COLOUR = HEX_COLOURS.get('lightBlue')
ERROR_COLOUR = HEX_COLOURS.get('lightRed')
SPACE_CHARACTER = '&nbsp;'

KNOB_POSITIONS = {'file': 0, 'label': 1}
CLASS_POSITIONS = {'all': 0, 'read': 1}

KNOB_BLACKLIST = ['help', 'onCreate', 'updateUI', 'rootNodeUpdated', 'knobChanged', 'autolabel', 'onDestroy', 'icon',
                  'name']


def hasKnob(node, knobName):
    """
    This is used to determine if the given node has the specified knob or not
    Args:
        node (nuke.Node): The node in which to check
        knobName (str): The name of the knob to check fo

    Returns:
        bool: True or False if the given knob name exists on the node
    """
    try:
        node[knobName]
    except NameError:
        return False

    return True


def getStringKnobs(node):
    """
    This will take a given node and check with knobs return a string value.  When it had gone over all knobs it will
    return a set of all the knobs that contained string values
    Args:
        node (nuke.Node): This is the node in which to collect all of the knobs for

    Returns:
        set: This is a set of all the knobs which contain string values
    """
    stringKnobNames = set()
    for knobName in node.knobs().keys():
        if knobName in KNOB_BLACKLIST:
            continue
        if isinstance(node[knobName].value(), str):
            stringKnobNames.add(knobName)

    return stringKnobNames


def getReplacementInfo(node, knobName, searchFor, replaceWith, useRegex=False, caseSensitive=True):
    """
    This is used to collect the replacement info for the given node and knob.  This will create the replacement value
    and additionally create coloured new/original values that can be used in a GUI environment
    interface
    Args:
        node (nuke.Node): This is the node in which to create the label information for
        knobName (str): This is the knob name to get the label information for
        searchFor (str): This is the original text that is to be replaced
        replaceWith (str): This is the text to use for the replacement
        useRegex (bool|optional): True or false if the given search for is a regex
        caseSensitive (bool|optional): True or False if the search is to ignore casing

    Returns:
        dict: This is a dictionary containing all of the label information if it can be collected
              ie: {'colouredSearchFor': <search for string with coloured formatting>,
                   'colouredReplaceWith': <replace with string with coloured formatting>,
                   'colouredOriginalValue': <the full value with the coloured formatted search for in it>
                   'colouredNewValue': <the full value with the coloured formatted replacement in it>
                   'currentValue': <the current value of the given knob>,
                   'knob': <the name of the knob the values pertain to>,
                   'newValue: <This is the new non coloured value>}
    """
    baseLabelInfo = {'colouredSearchFor': None,
                     'colouredReplaceWith': None,
                     'currentValue': None,
                     'knob': knobName}

    replaceWith = replaceWith.replace('\\', '/')

    labelInfo = copy.copy(baseLabelInfo)
    if not hasKnob(node, knobName) or not searchFor:
        return baseLabelInfo

    # If we are searching with case sensitive as False then we will use re to find the matches
    if not caseSensitive and not useRegex:
        searchFor = re.escape(searchFor)
        useRegex = True

    labelInfo['currentValue'] = node[knobName].value()
    labelInfo['colouredReplaceWith'] = '<font color="{colour}">{value}</font>'.format(colour=REPLACE_WITH_COLOUR,
                                                                                      value=replaceWith)
    labelInfo['colouredSearchFor'] = '<font color="{colour}">{value}</font>'.format(colour=SEARCH_FOR_COLOUR,
                                                                                    value=searchFor)
    if useRegex:
        if not caseSensitive:
            flags = re.DOTALL | re.IGNORECASE
        else:
            flags = re.DOTALL

        try:

            match = re.search(searchFor, labelInfo.get('currentValue', ''), flags)

        except sre_constants.error:
            labelInfo['error'] = 'Invalid Regex: <font color="{colour}">{value}</font>'.format(colour=ERROR_COLOUR,
                                                                                               value=searchFor)
            return labelInfo

        if match:
            labelInfo['colouredSearchFor'] = '<font color="{colour}">{value}</font>'.format(colour=SEARCH_FOR_COLOUR,
                                                                                            value=match.group())
        else:
            return baseLabelInfo

        labelInfo['colouredNewValue'] = labelInfo.get('currentValue', '').replace(match.group(),
                                                                                  labelInfo.get('colouredReplaceWith',
                                                                                                replaceWith))

        labelInfo['colouredOriginalValue'] = labelInfo.get('currentValue',
                                                           '').replace(match.group(),
                                                                       labelInfo.get('colouredSearchFor',
                                                                                     replaceWith))

        labelInfo['newValue'] = labelInfo.get('currentValue', '').replace(match.group(),
                                                                          replaceWith)

    else:
        if searchFor not in labelInfo.get('currentValue', '~'):
            return baseLabelInfo
        labelInfo['colouredNewValue'] = labelInfo.get('currentValue',
                                                      '').replace(searchFor,
                                                                  labelInfo.get('colouredReplaceWith', replaceWith))
        labelInfo['newValue'] = labelInfo.get('currentValue', '').replace(searchFor,
                                                                          replaceWith)
        labelInfo['colouredOriginalValue'] = labelInfo.get('currentValue',
                                                           '').replace(searchFor,
                                                                       labelInfo.get('colouredSearchFor', searchFor))

    return labelInfo


def replaceValues(nodes, knobs, searchFor, replaceWith, useRegex=None, caseSensitive=True):
    """
    This is used to set the values on the given nodes on the specified knobs with the appropriate replaced values
    Args:
        nodes (set|list): This is a set or list of the nodes to process the replacements on
        knobs (set|list): This is a set or list of knobs to attempt the replacement on
        searchFor (str): This is the original text that is to be replaced
        replaceWith (str): This is the text to use for the replacement
        useRegex (bool|optional): True or false if the given search for is a regex
        caseSensitive (bool|optional): True or False if the search is to ignore casing
    """

    for node in nodes:
        for knob in knobs:
            replacementInfo = getReplacementInfo(node,
                                                 knob,
                                                 searchFor,
                                                 replaceWith,
                                                 useRegex=useRegex,
                                                 caseSensitive=caseSensitive)

            try:
                success = node[knob].setValue(replacementInfo.get('newValue', replacementInfo.get('currentValue', '')))
            except (TypeError, NameError):
                success = False


def getNodeData(selected=False):
    """
    This is used to collect all nodes and their respective string knobs.  If the value on a knob is not a string then
    it will not be give as an accepted knob.

    Args:
        selected (bool|optional): True or False if the data should be collected for only selected nodes

    Returns:
        dict: This is a dictionary of all the node information.  This will contain all of the knobs for each node class
            ie: {'Blur': ['label', 'channels', etc.....
    """
    if selected:
        nodes = nuke.selectedNodes()
    else:
        nodes = nuke.allNodes()

    nodeData = dict()

    for node in nodes:
        nodeClass = node.Class()
        knobList = nodeData.get(nodeClass, list())
        if knobList:
            continue

        knobList = getStringKnobs(node)
        nodeData[nodeClass] = list(knobList)

    return nodeData


def getKnobSortIndex(knob):
    """
    This will take a given knob and get a predefined index for sorting.  This is to ensure that certain knobs will
    appear first in the list
    Args:
        knob(str) : This is the knob in which to collect the index for

    Returns:
        int: This is the index for the knob
    """
    maxPosition = max(KNOB_POSITIONS.values())
    position = KNOB_POSITIONS.get(knob, None)

    if not isinstance(position, int):
        # here we need to add 1 in order to ensure that the first index is a value of 1.  Then we add in the max
        # position of already defined keys.  This way we ensure any item that has not been defined is always after
        # The defined keys
        position = ascii_lowercase.index(knob[0].lower()) + maxPosition + 1

    return position


def getClassSortIndex(nodeClass):
    """
    This will take a given nodeClass and get a predefined index for sorting.  This is to ensure that certain classes
    will appear first in the list
    Args:
        nodeClass(str) : This is the nodeClass in which to collect the index for

    Returns:
        int: This is the index for the nodeClass
    """
    maxPosition = max(CLASS_POSITIONS.values())
    position = CLASS_POSITIONS.get(nodeClass.lower(), None)

    if not isinstance(position, int):
        # here we need to add 1 in order to ensure that the first index is a value of 1.  Then we add in the max
        # position of already defined keys.  This way we ensure any item that has not been defined is always after
        # The defined keys
        position = ascii_lowercase.index(nodeClass[0].lower()) + maxPosition + 1

    return position

