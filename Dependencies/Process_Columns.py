# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 12:43:17 2017

@author: kibs
"""
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


#Result = {'Delta':y1,'Theta':y2,'Alpha':y3,'Beta':y4,'Gamma':y5}



def Standardize_Col(data, col):
    print('Standardizing column: %s'%col)
    max_col = max(data[col])
    min_col = min(data[col])
    result = (data[col] - min_col)/(max_col - min_col)
    
    return result
    
def Process_Targets(data, col):
    print('Processing target columns')
    
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data[col]) #encode the string into numerics

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    
    columns_names = [i for i in range(len(onehot_encoded[0]))]
    
    for counter in range(len(data[col])):        
        item = list(onehot_encoded[counter])
        columns_names[item.index(1)] = data[col][counter]

#  ['Movement time', 'Sleep stage 1', 'Sleep stage 2', 'Sleep stage 3', 'Sleep stage 4', 'Sleep stage ?', 'Sleep stage R', 'Sleep stage W']
    newtargets_int = label_encoder.transform(data['target']) #encode the string into numerics
    newtargets_int = newtargets_int.reshape(len(newtargets_int), 1)
    newtargets = onehot_encoder.transform(newtargets_int)
    
#    print newtargets
#    print columns_names
    
    for counter in range(len(columns_names)):
        data[columns_names[counter]] = newtargets[:,counter]
    
    data.pop('target')
    
    return data