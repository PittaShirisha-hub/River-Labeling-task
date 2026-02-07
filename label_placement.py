from shapely import wkt
from shapely.geometry import Point, box
import math


def estimate_text_box(text, font_size):
    """
    Rough estimation of text bounding box (in points).
    """
    width = font_size * 0.6 * len(text)
    height = font_size
    return width, height


def generate_candidate_points(polygon, step=10):
    """
    Generate grid-based candidate points inside polygon.
    """
    minx, miny, maxx, maxy = polygon.bounds
    points = []

    x = minx
    while x < maxx:
        y = miny
        while y < maxy:
            p = Point(x, y)
            if polygon.contains(p):
                points.append(p)
            y += step
        x += step

    return points


def local_width(polygon, point, radius=20):
    """
    Approximate local river width by intersecting a small circle.
    """
    circle = point.buffer(radius)
    intersection = polygon.intersection(circle)
    return intersection.area


def place_river_label(wkt_geom, text, font_size):
    """
    Main river labeling function.
    """
    river = wkt.loads(wkt_geom)

    # Ensure polygon or multipolygon
    if river.geom_type == "MultiPolygon":
        polygons = list(river.geoms)
    else:
        polygons = [river]

    text_width, text_height = estimate_text_box(text, font_size)
    best_candidate = None
    best_score = -1

    for poly in polygons:
        # Safe zone with padding
        safe_zone = poly.buffer(-font_size * 0.6)
        if safe_zone.is_empty:
            continue

        candidates = generate_candidate_points(safe_zone)

        for point in candidates:
            # Create text bounding box
            text_box = box(
                point.x - text_width / 2,
                point.y - text_height / 2,
                point.x + text_width / 2,
                point.y + text_height / 2
            )

            if safe_zone.contains(text_box):
                score = local_width(poly, point)
                if score > best_score:
                    best_score = score
                    best_candidate = point

    # Fallback: centroid
    if best_candidate is None:
        return river.centroid, False

    return best_candidate, True
