import numpy as np

from medDiaJson import *
from roman_date import *
from bokeh.charts import Bar, output_notebook, show
from bokeh.io import gridplot
from bokeh.palettes import viridis



df = medDiaCon(237)
df['date'] = df['date'].apply(lambda row: from_roman(row)*100)


biblioList = []

for biblio in [x for x in authorKey(df,'Capella','biblio')]:
    # Create reduced dataframe
    resTemp = reducedData(df,[['author','Capella'],['biblio',biblio]])
    # Drop all columns appart from date, biblio and diaTyp
    temp = resTemp.drop([x for x in resTemp.columns if x not in ('date','biblio','diaTyp')],axis=1)
    # create mapping for diagram types which are present in this dataframe diaTyp : 1
    d1 = {int(x):1 for x in list(temp['diaTyp'].values) if x not in ['']}
    # and for those not present diaTyp : 0
    s1 = set(x for x in temp['diaTyp'].values if x not in [''])
    s2 = set(range(18,32))
    d2 = {int(x):0 for x in list(s1 ^ s2)}
    # combine the two dicts
    d0 = {**d1, **d2}
    # Create new dataframe with all possible diagram types for Capella
    dfTEMP = pd.DataFrame(list(zip(list(range(18,32)),[0]*14)),index=range(14),columns=['diaTyp','Count'])
    # apply the mapping
    dfTEMP['Count'] = dfTEMP['diaTyp'].map(d0)
    # copy information for biblio and date
    dfTEMP['biblio'] = biblio
    dfTEMP['date'] = temp['date'][0]
    res = dfTEMP.sort_values(by='diaTyp',inplace=True)
    # append to list of dataframes
    biblioList.append(dfTEMP)

def plotDateGrid(date):
    # Assert given date is available.
    assert date in authorKey(df,'Capella','date'), 'No entries for this date.'
    # Create list of fitting dataframes
    tempList = [biblioList[s] for s in range(len(biblioList)) if biblioList[s]['date'][0] in [date]]
    # sort by occuring diagrams
    dfDATE = sorted(tempList,key=lambda tempList: tempList['Count'].sum(),reverse=True)
    plotListDATE = []
    for x in range(len(dfDATE)):
        titleS = dfDATE[x]['biblio'][0] + '; ' + str(dfDATE[x]['date'][0]) + ' CE'
        b0 = Bar(dfDATE[x],title=titleS,label='biblio',values='Count',group='diaTyp',
        bar_width=1,ylabel='Diagrams',palette=viridis(14),width=250,height=250,
        legend=False)
        b0.xaxis.major_label_orientation = "horizontal"
        b0.xaxis.axis_label=''
        plotListDATE.append(b0)
    plotGrid = gridplot(plotListDATE,ncols=3)
    show(plotGrid )

plotDateGrid(900)
