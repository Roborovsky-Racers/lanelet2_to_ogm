import yaml
from lanelet2.io import Origin
from lanelet2.projection import UtmProjector
from lanelet2.io import load

# マップファイルのパスを指定
map_file = '/aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/map/lanelet2_map.osm'

# 原点とプロジェクションを設定
origin = Origin(35.22312494056, 138.8024583466)  # 緯度と経度
projector = UtmProjector(origin)

# マップをロード
lanelet_map = load(map_file, origin)
lanelet_map = load(map_file, projector)

import lanelet2.projection
import numpy as np
import cv2

# グリッドマップのパラメータ設定
resolution = 0.1  # メートル単位の解像度
map_width = 100  # マップの幅（メートル）
map_height = 100  # マップの高さ（メートル）

# 占有グリッドマップを初期化
occupancy_grid = np.zeros((int(map_height / resolution), int(map_width / resolution)), dtype=np.uint8)

# Lanelet2のレーンレットを取得
lanelets = lanelet_map.laneletLayer


# マップ全体の範囲を取得
min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
for lanelet in lanelets:
    for pt in lanelet.polygon2d():
        min_x = min(min_x, pt.x)
        min_y = min(min_y, pt.y)
        max_x = max(max_x, pt.x)
        max_y = max(max_y, pt.y)

# グリッドマップのサイズをマップ範囲に合わせて調整
grid_width = int((max_x - min_x) / resolution)
grid_height = int((max_y - min_y) / resolution)
occupancy_grid = np.zeros((grid_height, grid_width), dtype=np.uint8)
occupancy_grid_flip = np.zeros((grid_height, grid_width), dtype=np.uint8)

# レーンレットをグリッドマップに変換
for lanelet in lanelets:
    polygon = lanelet.polygon2d()
    pts = []
    for pt in polygon:
        x_pixel = int((pt.x - min_x) / resolution)
        y_pixel = int((pt.y - min_y) / resolution)
        pts.append([x_pixel, y_pixel])
    pts = np.array([pts], dtype=np.int32)
    cv2.fillPoly(occupancy_grid, pts, 255)

# レーンレットをグリッドマップに変換(Y座標を反転)
for lanelet in lanelet_map.laneletLayer:
    polygon = lanelet.polygon2d()
    pts = []
    for pt in polygon:
        x_pixel = int((pt.x - min_x) / resolution)
        y_pixel = grid_height - int((pt.y - min_y) / resolution)  # Y座標を反転
        pts.append([x_pixel, y_pixel])
    pts = np.array([pts], dtype=np.int32)
    cv2.fillPoly(occupancy_grid_flip, pts, 255)

# PGMファイルとして保存
map_filename = 'occupancy_grid_map'
pgm_filename = map_filename + ".pgm"

# pgm では Y軸反転した向きで使用する
cv2.imwrite(pgm_filename, occupancy_grid_flip)
cv2.imwrite(map_filename + ".png", occupancy_grid)

# YAMLファイルの内容を生成
yaml_data = {
    'image': pgm_filename,
    'resolution': resolution,
    'origin': [min_x, min_y, 0.0],
    'negate': 0,
    'occupied_thresh': 0.65,
    'free_thresh': 0.196,
}

# YAMLファイルとして保存
yaml_filename = map_filename + ".yaml"
with open(yaml_filename, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"PGM file saved to {pgm_filename}")
print(f"YAML file saved to {yaml_filename}")