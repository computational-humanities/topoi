#################
# Preliminaries #
#################

import os
import re
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import webbrowser
from IPython.display import HTML
from bs4 import BeautifulSoup
import requests


# To always find data, relative paths are made absolute.
# Since the structure of projects is Project/data Project/program(testing)
# this should work on any system.

script_dir = os.path.dirname(__file__)
rel_path = '../data/MedievalDiagrams_DB.json'
abs_file_path = os.path.join(script_dir, rel_path)

data_file = open(abs_file_path,encoding='utf-8')

# First load with json.load().
# Manipulations are made using pandas.
data = json.load(data_file)

dfInstances = pd.DataFrame(data['instances']['diaTyp'])
#####################################
#Open image for diagramID in new tab#
#####################################


def id2image(dataframe, diaID):
    """
    Opens link to picture of diagram type inline.

    :param diaID: diagram ID
    :type diaID: string
    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame

    :returns: webpage
    """
    url_start = 'http://repository.edition-topoi.org/digilib/digilib.html?fn=/MAPD/ReposMAPD/EastwoodCollection/'
    url_end = dataframe[dataframe['diaID']==diaID].reset_index(drop=True)['diaURL'][0]
    #print(url_start + url_end)
    return HTML('<iframe src=' + url_start + url_end + ' + width=100% height=460></iframe>')

def textId2imagegrid(dataframe, author, textID):
    """
    Opens all pictures for given author and textID as a grid.

    :param author: Name of Author
    :type author: string
    :param textID: text ID
    :type textID: string
    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame

    :returns: inline html table
    """
    #url_list = []
    imageList = []
    listRows = []
    listIDRows = []

    url_start = 'http://repository.edition-topoi.org/MAPD/ReposMAPD/'

    reddf = reducedData(dataframe,[['author',author],['textID',textID]])

    for diaID in reddf.diaID:
        url = url_start + diaID
        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data,'lxml')
        res = re.findall('([-\w]+\.(?:jpg))', str(soup))
        if res:
            imageList.append(url + '/' + res[0])

    listImgSrc = ['<td><img src={0} + width=100%/></td>'.format(x) for x in imageList]
    listTableData = [listImgSrc[x:x+3] for x in range(0,len(listImgSrc),3)]

    for x in listTableData:
        res = '<tr>' + ''.join(x) + '</tr>'
        listRows.append(res)

    url_start2 = 'http://repository.edition-topoi.org/digilib/digilib.html?fn=/MAPD/ReposMAPD/EastwoodCollection/'
    idList = ['<td><a target="_blank" href={0}>{1}</a>{2}</td>'.format(url_start2 + reddf['diaURL'].loc[x],reddf['diaID'].loc[x],', Dia. type: ' + str(reddf['diaTyp'].loc[x])) for x in range(len(reddf.diaID))]
    idListData = [idList[x:x+3] for x in range(0,len(idList),3)]

    for x in idListData:
        res = '<tr>' + ''.join(x) + '</tr>'
        listIDRows.append(res)

    fullData = [x + y for x,y in zip(listRows,listIDRows)]

    htmlcode = '<table style="width:100%"><tr><th>Diagrams in text {0} from author {1} in manuscript {2} </th><th></th><th></th></tr>'.format(textID,author,reddf['manID'].loc[0]) + ''.join(fullData) + '</table>'

    return HTML(htmlcode)

def altId2image(dataframe, diaID):
    """
    Opens browsertab with link to picture of diagram one level higher

    :param diaID: diagram ID
    :type diaID: string
    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame

    :returns: webpage
    """
    url_start = 'http://repository.edition-topoi.org/collection/MAPD/single/'
    url_end = ''.join([x for x in diaID if x.isdigit()])
    return webbrowser.open(url_start + url_end)


def manID2image(dataframe, manID):
    """
    Opens browsertab with link to startpage of manuscript

    :param diaID: manuscript ID
    :type diaID: string
    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame

    :returns: webpage
    """
    url_start = 'http://repository.edition-topoi.org/collection/MAPD/object/'
    url_end =  dataframe[dataframe['manID']==manID].reset_index(drop=True)['manURL'][0].split('&')[0]
    return webbrowser.open(url_start + url_end)

#######################
# Load Citeables      #
#######################




#######################
# Normalize JSON file #
#######################

def level0(manuscr):
    """
    Normalization on manuscript level.
    Axis 'texts' is dropped.

    :param manuscr: Manuscript number
    :type manuscr: int

    :returns: DataFrame
    """
    try:
        res = json_normalize(data['manuscripts'][manuscr]).drop('texts',axis=1)
        return res
    except IndexError:
        print("Out of range.")
        pass


def level1(manuscr,text):
    """
    Normalization on text level.
    Axis 'pages' is dropped.

    :param manuscr: Manuscript number
    :param text: Text number
    :type manuscr: int
    :type text: int

    :returns: DataFrame
    """
    try:
        res = json_normalize(data['manuscripts'][manuscr]['texts']\
                             [text]).drop('pages',axis=1)
        return res
    except IndexError:
        pass

def level2(manuscr, text, page):
    """
    Normalization on pages level.
    Axis 'diagrams' is dropped.

    :param manuscr: Manuscript number
    :param text: Text number
    :param page: Page number
    :type manuscr: int
    :type text: int
    :type page: int

    :returns: DataFrame
    """
    try:
        res = json_normalize(data['manuscripts'][manuscr]['texts'][text]
                             ['pages'][page]).drop('diagrams',axis=1)
        return res
    except IndexError:
        pass

def level3(manuscr,text, page,diagram):
    """
    Normalization on diagram level.
    Axis 'diaAttr' is dropped.

    :param manuscr: Manuscript number
    :param text: Text number
    :param page: Page number
    :param diagram: Diagram number
    :type manuscr: int
    :type text: int
    :type page: int
    :type diagram: int

    :returns: DataFrame
    """
    try:
        res = json_normalize(data['manuscripts'][manuscr]['texts'][text]\
        ['pages'][page]['diagrams']).drop('diaAttr',axis=1)
        res = res.iloc[diagram].to_frame().transpose().reset_index(drop=True)
        return res
    except IndexError:
        pass

def level4(manuscr, text, page, diagram):
    """
    Normalization on diagram attributes level.

    :param manuscr: Manuscript number
    :param text: Text number
    :param page: Page number
    :param diagram: Diagram number
    :type manuscr: int
    :type text: int
    :type page: int
    :type diagram: int

    :returns: DataFrame
    """
    try:
        res = json_normalize(data['manuscripts'][manuscr]['texts'][text]\
        ['pages'][page]['diagrams'][diagram]['diaAttr'])
        return res
    except IndexError:
        pass

def diagCon(manuscr, text, page, diagram):
    """
    Construct dataframe with all information contained
    in the JSON file for one specific diagram.

    :param manuscr: Manuscript number
    :param text: Text number
    :param page: Page number
    :param diagram: Diagram number
    :type manuscr: int
    :type text: int
    :type page: int
    :type diagram: int

    :returns: DataFrame
    """
    res = level0(manuscr).join(level1(manuscr,text).\
                               join(level2(manuscr,text,page).\
                                    join(level3(manuscr,text,page,diagram).\
                                         join(level4(manuscr,text,page,diagram)))))
    return res

#########################################
# Determining length of different lists #
#########################################
def rangeMan():
    """Range of manuscript list.

    Uses full json file, therefore no parameter.

    :returns: range
    """
    res = len(data['manuscripts'])
    return range(res)

def rangeTexts(manuscr):
    """Range of text list.

    :param manuscr: Manuscript index
    :type manuscr: int
    :returns: range
    """
    res = len(data['manuscripts'][manuscr]['texts'])
    return range(res)

def rangePages(manuscr, text):
    """Range of pages list.

    :param manuscr: Manuscript index
    :type manuscr: int
    :param text: Text number
    :type tex: int
    :returns: range
    """
    res = len(data['manuscripts'][manuscr]['texts'][text]['pages'])
    return range(res)

def rangeDiag(manuscr, text, page ):
    """"Range of diagram list.

    :param manuscr: Manuscript index
    :type manuscr: int
    :param text: Text number
    :type tex: int
    :param page: Page number
    :type page: int
    :returns: range
    """
    res = len(data['manuscripts'][manuscr]['texts'][text]['pages'][page]['diagrams'])
    return range(res)

##################################################
# Constructing dataframe for one manuscript index#
##################################################
def biblioCon(manuscr):
    """
    Constructs the full dataframe for one manuscript index.

    :param manuscr: Manuscript number
    :type manuscr: int
    :returns: DataFrame
    """
    tempList = []
    for t in rangeTexts(manuscr):
        for p in rangePages(manuscr,t):
            for d in rangeDiag(manuscr,t,p):
                tempList.append(diagCon(manuscr,t,p,d))
    tempRes = pd.concat(tempList).reset_index(drop=True)
    return tempRes

######################
#Construct dataframe #
######################

# Careful!, takes time and can use quite a lot of memory
def medDiaCon(x):
    """
    Constructs a dataframe for the first k entries in the manuscript index.

    :warning:

        Takes some time to build full dataframe (x=236),
        memory usage is high, too.

    :param x: Number of manuscripts to include.
    :type x: int
    :returns: Dataframe
	"""
    tempList = []
    for i in range(x):
        tempList.append(biblioCon(i))
    res = pd.concat(tempList).reset_index(drop=True)
    return res

#######################
# Helper functions    #
#######################

def uniqueValues(dataframe, key = 'author'):
    """Get the unique dataframe values for a given column name.

    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame
    :param key: Column key (default = 'author')
    :type key: string
    :returns: list
    """
    dfType = str(type(dataframe).__name__)

    assert dfType == 'DataFrame', 'Please provide dataframe. Provided data is of type: %s ' % dfType

    if key in dataframe.keys().tolist():
        res = list(set(dataframe[key].tolist()))
        #print('For the key: "' + key + '" the following unique values exist:')
        return res
    else:
        print(key + ' is not a valid key for the given dataframe.')

def authorKey(dataframe, author, key):
    """Get all different values for one key for a given author.

    :param dataframe: DataFrame
    :param author: Name of author
    :param key: Column name
    :type dataframe: pandas.DataFrame
    :type author: string
    :type key: string
    :returns: list
    """
    dfType = str(type(dataframe).__name__)

    assert dfType == 'DataFrame', 'Please provide dataframe. Provided data is of type: %s ' % dfType

    if key in dataframe.keys().tolist():
        res = list(set(dataframe[dataframe['author'] == author][key].tolist()))
        #print(author + ' has for the key "' + key + '" the following different entries:\n')
        return res
    else:
        print(key + ' is not a valid key.')


def diagYearAuthor(dataframe, author):
    """
    Returns dataframe with unique diagram IDs and corresponding years
    for given author.

    :param dataframe: DataFrame
    :param author: name of author
    :type dataframe: pandas.DataFrame
    :type author: string

    :returns: DataFrame

    :example:
        >>> diagYearAuthor(df,'Plinius')
            DataFrame
    """
    dfType = str(type(dataframe).__name__)

    assert dfType == 'DataFrame', 'Please provide dataframe. Provided data is of type: %s ' % dfType

    resdiaID = dataframe[dataframe['author'] == author]['diaID']
    resdate= dataframe[dataframe['author'] == author]['date']
    resUnique = pd.concat([resdiaID,resdate],axis=1).reset_index(drop=True).drop_duplicates(subset = 'diaID')
    return resUnique


def diaID2Type(dataframe, diaID):
    """
    Gives the diagram typ for a given diagram ID.

    :param dataframe: dataframe
    :type dataframe: pandas.DataFrame
    :param diaID: Diagram ID
    :type diaID: string

    :returns: float

    :example:
        >>> diaID2Type(df,'MAPD0249')
            15.0
    """
    dfType = str(type(dataframe).__name__)

    assert dfType == 'DataFrame', 'Please provide dataframe. Provided data is of type: %s ' % dfType

    resTemp = dataframe[dataframe['diaID'] == diaID]['diaTyp']
    if 0 in list(resTemp.shape):
        print(' DiaID not found.')
    else:
        res = resTemp[resTemp.index.values[0]]
        return res

def diaTypeDescr(dataframe,diaType):
    """
    Returns name and description of diagram typ.

    :param dataframe: dataframe
    :param diaTyp: diagram typ
    :type dataframe: pandas.DataFrame
    :type diaTyp: float
    :returns: text
    """
    head = dfInstances[dfInstances['diaTyp']==diaType]['diaName'][diaType-1]
    body = dfInstances[dfInstances['diaTyp']==diaType]['diaDescription'][diaType-1]
    print(head + '\n')
    print(body)


# get new dataframe object for given list of key, value pairs, reseting the original index
# Depending on key, value can be string, float or int
def reducedData(dataframe, keyValueList,debug=False):
    """Construct reduced dataframe for (key, value) pair.
    If value is of type string, partial strings are also matched.
    Columns are only dropped from dataframe, if all values are NaN.
    If debug=True: asserts whether values have correct type() for given key.
    Returns empty dataframe, if no dataset fulfills all conditions.

    :param dataframe: Name of dataframe for reduction.
    :type dataframe: pandas.DataFrame
    :param override: Override key-value-dtype assertion, default: False
    :type override: bool
    :param keyValueList: List of (key,value) pairs to consider
    :type keyValueList: list of lists, e.g. [['a','b'],['c','d']]
    :returns: DataFrame
    """

    dfType = str(type(dataframe).__name__)
    assert dfType == 'DataFrame', 'Please provide dataframe. Provided data is of type: %s ' % dfType

    if debug:
        typKeyList = [type(dataframe[key][0]) for key in [x[0] for x in keyValueList]]
        typValueList = [type(value) for value in [x[1] for x in keyValueList]]
        assert typKeyList == typValueList, 'Possible failure in dtype:\n %s \n %s' % (typKeyList,typValueList)
    else:
        pass

    condList = []
    # Old search for full strings
    # for x in keyValueList:
    #     if isinstance(x[1],str):
    #         resTemp = '(dataframe["' + x[0] + '"] == "' + x[1] + '")'
    #         condList.append(resTemp)
    #     else:
    #         resTemp = '(dataframe["' + x[0] + '"] == ' + str(x[1]) + ')'
    #         condList.append(resTemp)
    #     result = dataframe.loc[eval('& '.join(condList))]
    for x in keyValueList:
        if isinstance(x[1],str):
            if '('  in x[1] or ')' in x[1]:
                x[1] = x[1].replace('(','\(').replace(')','\)')
            resTemp = '(dataframe["' + x[0] + '"].str.contains("' + x[1] + '")==True)'
            condList.append(resTemp)
        else:
            resTemp = '(dataframe["' + x[0] + '"] == ' + str(x[1]) + ')'
            condList.append(resTemp)
        result = dataframe.loc[eval('& '.join(condList))]
    if debug:
        if 0 in result.shape:
            print('Conditions can not be fulfilled. DataFrame empty.\n',keyValueList, ' & '.join(condList))
    return result.reset_index(drop=True).dropna(axis=1,how='all')


def diaAttrPlot(dataframe, author, diaTyp):
    """Prepares diagram attributes for plotting as bar plot grouped by date.

    :param dataframe: DataFrame
    :param author: Name of author
    :param diaTyp: Diagram typ
    :type dataframe: pandas.DataFrame
    :type author: string
    :type diaTyp: float
    :returns: DataFrame
    """
    resList = []
    for date in authorKey(dataframe,author,'date'):
        dftemp = reducedData(dataframe,[['author',author],['diaTyp',diaTyp],['date',np.int64(date)]]).dropna(axis=1,how='all')
        # List column names
        colList=list(dftemp.columns.values)
        # Regex search string for attributes of diaTyp = diaTyp
        regexstr = "^(?!M" + str(int(diaTyp)) + "|\.).*"
        regex=re.compile(regexstr)
        # List all column names that do not fit and drop them.
        listAttr = [m.group(0) for l in colList for m in [regex.search(l)] if m]
        dftemp2 = dftemp.drop(listAttr,axis=1)
        # Data cleaning for unknown attributes
        if '?' in dftemp2.values:
            res = dftemp2.replace(['?'],[None]).sum().to_frame(name='attribute')
        else:
            res = dftemp2.sum().to_frame(name='attribute')
        res['date'] = int(date)
        resList.append(res)
    result = pd.concat(resList)
    result.sort_values(by='date',inplace=True)
    return result
