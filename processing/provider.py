# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com
"""

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .abc_kmeans_algorithm import ABCKMeansAlgorithm
from .abc_kmeans2_algorithm import ABCKMeans2Algorithm
from .abc_hier_algorithm import ABCHierAlgorithm
from .abc_hier2_algorithm import ABCHier2Algorithm
import os

class AttributeBasedClusteringProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        """Add your algorithms here"""
        self.addAlgorithm(ABCKMeansAlgorithm())
        self.addAlgorithm(ABCKMeans2Algorithm())
        self.addAlgorithm(ABCHierAlgorithm())
        self.addAlgorithm(ABCHier2Algorithm())

    def id(self):
        """Unique identifier for the provider"""
        return "attribute_based_clustering_provider"

    def name(self):
        """Display name in the Processing Toolbox"""
        return "Attribute based clustering"

    def longName(self):
        """Longer display name"""
        return "Attribute based clustering"
    
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), '../icon.png'))