import matplotlib.pyplot as plt
from shapely.geometry import (
    LineString,
    MultiLineString,
    Point,
    MultiPoint,
    Polygon,
    MultiPolygon,
)
from typing import Union, List
from mpl_toolkits.mplot3d import Axes3D


def show_linestrings(
    *linestrings: Union[LineString, MultiLineString, List[LineString]]
) -> None:
    """
    matplotlib을 사용하여 LineString, MultiLineString 또는 LineString의 리스트를 시각화합니다.

    매개변수:
    linestrings: LineString, MultiLineString, 또는 LineString의 리스트
        시각화할 linestring 기하학입니다.
    """
    fig, ax = plt.subplots()
    for linestring in linestrings:
        if isinstance(linestring, LineString):
            x, y = linestring.xy
            ax.plot(x, y, color="black")
        elif isinstance(linestring, MultiLineString) or isinstance(linestring, list):
            for line in linestring:
                x, y = line.xy
                ax.plot(x, y, color="black")
    ax.set_aspect("equal", "datalim")
    plt.show()


def show_points(*points: Union[Point, MultiPoint, List[Point]]) -> None:
    """
    matplotlib을 사용하여 Point, MultiPoint 또는 Point의 리스트를 시각화합니다.

    매개변수:
    points: Point, MultiPoint, 또는 Point의 리스트
        시각화할 point 기하학입니다.
    """
    fig, ax = plt.subplots()
    for point in points:
        if isinstance(point, Point):
            ax.plot(point.x, point.y, "ro")  # 'ro'는 빨간색 원형 마커를 의미합니다.
        elif isinstance(point, MultiPoint) or isinstance(point, list):
            for pt in point:
                ax.plot(pt.x, pt.y, "ro")
    ax.set_aspect("equal", "datalim")
    plt.show()


def show_polygons(*polygons: Union[Polygon, MultiPolygon, List[Polygon]]) -> None:
    """
    matplotlib을 사용하여 Polygon, MultiPolygon 또는 Polygon의 리스트를 시각화합니다.

    매개변수:
    polygons: Polygon, MultiPolygon, 또는 Polygon의 리스트
        시각화할 polygon 기하학입니다.
    """
    fig, ax = plt.subplots()
    for polygon in polygons:
        if isinstance(polygon, Polygon):
            x, y = polygon.exterior.xy
            ax.fill(x, y, color="green", alpha=0.5)
        elif isinstance(polygon, MultiPolygon) or isinstance(polygon, list):
            for poly in polygon:
                x, y = poly.exterior.xy
                ax.fill(x, y, color="green", alpha=0.5)
    ax.set_aspect("equal", "datalim")
    plt.show()


def show_geoms(geometries: List[Union[Point, LineString, Polygon]]) -> None:
    """
    matplotlib을 사용하여 각 유형에 대해 특정 색상으로 기하학의 리스트를 시각화합니다.

    매개변수:
    geometries: 기하학의 리스트
        시각화할 기하학입니다. 점은 빨간색, 선은 검은색, 다각형은 알파 0.5의 녹색입니다.
    """
    fig, ax = plt.subplots()
    for geom in geometries:
        if isinstance(geom, Point):
            ax.plot(geom.x, geom.y, "ro")  # 점은 빨간색
        elif isinstance(geom, LineString):
            x, y = geom.xy
            ax.plot(x, y, color="black")  # 선은 검은색
        elif isinstance(geom, Polygon):
            x, y = geom.exterior.xy
            ax.fill(x, y, color="green", alpha=0.5)  # 다각형은 알파 0.5의 녹색
    ax.set_aspect("equal", "datalim")
    plt.show()


def show_polygons_Z(*polygons: Union[Polygon, MultiPolygon, List[Polygon]]) -> None:
    """
    matplotlib을 사용하여 Z 값을 가진 3D 다각형을 시각화합니다.

    매개변수:
    polygons: Polygon, MultiPolygon, 또는 Polygon의 리스트
        시각화할 3D 다각형 기하학입니다.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    for polygon in polygons:
        if isinstance(polygon, Polygon):
            x, y, z = (
                polygon.exterior.xy[0],
                polygon.exterior.xy[1],
                polygon.exterior.xy[2],
            )
            ax.plot_trisurf(x, y, z, color="green", alpha=0.5)
        elif isinstance(polygon, MultiPolygon) or isinstance(polygon, list):
            for poly in polygon:
                x, y, z = poly.exterior.xy[0], poly.exterior.xy[1], poly.exterior.xy[2]
                ax.plot_trisurf(x, y, z, color="green", alpha=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
