# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 Attribute based clustering for vector layers by numeric attributes using hierarchical or k-means algorithms (known and unknown number of clusters supported).
                             -------------------
        begin                : 2019-01-01
        copyright            : (C) 2019 by Eduard Kazakov
        email                : silenteddie@gmail.com
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AttributeBasedClustering class from file AttributeBasedClustering.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .attribute_based_clustering import AttributeBasedClustering
    return AttributeBasedClustering(iface)
