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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


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

    제한: MultiPoint/MultiLineString/MultiPolygon은 지원하지 않는다. 필요 시
    call-site에서 적절히 분해하여 전달할 것.

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

    xs_all: List[float] = []
    ys_all: List[float] = []
    zs_all: List[float] = []

    def _add_polygon_3d(poly: Polygon) -> None:
        """Polygon(exterior.coords)의 (x,y,z) 좌표를 사용해 3D 면을 추가한다."""
        # shapely 3D 좌표는 exterior.coords에서 (x, y, z) 형태로 접근한다.
        coords = list(poly.exterior.coords)
        verts = []
        for c in coords:
            if len(c) >= 3:
                x, y, z = c[0], c[1], c[2]
            else:
                x, y, z = c[0], c[1], 0.0
            verts.append((x, y, z))
            xs_all.append(x)
            ys_all.append(y)
            zs_all.append(z)

        collection = Poly3DCollection(
            [verts], facecolors="green", edgecolors="black", alpha=0.5
        )
        ax.add_collection3d(collection)

    for item in polygons:
        if isinstance(item, Polygon):
            _add_polygon_3d(item)
        elif isinstance(item, MultiPolygon):
            for poly in item.geoms:
                _add_polygon_3d(poly)
        elif isinstance(item, list):
            for poly in item:
                _add_polygon_3d(poly)

    if xs_all and ys_all and zs_all:
        # 축 같은 비율 유지: 전체 범위에서 가장 긴 길이를 기준으로 큐브 범위 설정
        x_min, x_max = min(xs_all), max(xs_all)
        y_min, y_max = min(ys_all), max(ys_all)
        z_min, z_max = min(zs_all), max(zs_all)

        x_mid = 0.5 * (x_min + x_max)
        y_mid = 0.5 * (y_min + y_max)
        z_mid = 0.5 * (z_min + z_max)

        x_range = x_max - x_min
        y_range = y_max - y_min
        z_range = z_max - z_min
        max_range = max(x_range, y_range, z_range, 1e-9)

        half = 0.5 * max_range
        ax.set_xlim(x_mid - half, x_mid + half)
        ax.set_ylim(y_mid - half, y_mid + half)
        ax.set_zlim(z_mid - half, z_mid + half)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
