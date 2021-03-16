# -*- coding: utf-8 -*-
"""
Attribute based clustering: QGIS Plugin

https://github.com/eduard-kazakov/attributeBasedClustering

Eduard Kazakov | ee.kazakov@gmail.com
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AttributeBasedClustering class from file AttributeBasedClustering.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .attribute_based_clustering import AttributeBasedClustering
    return AttributeBasedClustering(iface)
