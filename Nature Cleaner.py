# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 13:31:29 2019

This is where the processing actually happens.

@author: devon
"""
import pandas as pd
import numpy as np


#The "type" also ended up having the date in it separated by "|", this gets rid
#of the date in "type" and also creates a separate "year" column for later convenience
def splitter(data):   
    m = len(data)
    
    year = pd.DataFrame(np.empty(m))
    
    for i in range(m):
        temp = (data.loc[i,'Type']).split('|')
        temp = temp[0]
        data.loc[i,'Type'] = temp
        temp = str(data.loc[i,'Date'])
        year.iloc[i] = temp[-4:]
    
    year.columns = ['Year']  
    data = pd.concat([data,year],axis=1)
    
    data.to_csv('data_clean.csv',index=False)
    

#This eliminates whitespace before and after the "type"
def spacecleaner(data):
    m = len(data)
    
    for i in range(m):
        temp = data.loc[i,'Type'].split()
        if len(temp) > 1:
            for j in range(len(temp)-1):
                temp[0] = temp[0] + ' ' + temp[j+1]
            temp = temp[0]
        data.loc[i,'Type'] = temp
    data.to_csv('data_clean.csv',index=False)

#This sorts the data by what "type" of title it is
def sorter(data):
    m = len(data)
    data = data.sort_values(by=['Type'])
    data = data.reset_index(drop=True)
    data.to_csv('data_clean.csv',index=False)

#This separates all of the different types of publications into separate csv files with just a 
#title, year, and detailed date
def separator(data):
    m = len(data)
    firstflag = True
    flag = True
    i = 0
    typename = data.loc[i,'Type']
    
    while flag == True and i < m:
        
        if data.loc[i,'Type'] == typename:
            if firstflag == True:
                firstflag = False
                current_type = pd.DataFrame([data.loc[i,'Name'],data.loc[i,'Year'],data.loc[i,'Date']])
                data = data.drop([i])
            else:
                current_type = pd.concat([current_type,pd.DataFrame([data.loc[i,'Name'],data.loc[i,'Year'],data.loc[i,'Date']])],axis=1,ignore_index=True)
                data = data.drop([i])
        else:
            flag = False
        i += 1
    data = data.reset_index(drop=True)
    typename = str(typename)
    typename = typename + '.csv'
    current_type.T.to_csv(typename,index=False)
    data = data.sort_values(by=['Type'])
    print(data.loc[0,'Type'])


#This actually counts the number of instances of different words. For the main analysis 
#I wanted to exclude common words that are non-topic specific, so I check if they are part of
#the "boringwords" dictionary
def counter():
    data = pd.read_csv('Letter.csv')
    m = len(data)
    data = data.sort_values(by=['1'])
    data = data.reset_index(drop=True)
    boringwords = {'a','on','of','the','in','and','by','for','to','from',\
                   'with','an','is','at','as','during','control','formation',\
                   'via','reveals','through','using','into','that','evidence',\
                   'controls','systen','basis','observation','single','origin',\
                   'two','regulates','activity','promotes','new','large',\
                   'reveal','revealed','are','analysis','years','its',\
                   'distinct','states','loss','[letters','editor]','remarkable'\
                   'recent','â€œthe','mr.','observations','scientific','phenomena'\
                   ,'january','february','march','april','may','june','july',\
                   'august','september','october','november','december','notes'\
                   ,'prof.','bias','"the','remarkable','theory','science','british'\
                   ,'effect','research','principle','or',':','method','between',\
                   'determination','some','effects'}

    #I was a bit cusious when these particular terms were popular
    potatocount = np.empty(29)
    cellcount = np.empty(29)
    climatecount= np.empty(29)
    
    lettercount = np.empty(29)
    uniquecount= np.empty(29)
    
    countindex = 0
    firstflag = True
    yearindex = 0
    for startyear in range(1874,2019,5):
        endyear = startyear + 5
        counts = dict() 
        outputdict = dict()
        lettercount[countindex] = 0
        letterlen = []
        for i in range(m):
            if data.iloc[i,1] >= startyear and data.iloc[i,1] <= endyear:
                lettercount[countindex] += 1
                temp = data.iloc[i,0].split()
                letterlen.append(int(len(temp)))
                if len(temp) == 36:
                    print(data.iloc[i,0])
                    
                for j in range(len(temp)):
                    temp2 = temp[j]
                    temp2 = temp2.casefold()
                    if temp2 == 'cells':
                        temp2 = 'cell'
                    if (temp2 not in boringwords):
                        if (temp2 in counts):
                            counts[temp2] += 1
                        else:
                            counts[temp2] = 1
                        if temp2 in outputdict:
                            outputdict[temp2] += 1
                        else:
                            outputdict[temp2]= 1
        tempdf = pd.DataFrame.from_dict(outputdict,orient = 'index')
        tempdf.columns = [startyear]
        tempdf = tempdf.sort_values(startyear,ascending = False)
        tempdf = tempdf.iloc[:25]
        
        if firstflag == True:
            outputdf = tempdf
            letterlendf = pd.DataFrame(letterlen)
            firstflag = False
        else:
            letterlentempdf = pd.DataFrame(letterlen)
            letterlendf = pd.concat([letterlendf,letterlentempdf],axis=1)
            tempfiller = pd.DataFrame(np.zeros(len(outputdf)))
            tempfiller.index = outputdf.index
            tempfiller.columns = [startyear]
            outputdf = pd.concat([outputdf,tempfiller],axis = 1)
            for i in range(len(tempdf)):
                if tempdf.iloc[i].name in outputdf.index:
                    row = tempdf.iloc[i].name
                    outputdf.loc[row,startyear] = int(tempdf.iloc[i])
                else:
                    bottomfiller = pd.DataFrame([0]*(yearindex+1)).T
                    bottomfiller.iloc[0,-1] = int(tempdf.iloc[i])
                    bottomfiller.index = [tempdf.iloc[i].name]
                    bottomfiller.columns = outputdf.columns
                    outputdf = pd.concat([outputdf,bottomfiller],axis = 0)
        
        if 'potato' in counts:                    
            potatocount[countindex] = counts['potato']
        if 'cell' in counts:     
            cellcount[countindex] = counts['cell']  
        if 'climate' in counts:
            climatecount[countindex] = counts['climate']  
        counts = pd.DataFrame(counts,index = [0])
        savename = 'Counts/counts_letter_' + str(startyear) + '-' + str(endyear) + '.csv'
        counts.to_csv(savename,index=False)
        countindex += 1
        yearindex += 1
        [filler,uniquecount] = counts.shape
        print(sum(counts.iloc[0,:]))
        
    return(potatocount,cellcount,lettercount,climatecount,outputdf)   
    
if __name__ == '__main__':
    data = pd.read_csv('Nature_Data.csv',index=False)
    splitter(data)
    spacecleaner(data)
    sorter(data)
    separator(data)
    [potatocount,cellcount,lettercount,climatecount,outputdict] = counter()
            
        
        
        
        
        
        