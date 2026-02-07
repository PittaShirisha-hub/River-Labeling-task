import matplotlib.pyplot as plt
from shapely.geometry import Polygon


def visualize_result(polygon, label_point, text, inside=True):
    x, y = polygon.exterior.xy

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, color="blue")
    plt.fill(x, y, alpha=0.3)

    plt.text(
        label_point.x,
        label_point.y,
        text,
        fontsize=12,
        ha="center",
        va="center",
        color="black"
    )

    title = "Label placed inside river" if inside else "Fallback placement"
    plt.title(title)
    plt.axis("equal")
    plt.show()
