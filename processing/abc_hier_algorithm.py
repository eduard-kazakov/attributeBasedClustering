# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com
"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterField,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFeatureSink,
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingException
)

from .attribute_based_clustering_algoritms import perform_clustering

class ABCHierAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    CLUSTER_NUMBER = 'CLUSTER_NUMBER'
    NORMALIZE = 'NORMALIZE'
    FIELDS = 'FIELDS'
    WEIGHTS = 'WEIGHTS'
    OUTPUT_FIELD_NAME = 'OUTPUT_FIELD_NAME'
    CENTROID_DISTANCES_MODE = 'CENTROID_DISTANCE_MODE'
    CENTROID_DISTANCES_PREFIX = 'CENTROID_DISTANCES_PREFIX'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return ABCHierAlgorithm()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                "Input layer",
                types=[QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELDS,
                "Fields to use for clustering",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
                allowMultiple=True
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.WEIGHTS,
                "Weights of fields (float numbers divided with ;). Leave empty to ignore weights",
                defaultValue='',
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CLUSTER_NUMBER,
                "Number of clusters",
                type=QgsProcessingParameterNumber.Integer,
                minValue=2,
                defaultValue = 5
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.NORMALIZE,
                "Normalize attribute values",
                defaultValue = True
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_FIELD_NAME,
                "Output field with cluster number",
                defaultValue='class'
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.CENTROID_DISTANCES_MODE,
                "Centroid distances calculation mode",
                options=["Do not calculate", "To objects class centroid", "To all centroids"],
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.CENTROID_DISTANCES_PREFIX,
                "Prefix for fields with distances",
                defaultValue='dist_'
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Clustered layer"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        vector_layer = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )

        if vector_layer.featureCount() == 0:
            raise QgsProcessingException("The input layer is empty. Please provide a non-empty layer.")

        fields = self.parameterAsFields(
            parameters,
            self.FIELDS, 
            context
        )

        weights = self.parameterAsString(
            parameters,
            self.WEIGHTS, 
            context
        )

        weights_list = []
        if not weights:
            for field in fields:
                weights_list.append(1.0)
        else:
            try:
                raw_weights = weights.replace(' ','').split(';')
                for weight in raw_weights:
                    weights_list.append(float(weight))
            except:
                raise QgsProcessingException("Error while processing weights. Weights shoud be float numbers divided by ;")
            
            if len(weights_list) != len(fields):
                raise QgsProcessingException("Number of weights should be equal to number of fields")
        
        attributes_list = [[x, y] for x, y in zip(fields, weights_list)]

        cluster_number = self.parameterAsInt(
            parameters,
            self.CLUSTER_NUMBER,
            context
        )

        normalize = self.parameterAsBoolean(
            parameters,
            self.NORMALIZE,
            context
        )

        output_field_name = self.parameterAsString(
            parameters, 
            self.OUTPUT_FIELD_NAME, 
            context
        )

        centroid_distances_mode = self.parameterAsEnum(
            parameters,
            self.CENTROID_DISTANCES_MODE,
            context
        )

        if centroid_distances_mode == 0:
            distance_calculation_method = 'disabled'
        if centroid_distances_mode == 1:
            distance_calculation_method = 'only_object_cluster'
        if centroid_distances_mode == 2:
            distance_calculation_method = 'all_clusters'

        distance_field_prefix = self.parameterAsString(
            parameters,
            self.CENTROID_DISTANCES_PREFIX,
            context
        )
        
        run_parameters = {
                          'cluster_number': cluster_number
            }
        
        clustered_layer = perform_clustering(vector_layer=vector_layer,
                                             attributes_list=attributes_list,
                                             normalize=normalize,
                                             algorithm='hier',
                                             parameters=run_parameters,
                                             output_field_name=output_field_name,
                                             output_mode='temp',
                                             distance_calculation_method=distance_calculation_method,
                                             distance_field_prefix=distance_field_prefix,
                                             just_error_calculation=False,
                                             temporary_file_name='Clustered')
        
        (sink, sink_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            clustered_layer.fields(), clustered_layer.wkbType(), clustered_layer.crs()
        )

        for feature in clustered_layer.getFeatures():
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: sink_id}

    def name(self):
        return "abc_hier_algorithm"

    def displayName(self):
        return "Hierarchical clustering — known number of clusters (ABC)"

    def shortHelpString(self):
        help_string = (
            'Attribute based clustering using Hirarchical algorithm (native realization)\n\n'
            'Categorizes layer objects based on a specified set of attributes. Objects that are closer to each other based on the set of values of all attributes will be categorized into the same cluster.\n'
            '<i>Input layer</i> — vector layer to be clustered, any type of geometry, any source\n'
            '<i>Fields to use for clustering</i> — these attributes would be used to calculate clusters\n'
            '<i>Weights of fields</i> — list of float numbers divided by semicolon (;). Number of weights should be equal to number of used fields. Example for three fields: <b>1.0;1.5;1.3</b>. Leave empty to use default weights (1.0 fo each field) \n'
            '<i>Number of clusters</i> — how many clusters to divide layer features into\n'
            '<i>Normalize attribute values</i> — if set, original values of each attribute would be recalculated to 0 - 1 range. Crucial if attributes contain uncomparable units\n'
            '<i>Output field with cluster number</i> — name of new field containing number of cluster for each feature\n'
            '<i>Centroid distances calculation mode</i> — this tool could calculate distances for clusters centroids for each feature. It could be very helpful to determine confidence and uncertainty of clustering in each particular case\n'
            '   - Do not calculate: do not calculate distance to centroids\n'
            '   - To objects class centroid: for each feature calculate only distance to the cluster centroid to which it belongs\n'
            '   - To all centroids: for each feature calculate distances to the all cluster centroids\n'
            '<i>Prefix for fields with distances</i> — field name prefix for calculated distances to cluster centroids. Not used if _Do not calculate_ mode is set\n\n'
        )
        return help_string
