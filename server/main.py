# import geopandas as gpd

# # 世界地図データの読み込み
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# import matplotlib.pyplot as plt

# # 地図の描画
# world.plot()

# # 表示のための設定
# plt.title("World Map")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.show()

from fastapi import FastAPI
import geopandas as gpd
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from shapely.geometry import Point

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可（本番環境では適切に設定）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-geojson")
async def get_geojson():
    # GeoPandasでデータを読み込む
    gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # 新しいピン（ポイント）の作成
    # 例: 東京の座標 (経度: 139.6917, 緯度: 35.6895)
    new_point = gpd.GeoDataFrame(geometry=[Point(139.6917, 35.6895)], crs="EPSG:4326")

    # 新しいポイントをデータフレームに追加
    gdf = gdf._append(new_point, ignore_index=True)

    # GeoJSON形式に変換
    geojson = gdf.to_json()

    return Response(content=geojson, media_type="application/json")