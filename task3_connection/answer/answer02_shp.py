from typing import List
from shapely.geometry import LineString, MultiLineString
import geopandas as gpd


def _read_shp_lines(shp_path: str) -> List[LineString]:
    """
    geopandas를 사용해 SHP에서 등고선(LineString)만 추출한다.
    MultiLineString은 개별 LineString으로 분해한다.
    """
    gdf = gpd.read_file(shp_path)
    contours: List[LineString] = []
    for geom in gdf.geometry.tolist():
        if geom is None:
            continue
        if isinstance(geom, LineString):
            contours.append(geom)
        elif isinstance(geom, MultiLineString):
            contours.extend(list(geom.geoms))
    return contours


def task(shp_path: str) -> List[LineString]:
    return _read_shp_lines(shp_path)


if __name__ == "__main__":
    # 예시: 실제 파일명으로 교체해서 사용
    shp_path = "task3_connection/input/N3L_F0010000.shp"
    contours = task(shp_path)

    from utils._viauslize_utils import show_linestrings

    show_linestrings(contours)
