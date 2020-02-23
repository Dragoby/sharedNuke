import re
import nuke
import traceback

HEX_COLOURS = {'lightGreen': '#03CC00',
               'lightBlue': '#00B3CC'}

SEARCH_FOR_COLOUR = HEX_COLOURS.get('lightGreen')
REPLACE_WITH_COLOUR = HEX_COLOURS.get('lightBlue')
SPACE_CHARACTER = '&nbsp;'


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


def getComparisonLabel(node, knobName, searchFor, replaceWith, useRegex=False):
    """
    This is used to collect the label info in formatted strings with the appropriate colours to be displayed in the
    interface
    Args:
        node (nuke.Node): This is the node in which to create the label information for
        knobName (str): This is the knob name to get the label information for
        searchFor (str): This is the original text that is to be replaced
        replaceWith (str): This is the text to use for the replacement
        useRegex (bool|optional): True or false if the given search for is a regex

    Returns:
        dict: This is a dictionary containing all of the label information if it can be collected
              ie: {'colouredSearchFor': <search for string with coloured formatting>,
                   'colouredReplaceWith': <replace with string with coloured formatting>,
                   'colouredOriginalValue': <the full value with the coloured formatted search for in it>
                   'colouredNewValue': <the full value with the coloured formatted replacement in it>
                   'currentValue': <the current value of the given knob>,
                   'knob': <the name of the knob the values pertain to>}
    """
    labelInfo = {'colouredSearchFor': searchFor,
                 'colouredReplaceWith': replaceWith,
                 'currentValue': None,
                 'knob': knobName}
    if not hasKnob(node, knobName):
        return labelInfo

    labelInfo['currentValue'] = node[knobName].value()
    labelInfo['colouredReplaceWith'] = '<font color="{colour}">{value}</font>'.format(colour=REPLACE_WITH_COLOUR,
                                                                                      value=replaceWith)
    labelInfo['colouredSearchFor'] = '<font color="{colour}">{value}</font>'.format(colour=SEARCH_FOR_COLOUR,
                                                                                    value=searchFor)
    if useRegex:
        match = re.search(searchFor, labelInfo.get('currentValue', ''), re.DOTALL)
        if match:
            labelInfo['colouredSearchFor'] = '<font color="{colour}">{value}</font>'.format(colour=SEARCH_FOR_COLOUR,
                                                                                            value=match.group())
        else:
            return labelInfo

        labelInfo['colouredNewValue'] = re.sub(searchFor,
                                               labelInfo.get('colouredReplaceWith', replaceWith),
                                               labelInfo.get('currentValue', ''),
                                               re.DOTALL)

        labelInfo['colouredOriginalValue'] = re.sub(searchFor,
                                                    labelInfo.get('colouredSearchFor', searchFor),
                                                    labelInfo.get('currentValue', ''),
                                                    re.DOTALL)
    else:
        labelInfo['colouredNewValue'] = labelInfo.get('currentValue',
                                                      '').replace(searchFor,
                                                                  labelInfo.get('colouredReplaceWith', replaceWith))
        labelInfo['colouredOriginalValue'] = labelInfo.get('currentValue',
                                                           '').replace(searchFor,
                                                                       labelInfo.get('colouredSearchFor', searchFor))

    return labelInfo


def replaceValues(nodes, knobs, searchFor, replaceWith, useRegex=None):
    """
    This is used to set the values on the given nodes on the specified knobs with the appropriate replaced values
    Args:
        nodes (set|list): This is a set or list of the nodes to process the replacements on
        knobs (set|list): This is a set or list of knobs to attempt the replacement on
        searchFor (str): This is the original text that is to be replaced
        replaceWith (str): This is the text to use for the replacement
        useRegex (bool|optional): True or false if the given search for is a regex
    """

    for node in nodes:
        knobs = dict()
        for knob in knobs:
            if not hasKnob(node, knob):
                continue
            currentValue = node[knob].value()
            if useRegex:
                newValue = re.sub(searchFor, replaceWith, currentValue)
            else:
                newValue = currentValue.replace(searchFor, replaceWith)
            node[knob].setValue(newValue)
