"""
/***************************************************************************
Atrribute based clustering
                                 A QGIS plugin
Plugin produces clustering for features of vector layer based on unlimited number of attributes using hierarchical or k-means algorithms.
Hierarchical algorithm is native, k-means requieres scipy. You can define weight for every attribute, if hierarchical clustering used.

                              -------------------
        begin                : 2016-04-23
        copyright            : (C) 2016 by Eduard Kazakov
        email                : silenteddie@gmail.com
        homepage             : http://ekazakov.info
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import *

# Return vector layer by it's name, or None
from PyQt4.QtCore import QVariant, Qt

import numpy as np
import math

# return QgsLayer by it's name
def getLayerByName(vectorLayerName):
    layer = None
    for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
        if lyr.name() == vectorLayerName:
            layer = lyr
            break

    return layer

# return list of names of layer's fields. Second parameter can contain types of needed fields
# e.g. ['Integer','Real']
def getAttributesListOfVectorLayer(layer, types=None):
    names = []

    for field in layer.pendingFields():
        if not types:
            names.append(field.name())
        else:
            if str(field.typeName()) in types:
                names.append(field.name())

    return names

# calculates simple distance in n-dimensions
def calculateDistance (a,b, weights):
    sum_sqr = 0
    k = 0

    for i, j in zip(a,b):
        sum_sqr += weights[k]*((float(i)-float(j))**2)
        k += 1
    distance = math.sqrt(sum_sqr)
    return distance

# get average between two n-dimensional points
def getAverageOfTwo (a,b):
    newObject = []
    i = 0
    while i < len (a):
        newObject.append((a[i]+b[i])/2.0)
        i += 1
    return newObject

# Performs hierarchical clustering. Updates vector layer field.
def hierarchicalClustering (vectorLayer, attributesList, normalize, clusterNumber, outputFieldName):
    weights = []
    # weights array
    for attribute in attributesList:
        weights.append(attribute[1])

    fullObjectsList = []
    clusterObjectList = []
    features = vectorLayer.getFeatures()

    # create full list with all characteristics
    for feature in features:
        fullObjectsList.append([])
        for attribute in attributesList:
            if feature[attribute[0]]:
                fullObjectsList[len(fullObjectsList)-1].append(feature[attribute[0]])
            else:
                fullObjectsList[len(fullObjectsList)-1].append(0)
        clusterObjectList.append([feature.id()])

    #NORMALIZING (if needed)
    if normalize:
        i = 0
        maxValues = []
        while i < len(attributesList):

            maxValues.append(max(item[i] for item in fullObjectsList))
            i += 1

        j = 0
        while j < len(fullObjectsList):
            i = 0
            while i < len(fullObjectsList[j]):
                fullObjectsList[j][i] = (fullObjectsList[j][i] * 1.0) / (maxValues[i] * 1.0)
                i += 1
            j += 1

    # GO CLUSTERING
    currentClusterNum = len(fullObjectsList)
    while currentClusterNum > clusterNumber:
        # Distance matrix
        distanceMatrix = []
        i = 0
        min = None
        min_i = 0
        min_j = 0
        while i < currentClusterNum:
            distanceMatrix.append([])
            j = 0
            while j < currentClusterNum:
                if j >= i:
                    distanceMatrix[i].append(0.0)
                    j += 1
                    continue
                currentDistance = calculateDistance(fullObjectsList[j],fullObjectsList[i],weights)
                if (min == None) and (i != j):
                    min = currentDistance
                    min_i = i
                    min_j = j

                if (currentDistance < min) and (i != j):
                    min = currentDistance
                    min_i = i
                    min_j = j

                distanceMatrix[i].append(round(currentDistance, 2))
                j += 1

            i += 1

        # split two objects into one
        fullObjectsList[min_i] = getAverageOfTwo(fullObjectsList[min_i],fullObjectsList[min_j])
        del fullObjectsList[min_j]

        # updating array with clusters id
        k = 0
        while k < len(clusterObjectList[min_j]):
            clusterObjectList[min_i].append(clusterObjectList[min_j][k])
            k += 1
        del clusterObjectList[min_j]


        currentClusterNum -= 1

    #Working with layer
    vectorLayerDataProvider = vectorLayer.dataProvider()

    # Create field of not exist
    if vectorLayer.fieldNameIndex(outputFieldName) == -1:
        vectorLayerDataProvider.addAttributes([QgsField(outputFieldName, QVariant.Int)])

    vectorLayer.updateFields()
    vectorLayer.startEditing()
    attrIdx = vectorLayer.fieldNameIndex(outputFieldName)
    features = vectorLayer.getFeatures()

    for feature in features:
        i = 0
        for idList in clusterObjectList:
            if feature.id() in idList:
                vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(i))
            i += 1

    vectorLayer.updateFields()
    vectorLayer.commitChanges()



# Performs K-Means clustering. Updates vector layer field.
def kmeans_clustering (vectorLayer, attributesList, normalize, clusterNumber, outputFieldName):
    from scipy.cluster.vq import kmeans,vq
    from numpy import array
    fullObjectsList = []
    features = vectorLayer.getFeatures()

    for feature in features:
        fullObjectsList.append([])
        for attribute in attributesList:
            if feature[attribute[0]]:
                fullObjectsList[len(fullObjectsList)-1].append(feature[attribute[0]])
            else:
                fullObjectsList[len(fullObjectsList)-1].append(0)

    #NORMALIZING
    if normalize:
        i = 0
        maxValues = []
        while i < len(attributesList):

            maxValues.append(max(abs(item[i]) for item in fullObjectsList))
            i += 1

        j = 0
        while j < len(fullObjectsList):
            i = 0
            while i < len(fullObjectsList[j]):
                fullObjectsList[j][i] = (fullObjectsList[j][i] * 1.0) / (maxValues[i] * 1.0)
                i += 1
            j += 1

    data = array(fullObjectsList)

    centroids,_ = kmeans(data, clusterNumber, 25)
    idx,_ = vq(data,centroids)
    idx = idx.tolist()
    vectorLayerDataProvider = vectorLayer.dataProvider()

    # Create field of not exist
    if vectorLayer.fieldNameIndex(outputFieldName) == -1:
        vectorLayerDataProvider.addAttributes([QgsField(outputFieldName, QVariant.Int)])

    vectorLayer.updateFields()
    vectorLayer.startEditing()
    attrIdx = vectorLayer.fieldNameIndex(outputFieldName)
    features = vectorLayer.getFeatures()

    i = 0
    for feature in features:
        vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(idx[i]))
        i += 1

    vectorLayer.updateFields()
    vectorLayer.commitChanges()