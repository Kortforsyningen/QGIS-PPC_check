# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PPC_check
                                 A QGIS plugin
 Tool for checking PPC files
                             -------------------
        begin                : 2016-03-08
        copyright            : (C) 2016 by www.sdfe.dk
        email                : anfla@sdfe.dk, mafal@sdfe.dk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PPC_check class from file PPC_check.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PPC_check import PPC_check
    return PPC_check(iface)
