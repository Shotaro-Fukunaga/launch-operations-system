from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from src.settings.database import Base


class Flights(Base):
    """
    ロケットのフライトに関する情報を格納するテーブル。

    Attributes:
        flight_id (Integer): フライトの一意識別子。プライマリキー。
        flight_number (String): フライト番号。各フライトを区別するための識別子。
        rocket_type (String): 使用されるロケットの型式またはモデル。
        launch_datetime (DateTime): フライトの打ち上げ日時。
        launch_site (String): フライトの打ち上げが行われる場所や施設。
        payload (Text): フライトによって運ばれるペイロードの詳細説明。
        orbit (String): ペイロードが投入される目的の軌道。
        mission_objective (Text): フライトのミッションや目的の詳細。
        launch_outcome (String): フライトの結果（例: "成功", "失敗"）。
        booster_landing_success (Boolean): 再利用可能なブースターの着陸が成功したかどうか。
        anomalies (Text): フライト中に発生した異常や問題に関する詳細情報。
    """

    __tablename__ = "flights"

    flight_id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String)
    rocket_type = Column(String)
    launch_datetime = Column(DateTime)
    launch_site = Column(String)
    payload = Column(Text)
    orbit = Column(String)
    mission_objective = Column(Text)
    launch_outcome = Column(String)
    booster_landing_success = Column(Boolean)
    anomalies = Column(Text)


class FlightPlans(Base):
    """
    FlightPlansテーブルは、フライト計画全体に関する静的な情報を保存します。

    Attributes:
        plan_id (Integer): 計画の一意識別子。プライマリキー。
        flight_id (Integer): 関連するフライトのID。外部キー。
        launch_window_start (DateTime): 打ち上げウィンドウ開始時間。
        launch_window_end (DateTime): 打ち上げウィンドウ終了時間。
        payload_mass (Float): ペイロードの質量。
        destination_orbit (String): 目的地となる軌道。
        mission_duration (Integer): ミッション期間（例：日数）。
        backup_date (DateTime): 予備日。
        mission_objectives (String): ミッションの目的や目標。
    """

    __tablename__ = "flight_plans"
    plan_id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.flight_id"))
    launch_window_start = Column(DateTime)
    launch_window_end = Column(DateTime)
    payload_mass = Column(Float)
    destination_orbit = Column(String)
    mission_duration = Column(Integer)
    backup_date = Column(DateTime)
    mission_objectives = Column(String)


class FlightPlanEvents(Base):
    """
    FlightPlanEventsテーブルは、フライト計画の各イベントに関する時系列情報を保存します。

    Attributes:
        plan_event_id (Integer): 計画イベントの一意識別子。プライマリキー。
        flight_id (Integer): 関連するフライトのID。外部キー。
        event_name (String): 計画されたイベントの名称（例：「MECO」「フェアリング分離」など）。
        planned_event_time (DateTime): 計画されたイベントの予定時刻。
        target_altitude (Float): 計画されたイベント時の目標高度（単位：km）。
        target_velocity (Float): 計画されたイベント時の目標速度（単位：km/s）。
        target_latitude (Float): 計画されたイベント時の目標緯度。
        target_longitude (Float): 計画されたイベント時の目標経度。
        target_orbit (String): 計画されたイベントにおける目的軌道。
    """

    __tablename__ = "flight_plan_events"
    plan_event_id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("flight_plans.plan_id"))
    event_name = Column(String(100))
    planned_event_time = Column(DateTime)
    target_altitude = Column(Float)
    target_velocity = Column(Float)
    target_latitude = Column(Float)
    target_longitude = Column(Float)
    target_orbit = Column(String(100))


class FlightEvents(Base):
    """
    FlightEventsテーブルは、ロケットのフライトイベントとテレメトリーデータを記録します。

    Attributes:
        event_id (Integer): イベントの一意識別子。プライマリキー。
        flight_id (Integer): 関連するフライトのID。外部キー。
        event_type (String): イベントの種類（例:打ち上げ、第一段階分離など）。
        event_time (DateTime): イベント発生の正確な日時。
        altitude (Float): イベント時の高度（単位:km）。
        velocity (Float): イベント時の速度（単位:km/s）。
        latitude (Float): イベント発生時の緯度。
        longitude (Float): イベント発生時の経度。
        acceleration (Float): イベント時の加速度（単位:m/s^2）。
        stage (Integer): ロケットのステージ番号（例:1, 2など）。
        liquid_fuel (Float): 液体燃料の残量（単位:kg）。
        oxidizer (Float): 酸化剤の残量（単位:kg）。
        delta_v (Float): デルタV（単位:m/s）、フライトの可変性を表す。
        engine_status (String): エンジンの状態（"running", "stopped", "fault"など）。
        communication_status (Boolean): 通信状態が確立しているかどうか（True: 確立, False: 障害あり）。
        battery_status (Float): バッテリーの状態または残量（単位:% または V）。
    """

    __tablename__ = "flight_events"

    event_id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, index=True)
    event_type = Column(String)
    event_time = Column(DateTime)
    altitude = Column(Float)
    velocity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    acceleration = Column(Float)
    stage = Column(Integer)
    liquid_fuel = Column(Float)
    oxidizer = Column(Float)
    delta_v = Column(Float)
    engine_status = Column(String)  # "running", "stopped", "fault" などの状態を文字列で保持
    communication_status = Column(Boolean)  # True で通信が確立している, False で通信障害がある
    battery_status = Column(Float)
