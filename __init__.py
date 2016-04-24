# -*- coding: utf-8 -*-

"""
/***************************************************************************
 MinkowskyDimCalculator init
                                 A QGIS plugin
 Plugin calculates Minkowski dimension (also known as Minkowski–Bouligand
 dimension; box-counting dimension) for features of vector layer.

                              -------------------
        begin                : 2015-12-16
        copyright            : (C) 2015 by Eduard Kazakov
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

def classFactory(iface):
    from abc import ABC
    return ABC(iface)
