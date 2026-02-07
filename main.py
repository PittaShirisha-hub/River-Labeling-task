from shapely import wkt
from label_placement import place_river_label
from visualize import visualize_result


# Example river geometry (simple curved river polygon)
river_wkt = """
POLYGON ((
0 0, 100 20, 200 40, 300 30, 400 20,
400 60, 300 80, 200 90, 100 70, 0 50, 0 0
))
"""

TEXT = "ELBE"
FONT_SIZE = 12

label_point, placed_inside = place_river_label(
    river_wkt,
    TEXT,
    FONT_SIZE
)

river_polygon = wkt.loads(river_wkt)

visualize_result(
    river_polygon,
    label_point,
    TEXT,
    placed_inside
)
