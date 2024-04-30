# from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
# from src.settings.database import Base


# class FlightDetails(Base):
#     """
#     ロケットフライトに関連する情報を格納するテーブル

#     Attributes:
#         flight_id (Integer): フライトの一意識別子であり、プライマリキー
#         rocket_type (String): 使用されるロケットの型式またはモデル
#         launch_datetime (DateTime): フライトの打ち上げ日時
#         mission_end_datetime (DateTime): ミッションの終了予定日時
#         launch_site (String): フライトの打ち上げ場所
#         payload (Text): フライトによって運ばれるペイロードの詳細
#         orbit (String): ペイロードが投入される予定の軌道
#         mission_objective (Text): フライトの目的
#         launch_outcome (String): フライトの結果（成功または失敗）
#         launch_window_start (DateTime): 打ち上げウィンドウの開始時間
#         launch_window_end (DateTime): 打ち上げウィンドウの終了時間
#         payload_mass (Float): ペイロードの質量
#         target_periapsis (Float): 目標とする近地点の高度
#         target_apoapsis (Float): 目標とする遠地点の高度
#         orbit_inc (Float): 目標とする軌道の傾斜角
#         max_q_altitude (Float): 最大動圧を受ける高度
#     """

#     __tablename__ = "flight_details"

#     flight_id = Column(Integer, primary_key=True, index=True)
#     rocket_type = Column(String)
#     launch_datetime = Column(DateTime)
#     mission_end_datetime = Column(DateTime)
#     launch_site = Column(String)
#     payload = Column(Text)
#     orbit = Column(String)
#     mission_objective = Column(Text)
#     launch_outcome = Column(String)
#     launch_window_start = Column(DateTime)
#     launch_window_end = Column(DateTime)
#     payload_mass = Column(Float)
#     target_periapsis = Column(Float)
#     target_apoapsis = Column(Float)
#     target_orbit_inc = Column(Float)
#     target_orbit_speed = Column(Float)
#     max_q_altitude = Column(Float)


# class FlightEventLog(Base):
#     """
#     フライトイベントの記録を格納するテーブル

#     Attributes:
#         log_id (Integer): ログの一意識別子であり、プライマリキー
#         flight_id (Integer): 関連するフライトのID、外部キー
#         event_time (DateTime): イベント発生時刻
#         event_type (String): イベントのタイプ
#         event_details (Text): イベントの詳細情報
#         altitude (Float): イベント発生時の高度
#         latitude (Float): イベント発生時の緯度
#         longitude (Float): イベント発生時の経度
#         orbital_speed (Float): イベント発生時の軌道速度
#         apoapsis_altitude (Float): イベント発生時の遠地点の高度
#         periapsis_altitude (Float): イベント発生時の近地点の高度
#         inclination (Float): イベント発生時の軌道傾斜角
#         eccentricity (Float): イベント発生時の軌道離心率
#     """

#     __tablename__ = "flight_event_logs"

#     log_id = Column(Integer, primary_key=True)
#     flight_id = Column(Integer, ForeignKey("flight_details.flight_id"))
#     event_time = Column(DateTime)
#     event_type = Column(String)
#     event_details = Column(Text)
#     altitude = Column(Float)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     orbital_speed = Column(Float)
#     apoapsis_altitude = Column(Float)
#     periapsis_altitude = Column(Float)
#     inclination = Column(Float)
#     eccentricity = Column(Float)


# class FlightEventPlan(Base):
#     """
#     フライトイベント計画を格納するテーブル

#     Attributes:
#         plan_event_id (Integer): イベント計画の一意識別子であり、プライマリキー
#         flight_id (Integer): 関連するフライトのID、外部キー
#         event_time (DateTime): イベント予定時刻
#         event_type (String): 計画されたイベントのタイプ
#         event_details (Text): イベント計画の詳細情報
#         altitude (Float): 計画されたイベントの高度
#         latitude (Float): 計画されたイベントの緯度
#         longitude (Float): 計画されたイベントの経度
#         orbital_speed (Float): 計画されたイベントの軌道速度
#         apoapsis_altitude (Float): 計画されたイベントの遠地点の高度
#         periapsis_altitude (Float): 計画されたイベントの近地点の高度
#         inclination (Float): 計画されたイベントの軌道傾斜角
#         eccentricity (Float): 計画されたイベントの軌道離心率
#     """

#     __tablename__ = "flight_event_plans"

#     plan_event_id = Column(Integer, primary_key=True)
#     flight_id = Column(Integer, ForeignKey("flight_details.flight_id"))
#     event_time = Column(DateTime)
#     event_type = Column(String)
#     event_details = Column(Text)
#     altitude = Column(Float)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     orbital_speed = Column(Float)
#     apoapsis_altitude = Column(Float)
#     periapsis_altitude = Column(Float)
#     inclination = Column(Float)
#     eccentricity = Column(Float)


# class FlightOrbitRecord(Base):
#     __tablename__ = "flight_orbit_record"
# TODO フライト中の情報が多いのでjsonで保存を検討する
