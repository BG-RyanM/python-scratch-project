import random
import matplotlib.pyplot as plt

xy_list = []


def make_coordinates():
    start_y = random.randrange(100)
    y = start_y
    for x in range(100):
        xy_list.append((x, y))
        y = y + random.randrange(5) - 2
        if y < 0: y = 0
        if y > 99: y = 99

def plot_graph(trend_pts, trend_pts2 = None):
    x_coords = [pair[0] for pair in xy_list]
    y_coords = [pair[1] for pair in xy_list]
    plt.plot(x_coords, y_coords)
    x_coords = [pair[0] for pair in trend_pts]
    y_coords = [pair[1] for pair in trend_pts]
    plt.plot(x_coords, y_coords, "ro")
    if trend_pts2 is not None:
        x_coords = [pair[0] for pair in trend_pts2]
        y_coords = [pair[1] for pair in trend_pts2]
        plt.plot(x_coords, y_coords, "bo")
    plt.show()

def get_trendline(upper, start_x, end_x, min_dist):
    # Returns list
    # end_x is inclusive

    def _get_steepest_target(sx, ex):
        sy = xy_list[sx][1]
        best_x = None
        best_slope = -1000000.0 if upper else 1000000.0
        for x in range(sx+1, ex+1):
            y = xy_list[x][1]
            slope = float((y - sy)) / float((x - sx))
            if upper and slope > best_slope:
                best_x = x
                best_slope = slope
            elif not upper and slope < best_slope:
                best_x = x
                best_slope = slope
        return best_x, xy_list[best_x][1]

    pts_list = []
    coords = (start_x, xy_list[start_x][1])
    while True:
        if coords[0] >= end_x:
            break
        next_coords = _get_steepest_target(coords[0], end_x)
        if next_coords[0] < end_x:
            pts_list.append(next_coords)
        coords = next_coords

    if len(pts_list) <= 1:
        return pts_list

    ret_list = []
    for i, pt in enumerate(pts_list):
        if i == 0:
            continue
        if pts_list[i][0] - pts_list[i-1][0] >= min_dist:
            if pts_list[i-1] not in ret_list:
                ret_list.append(pts_list[i-1])
            if pts_list[i] not in ret_list:
                ret_list.append(pts_list[i])

    return ret_list

make_coordinates()
trend_pts = get_trendline(True, 0, 80, 10)
trend_pts2 = get_trendline(False, 0, 80, 10)
plot_graph(trend_pts, trend_pts2)
