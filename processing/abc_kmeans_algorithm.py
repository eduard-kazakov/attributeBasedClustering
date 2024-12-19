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

from .attribute_based_clustering_algoritms import list_of_fields_to_struct, perform_clustering

class ABCKMeansAlgorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    CLUSTER_NUMBER = 'CLUSTER_NUMBER'
    ITER = 'ITER'
    THRESHOLD = 'THRESHOLD'
    NORMALIZE = 'NORMALIZE'
    FIELDS = 'FIELDS'
    OUTPUT_FIELD_NAME = 'OUTPUT_FIELD_NAME'
    CENTROID_DISTANCES_MODE = 'CENTROID_DISTANCE_MODE'
    CENTROID_DISTANCES_PREFIX = 'CENTROID_DISTANCES_PREFIX'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return ABCKMeansAlgorithm()

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
            QgsProcessingParameterNumber(
                self.CLUSTER_NUMBER,
                "Number of clusters",
                type=QgsProcessingParameterNumber.Integer,
                minValue=2,
                defaultValue = 5
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ITER,
                "The number of times to run K-Means",
                type=QgsProcessingParameterNumber.Integer,
                minValue=1,
                defaultValue = 20
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.THRESHOLD,
                "Threshold",
                type=QgsProcessingParameterNumber.Double,
                minValue=0.000001,
                defaultValue = 0.00001
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

        cluster_number = self.parameterAsInt(
            parameters,
            self.CLUSTER_NUMBER,
            context
        )

        iter = self.parameterAsInt(
            parameters,
            self.ITER,
            context
        )

        threshold = self.parameterAsDouble(
            parameters,
            self.THRESHOLD,
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
        
        attributes_list = list_of_fields_to_struct(fields)
        run_parameters = {
                          'cluster_number': cluster_number,
                          'iterations': iter,
                          'threshold': threshold
            }
        
        clustered_layer = perform_clustering(vector_layer=vector_layer,
                                             attributes_list=attributes_list,
                                             normalize=normalize,
                                             algorithm='kmeans',
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
        return "abc_kmeans_algorithm"

    def displayName(self):
        return "K-Means clustering (ABC)"

    def shortHelpString(self):
        help_string = (
            'Attribute based clustering using K-Means algorithm (scipy based)\n\n'
            'Categorizes layer objects based on a specified set of attributes. Objects that are closer to each other based on the set of values of all attributes will be categorized into the same cluster.\n'
            '<i>Input layer</i> — vector layer to be clustered, any type of geometry, any source\n'
            '<i>Fields to use for clustering</i> — these attributes would be used to calculate clusters\n'
            '<i>Number of clusters</i> — how many clusters to divide layer features into\n'
            '<i>The number of times to run K-Means</i> and <i>Threshold</i> — algorithm hyperparameters\n'
            '<i>Normalize attribute values</i> — if set, original values of each attribute would be recalculated to 0 - 1 range. Crucial if attributes contain uncomparable units\n'
            '<i>Output field with cluster number</i> — name of new field containing number of cluster for each feature\n'
            '<i>Centroid distances calculation mode</i> — this tool could calculate distances for clusters centroids for each feature. It could be very helpful to determine confidence and uncertainty of clustering in each particular case\n'
            '   - Do not calculate: do not calculate distance to centroids\n'
            '   - To objects class centroid: for each feature calculate only distance to the cluster centroid to which it belongs\n'
            '   - To all centroids: for each feature calculate distances to the all cluster centroids\n'
            '<i>Prefix for fields with distances</i> — field name prefix for calculated distances to cluster centroids. Not used if _Do not calculate_ mode is set\n\n'
            'Scipy documentation: <a href=https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html>https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html</a>'
        )
        return help_string
