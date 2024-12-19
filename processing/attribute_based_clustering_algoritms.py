# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com
"""

import copy
import math
import numpy as np
from numpy import array
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField, QgsVectorLayer
import processing

def list_of_fields_to_struct(fields_list):
    struct = []
    for field in fields_list:
        struct.append([field,1.0])
    return struct


def normalize_attributes (attributes_list, full_objects_list):
    # full_objects_list is list [[val1, val2, ... valN], ..., [val1, val2, ... valN]]
    i = 0
    max_values = []
    while i < len(attributes_list):
        max_values.append(max(abs(item[i]) for item in full_objects_list))
        i += 1

    j = 0
    while j < len(full_objects_list):
        i = 0
        while i < len(full_objects_list[j]):
            full_objects_list[j][i] = (full_objects_list[j][i] * 1.0) / (max_values[i] * 1.0)
            i += 1
        j += 1
    return full_objects_list

def get_data_for_clustering(vector_layer, attributes_list, normalize):
    full_objects_list = []
    features = vector_layer.getFeatures()

    for feature in features:
        full_objects_list.append([])
        for attribute in attributes_list:
            if feature[attribute[0]]:
                full_objects_list[len(full_objects_list) - 1].append(feature[attribute[0]])
            else:
                full_objects_list[len(full_objects_list) - 1].append(0)
    
    if normalize:
        full_objects_list = normalize_attributes(attributes_list, full_objects_list)

    return array(full_objects_list)

def calculate_distance(a, b, weights):
    sum_sqr = 0
    k = 0

    for i, j in zip(a, b):
        if weights == None:
            sum_sqr += 1.0 * ((float(i) - float(j)) ** 2)
        else:
            sum_sqr += weights[k] * ((float(i) - float(j)) ** 2)
        k += 1
    distance = math.sqrt(sum_sqr)
    return distance

def get_average_of_two(a, b):
        new_object = []
        i = 0
        while i < len(a):
            new_object.append((a[i] + b[i]) / 2.0)
            i += 1
        return new_object

def hierarchical_clustering_native (full_objects_list,
                                    cluster_number,
                                    weights):
    
    cluster_object_list = range(0,len(full_objects_list))
    cluster_object_list = [[i] for i in cluster_object_list]
    
    working_full_objects_list = copy.deepcopy(full_objects_list)
    p = 0

    # Initial distance matrix fill
    distance_matrix = np.zeros((len(working_full_objects_list),len(working_full_objects_list)))
    distance_matrix[:] = np.nan
    i = 0
    while i < len(full_objects_list):
        j = i+1
        while j < len(full_objects_list):
            current_distance = calculate_distance(working_full_objects_list[j], working_full_objects_list[i], weights)
            p+=1

            distance_matrix[i,j] = current_distance
            j+=1
        i += 1
    
    while distance_matrix.shape[0] > cluster_number:
        current_min_distance_idx = np.unravel_index(np.nanargmin(distance_matrix), distance_matrix.shape)

        working_full_objects_list[current_min_distance_idx[0]] = get_average_of_two(working_full_objects_list[current_min_distance_idx[0]],
                                                                                     working_full_objects_list[current_min_distance_idx[1]])

        k = 0
        while k < len(cluster_object_list[current_min_distance_idx[1]]):
            cluster_object_list[current_min_distance_idx[0]].append(cluster_object_list[current_min_distance_idx[1]][k])
            k += 1
        
        del cluster_object_list[current_min_distance_idx[1]]
        working_full_objects_list = np.delete(working_full_objects_list, current_min_distance_idx[1],axis=0)
        # update distance matrix
        # row
        i = current_min_distance_idx[0]
        j = i+1
        while j < len(working_full_objects_list):
            current_distance = calculate_distance(working_full_objects_list[j], working_full_objects_list[i], weights)
            p+=1

            distance_matrix[i,j] = current_distance
            j += 1  

        # col
        j = current_min_distance_idx[0]
        i = 0
        while i < j:
            current_distance = calculate_distance(working_full_objects_list[j], working_full_objects_list[i], weights)
            p+=1

            distance_matrix[i,j] = current_distance
            i += 1

        distance_matrix = np.delete(distance_matrix,current_min_distance_idx[1],axis=0)
        distance_matrix = np.delete(distance_matrix,current_min_distance_idx[1],axis=1)

    centroids = working_full_objects_list    
    idx = []
    for i in range(0,len(full_objects_list)):
        for k in range(0,len(cluster_object_list)):
            if i in cluster_object_list[k]:
                idx.append(k)
                continue

    return idx, centroids

def kmeans_scipy (full_objects_list,
                  cluster_number,
                  iterations,
                  threshold):
    
    from scipy.cluster.vq import kmeans, vq
    
    centroids, _ = kmeans(full_objects_list, cluster_number, iter=iterations, thresh=threshold)
    idx, _ = vq(full_objects_list, centroids)
    idx = idx.tolist()

    return idx, centroids

def kmeans2_scipy (full_objects_list,
                   cluster_number,
                   iterations,
                   method):
    
    from scipy.cluster.vq import kmeans2

    try:
        centroids, labels = kmeans2(full_objects_list, cluster_number, iter=iterations, minit=method)
    except np.linalg.LinAlgError as err:
        centroids, labels = kmeans2(full_objects_list, cluster_number, iter=iterations, minit='points')

    idx = labels.tolist()
    return idx, centroids

def hierarchical_clustering_scipy (full_objects_list,
                                   cluster_threshold,
                                   linkage_method, 
                                   criterion, 
                                   metric, 
                                   depth, 
                                   max_clust):
    
    import scipy.cluster.hierarchy as hcluster
    
    if criterion == 'maxclust':
        clusters = hcluster.fclusterdata(full_objects_list,
                                         t=max_clust,
                                         criterion=criterion,
                                         method=linkage_method,
                                         metric=metric,
                                         depth=depth)
    else:
        clusters = hcluster.fclusterdata(full_objects_list,
                                         t=cluster_threshold,
                                         criterion=criterion,
                                         method=linkage_method,
                                         metric=metric,
                                         depth=depth)

    centroids = list(set(clusters))
    
    return clusters, centroids

# return clusters and metrics
def clustering_with_metrics(vector_layer,
                            attributes_list,
                            normalize,
                            algorithm,
                            parameters,
                            distance_calculation_method):

    full_objects_list = get_data_for_clustering(vector_layer, attributes_list, normalize)

    weights = []
    for attribute in attributes_list:
        weights.append(attribute[1])

    if algorithm == 'kmeans':
        idx, centroids = kmeans_scipy(full_objects_list,
                                      parameters['cluster_number'],
                                      parameters['iterations'],
                                      parameters['threshold'])
        
    if algorithm == 'kmeans2':
        idx, centroids = kmeans2_scipy(full_objects_list,
                                       parameters['cluster_number'],
                                       parameters['iterations'],
                                       parameters['method'])
        
    if algorithm == 'hier2':
        idx, centroids = hierarchical_clustering_scipy(full_objects_list=full_objects_list,
                                                       cluster_threshold=parameters['threshold'],
                                                       linkage_method=parameters['linkage_method'], 
                                                       criterion=parameters['criterion'], 
                                                       metric=parameters['metric'], 
                                                       depth=parameters['depth'], 
                                                       max_clust=parameters['max_clusters'])
    
        return idx, centroids, None, None

    if algorithm == 'hier':
        idx, centroids = hierarchical_clustering_native(full_objects_list=full_objects_list,
                                                        cluster_number=parameters['cluster_number'],
                                                        weights=weights)
    
    distances = []
    sse = 0
    
    if distance_calculation_method == 'disabled':
        pass
    
    elif distance_calculation_method == 'only_object_cluster':

        for i in range(0,len(idx)):
            current_distance = calculate_distance(full_objects_list[i],centroids[int(idx[i])],weights)
            distances.append(current_distance)
            sse += current_distance * current_distance

    elif distance_calculation_method == 'all_clusters':
        for i in range(0,len(idx)):
            current_distances = []
            for j in range (0, parameters['cluster_number']):
                current_distance = calculate_distance(full_objects_list[i],centroids[j],weights)
                if j == int(idx[i]):
                    object_distance = current_distance
                current_distances.append(current_distance)

            distances.append(current_distances)
            sse += object_distance * object_distance
        
    return idx, centroids, distances, sse


# all work with writing results
def perform_clustering (vector_layer,
                        attributes_list,
                        normalize,
                        algorithm,
                        parameters,
                        output_field_name,
                        output_mode,
                        distance_calculation_method = 'disabled', 
                        distance_field_prefix = None,
                        just_error_calculation=False,
                        temporary_file_name=None):

    print (attributes_list)

    idx, centroids, distances, sse = clustering_with_metrics(vector_layer,
                                                             attributes_list,
                                                             normalize,
                                                             algorithm,
                                                             parameters,
                                                             distance_calculation_method=distance_calculation_method)

    if just_error_calculation:
        return sse
    
    if algorithm == 'hier2':
        distance_calculation_method = 'disabled'
    
    clusters_number = len(centroids)
    
    if output_mode == 'source':
        working_layer = vector_layer
    elif output_mode == 'temp':
        # clone layer to memory and work with it
        working_layer = QgsVectorLayer(processing.run("native:savefeatures", {'INPUT': vector_layer, 'OUTPUT': 'TEMPORARY_OUTPUT', 'LAYER_NAME':temporary_file_name})['OUTPUT'],temporary_file_name,'ogr')
    
    working_layer_data_provider = working_layer.dataProvider()
    if working_layer.fields().indexFromName(output_field_name) == -1:
        working_layer_data_provider.addAttributes([QgsField(output_field_name, QVariant.Int)])
        working_layer.updateFields()

    # Create distance fields if needed
    if distance_calculation_method == 'only_object_cluster':
        if working_layer.fields().indexFromName(distance_field_prefix) == -1:
            working_layer_data_provider.addAttributes([QgsField(distance_field_prefix, QVariant.Double)])
        working_layer.updateFields()
        distance_index = working_layer.fields().indexFromName(distance_field_prefix)

    elif distance_calculation_method == 'all_clusters':
        distance_indices = []
        for i in range(0,clusters_number):
            if working_layer.fields().indexFromName(distance_field_prefix+str(i)) == -1:
                working_layer_data_provider.addAttributes([QgsField(distance_field_prefix+str(i), QVariant.Double)])
                working_layer.updateFields()
            distance_indices.append(working_layer.fields().indexFromName(distance_field_prefix+str(i)))

    working_layer.updateFields()
    working_layer.startEditing()
    attrIdx = working_layer.fields().indexFromName(output_field_name)

    features = working_layer.getFeatures()
    i = 0
    for feature in features:
        # class number
        working_layer.changeAttributeValue(feature.id(), attrIdx, int(idx[i]))

        if distance_calculation_method == 'only_object_cluster':
            current_distance = distances[i]
            working_layer.changeAttributeValue(feature.id(), distance_index, current_distance)

        elif distance_calculation_method == 'all_clusters':
            for j in range(0, clusters_number):
                current_distance = distances[i][j]
                working_layer.changeAttributeValue(feature.id(), distance_indices[j], current_distance)
        
        i += 1

    working_layer.updateFields()
    working_layer.commitChanges()
    return working_layer


def draw_elbow_plot(vector_layer,
                    attributes_list,
                    normalize,
                    algorithm,
                    parameters,
                    max_clusters):
    
    import matplotlib.pyplot as plt
    
    cluster_num_list = []
    sse_list = []
    for i in range (1,max_clusters+1):
        parameters['cluster_number'] = i
        sse = perform_clustering(vector_layer=vector_layer,
                                 attributes_list=attributes_list,
                                 normalize=normalize,
                                 algorithm=algorithm,
                                 parameters=parameters,
                                 output_field_name=None,
                                 output_mode=None,
                                 distance_calculation_method = 'only_object_cluster', 
                                 distance_field_prefix = None,
                                 just_error_calculation=True,
                                 temporary_file_name=None)

        cluster_num_list.append(i)
        sse_list.append(sse)
    
    if not len(cluster_num_list) == 0:
        plt.close()
        plt.plot(cluster_num_list, sse_list, 'bx-')
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('Sum of squared errors')
        plt.show()