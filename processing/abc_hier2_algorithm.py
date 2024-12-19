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

class ABCHier2Algorithm(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    MAXCLUSTERS = "MAXCLUSTERS"
    THRESHOLD = 'THRESHOLD'
    
    CRITERION = 'CRITERION'
    criterion_options = ["inconsistent", "distance", "maxclust"]
    
    METRIC = "METRIC"
    metric_options = ["euclidean","minkowski","cityblock","seuclidean","sqeuclidean","cosine","correlation","hamming","jaccard","chebyshev","canberra","braycurtis","mahalanobis","matching","dice","kulsinski","rogerstanimoto","russellrao","sokalmichener","sokalsneath"]
    
    DEPTH = "DEPTH"

    LINKAGE = "LINKAGE"
    linkage_options = ["single","complete","average","median","weighted","ward","centroid"]

    NORMALIZE = 'NORMALIZE'
    FIELDS = 'FIELDS'
    OUTPUT_FIELD_NAME = 'OUTPUT_FIELD_NAME'
    CENTROID_DISTANCES_MODE = 'CENTROID_DISTANCE_MODE'
    CENTROID_DISTANCES_PREFIX = 'CENTROID_DISTANCES_PREFIX'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return ABCHier2Algorithm()

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
                self.THRESHOLD,
                "Clustering threshold",
                type=QgsProcessingParameterNumber.Double,
                minValue=0.001,
                defaultValue = 0.3
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.MAXCLUSTERS,
                "Max number of clusters",
                type=QgsProcessingParameterNumber.Integer,
                minValue=0,
                defaultValue = 0
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.CRITERION,
                "Criterion",
                options=self.criterion_options,
                defaultValue=1
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METRIC,
                "Metric",
                options=self.metric_options,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.DEPTH,
                "Depth",
                type=QgsProcessingParameterNumber.Integer,
                minValue=1,
                defaultValue = 2
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.LINKAGE,
                "Linkage method",
                options=self.linkage_options,
                defaultValue=2
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

        maxclusters = self.parameterAsInt(
            parameters,
            self.MAXCLUSTERS,
            context
        )

        depth = self.parameterAsInt(
            parameters,
            self.DEPTH,
            context
        )

        threshold = self.parameterAsDouble(
            parameters,
            self.THRESHOLD,
            context
        )

        criterion = self.parameterAsEnum(
            parameters,
            self.CRITERION,
            context
        )
        criterion = self.criterion_options[criterion]

        metric = self.parameterAsEnum(
            parameters,
            self.METRIC,
            context
        )
        metric = self.metric_options[metric]

        linkage_method = self.parameterAsEnum(
            parameters,
            self.LINKAGE,
            context
        )
        linkage_method = self.linkage_options[linkage_method]

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
        
        run_parameters = {'threshold': threshold,
                          'max_clusters': maxclusters,
                          'depth': depth,
                          'linkage_method': linkage_method,
                          'criterion': criterion,
                          'metric': metric}
        
        clustered_layer = perform_clustering(vector_layer=vector_layer,
                                             attributes_list=attributes_list,
                                             normalize=normalize,
                                             algorithm='hier2',
                                             parameters=run_parameters,
                                             output_field_name=output_field_name,
                                             output_mode='temp',
                                             distance_calculation_method='disable',
                                             distance_field_prefix='',
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
        return "abc_hier2_algorithm"

    def displayName(self):
        return "Hierarchical clustering 2 — unknown number of clusters (ABC)"

    def shortHelpString(self):
        help_string = (
            'Attribute based clustering using Hirarchical algorithm 2 (scipy based)\n\n'
            'Categorizes layer objects based on a specified set of attributes. Objects that are closer to each other based on the set of values of all attributes will be categorized into the same cluster.\n'
            'Number of clusters determined automatically in this algorithm\n'
            '<i>Input layer</i> — vector layer to be clustered, any type of geometry, any source\n'
            '<i>Fields to use for clustering</i> — these attributes would be used to calculate clusters\n'
            '<i>Clustering threshold</i>, <i>Max number of clusters</i>, <i>Criterion</i>, <i>Metric</i>, <i>Depth</i>, <i>Linkage method</i> — algorithm hyperparameters\n'
            '<i>Normalize attribute values</i> — if set, original values of each attribute would be recalculated to 0 - 1 range. Crucial if attributes contain uncomparable units\n'
            '<i>Output field with cluster number</i> — name of new field containing number of cluster for each feature\n'
            'Scipy documentation: <a href=https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fclusterdata.html#scipy.cluster.hierarchy.fclusterdata>https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fclusterdata.html#scipy.cluster.hierarchy.fclusterdata</a>'
        )
        return help_string
