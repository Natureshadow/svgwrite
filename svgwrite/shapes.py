#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: svg shapes
# Created: 08.09.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from svgwrite import parameter
from svgwrite.base import BaseElement
from svgwrite.validator import check_coordinate
from svgwrite.utils import points_to_string
from svgwrite.interface import ITransform

class Line(BaseElement, ITransform):
    """ The <line> element defines a line segment that starts at one point and ends
    at another.

    .. automethod:: svgwrite.Line.__init__

    **Supported SVG Attributes**

    * **x1** -- `coordinate` start-x
    * **y1** -- `coordinate` start-y
    * **x2** -- `coordinate` end-x
    * **y2** -- `coordinate` end-y
    """
    elementname = 'line'

    def __init__(self, start=(0, 0), end=(0, 0),
                 attribs=None, **extra):
        """
        :param 2-tuple start: start point (x1, y1)
        :param 2-tuple end: end point (x2, y2)
        :param dict attribs: additional SVG attributes
        :param extra: additional SVG attributs as keyword-arguments

        """
        super(Line, self).__init__(attribs=attribs, **extra)
        profile = parameter.profile
        x1, y1 = start
        x2, y2 = end
        self.attribs['x1'] = check_coordinate(x1, profile)
        self.attribs['y1'] = check_coordinate(y1, profile)
        self.attribs['x2'] = check_coordinate(x2, profile)
        self.attribs['y2'] = check_coordinate(y2, profile)

class Rect(BaseElement, ITransform):
    """ The <rect> element defines a rectangle which is axis-aligned with the current
    user coordinate system. Rounded rectangles can be achieved by setting appropriate
    values for attributes <rx> and <ry>.

    .. automethod:: svgwrite.Rect.__init__

    **Supported SVG Attributes**

    * **x** -- `coordinate` The x-axis coordinate of the side of the
               rectangle which has the smaller x-axis coordinate value
    * **y** -- `coordinate` The y-axis coordinate of the side of the
               rectangle which has the smaller y-axis coordinate value
    * **width** -- `lenght`
    * **height** -- `lenght`
    * **rx** -- `length` For rounded rectangles, the y-axis radius of the
                ellipse used to round off the corners of the rectangle.
    * **ry** -- `length` For rounded rectangles, the y-axis radius of the
                ellipse used to round off the corners of the rectangle.
    """
    elementname = 'rect'

    def __init__(self, insert=(0, 0), size=(1, 1), rx=None, ry=None,
                 attribs=None, **extra):
        """
        :param 2-tuple insert: insert point (x, y), left-upper point
        :param 2-tuple size: width, height
        :param length rx: corner x-radius
        :param length ry: corner y-radius
        :param dict attribs: additional SVG attributes
        :param extra: additional SVG attributs as keyword-arguments

        """
        super(Rect, self).__init__(attribs=attribs, **extra)

        profile = parameter.profile
        x, y = insert
        width, height = size
        self.attribs['x'] = check_coordinate(x, profile)
        self.attribs['y'] = check_coordinate(y, profile)
        self.attribs['width'] = check_coordinate(width, profile)
        self.attribs['height'] = check_coordinate(height, profile)
        if rx: self.attribs['rx'] = check_coordinate(rx, profile)
        if ry: self.attribs['ry'] = check_coordinate(ry, profile)

class Circle(BaseElement, ITransform):
    """ The <circle> element defines a circle based on a center point and a radius.

    .. automethod:: svgwrite.Circle.__init__

    **Supported SVG Attributes**

    * **cx** -- `coordinate` The x-axis coordinate of the center of the circle.
    * **cy** -- `coordinate` The y-axis coordinate of the center of the circle.
    * **r** -- `length` The radius of the circle.
    """
    elementname = 'circle'

    def __init__(self, center=(0, 0), r=1, attribs=None, **extra):
        """
        :param 2-tuple center: circle center point (cx, cy)
        :param length r: circle-radius r
        :param dict attribs: additional SVG attributes
        :param extra: additional SVG attributs as keyword-arguments

        """
        super(Circle, self).__init__(attribs=attribs, **extra)
        profile = parameter.profile
        cx, cy = center
        self.attribs['cx'] = check_coordinate(cx, profile)
        self.attribs['cy'] = check_coordinate(cy, profile)
        self.attribs['r'] = check_coordinate(r, profile)



class Ellipse(BaseElement, ITransform):
    """ The <ellipse> element defines an ellipse which is axis-aligned with the
    current user coordinate system based on a center point and two radii.

    .. automethod:: svgwrite.Ellipse.__init__

    **Supported SVG Attributes**

    * **cx** -- `coordinate` The x-axis coordinate of the center of the ellipse.
    * **cy** -- `coordinate` The y-axis coordinate of the center of the ellipse.
    * **rx** -- `length` The x-axis radius of the ellipse.
    * **ry** -- `length` The y-axis radius of the ellipse.
    """
    elementname = 'ellipse'

    def __init__(self, center=(0, 0), r=(1, 1), attribs=None, **extra):
        """
        :param 2-tuple center: ellipse center point (cx, cy)
        :param 2-tuple r: ellipse radii (rx, ry)
        :param dict attribs: additional SVG attributes
        :param extra: additional SVG attributs as keyword-arguments

        """
        super(Ellipse, self).__init__(attribs=attribs, **extra)
        profile = parameter.profile
        cx, cy = center
        rx, ry = r
        self.attribs['cx'] = check_coordinate(cx, profile)
        self.attribs['cy'] = check_coordinate(cy, profile)
        self.attribs['rx'] = check_coordinate(rx, profile)
        self.attribs['ry'] = check_coordinate(ry, profile)

class Polyline(BaseElement, ITransform):
    """ The <polyline> element defines a set of connected straight line segments.
    Typically, <polyline> elements define open shapes.

    .. automethod:: svgwrite.Polyline.__init__

    **Attributes**

    .. attribute:: Polyline.points

       *list* of points, a point is a <2-tuple> (x, y): x, y = <number>

    **Supported SVG Attributes**

    * **points** -- <list-of-points> The points that make up the polyline.
       All coordinate values are in the **user coordinate system** (no units
       allowed).

    How to append points::

        Polyline.points.append( point )
        Polyline.points.extend( [point1, point2, point3, ...] )
    """
    elementname = 'polyline'

    def __init__(self, points=[], attribs=None, **extra):
        """
        :param `iterable` points: of points and points are <2-tuple>s
        :param dict attribs: additional SVG attributes
        :param extra: additional SVG attributs as keyword-arguments

        """
        super(Polyline, self).__init__(attribs=attribs, **extra)
        if parameter.debug:
            for point in points:
                x, y = point
                check_coordinate(x, parameter.profile)
                check_coordinate(y, parameter.profile)
        self.points = list(points)

    def get_xml(self):
        self.attribs['points'] = points_to_string(self.points)
        return super(Polyline, self).get_xml()

class Polygon(Polyline):
    """ The <polygon> element defines a closed shape consisting of a set of connected
    straight line segments.

    Same as :class:`~svgwrite.shapes.Polyline` but closed.
    """
    elementname = 'polygon'
