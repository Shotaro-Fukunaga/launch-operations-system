import krpc

def main():
    # KSPに接続
    conn = krpc.connect(name='Ascent Autopilot Example')
    vessel = conn.space_center.active_vessel
    mechjeb = conn.mech_jeb

    # アセントオートパイロットモジュールを取得
    ascent = mechjeb.ascent_autopilot

    # 軌道の目標値を設定
    ascent.desired_orbit_altitude = 200000  # 目標軌道高度200km
    ascent.desired_inclination = 28.5       # 目標軌道傾斜角28.5度

    # ロール制御を設定
    ascent.force_roll = True
    ascent.turn_roll = 90

    # 自動ステージングを有効にする
    ascent.autostage = True

    # オートパイロットを有効にして打ち上げ
    ascent.enabled = True
    vessel.control.activate_next_stage()

    # 打ち上げが完了するまで待機
    while ascent.enabled:
        pass

    print("Launch complete!")

if __name__ == '__main__':
    main()




# import krpc

# class KrpcMechjeb:
#     # AscentAutopilot
#     # 
#     def __init__(self):
#         self.conn = krpc.connect(name='Ascent Autopilot Example')
#         self.vessel = self.conn.space_center.active_vessel
#         self.mechjeb = self.conn.mech_jeb.ascent_autopilot

#     @property
#     def enabled(self) -> bool:
#         return self.mechjeb.enabled

#     @enabled.setter
#     def enabled(self, value: bool):
#         self.mechjeb.enabled = value

#     @property
#     def status(self) -> str:
#         return self.mechjeb.status

#     @property
#     def ascent_path_index(self) -> int:
#         return self.mechjeb.ascent_path_index

#     @ascent_path_index.setter
#     def ascent_path_index(self, value: int):
#         self.mechjeb.ascent_path_index = value

#     @property
#     def desired_inclination(self) -> float:
#         return self.mechjeb.desired_inclination

#     @desired_inclination.setter
#     def desired_inclination(self, value: float):
#         self.mechjeb.desired_inclination = value

#     @property
#     def desired_orbit_altitude(self) -> float:
#         return self.mechjeb.desired_orbit_altitude

#     @desired_orbit_altitude.setter
#     def desired_orbit_altitude(self, value: float):
#         self.mechjeb.desired_orbit_altitude = value

#     @property
#     def force_roll(self) -> bool:
#         return self.mechjeb.force_roll

#     @force_roll.setter
#     def force_roll(self, value: bool):
#         self.mechjeb.force_roll = value

#     @property
#     def turn_roll(self) -> float:
#         return self.mechjeb.turn_roll

#     @turn_roll.setter
#     def turn_roll(self, value: float):
#         self.mechjeb.turn_roll = value

#     @property
#     def vertical_roll(self) -> float:
#         return self.mechjeb.vertical_roll

#     @vertical_roll.setter
#     def vertical_roll(self, value: float):
#         self.mechjeb.vertical_roll = value

#     @property
#     def limit_ao_a(self) -> bool:
#         return self.mechjeb.limit_ao_a

#     @limit_ao_a.setter
#     def limit_ao_a(self, value: bool):
#         self.mechjeb.limit_ao_a = value

#     @property
#     def max_ao_a(self) -> float:
#         return self.mechjeb.max_ao_a

#     @max_ao_a.setter
#     def max_ao_a(self, value: float):
#         self.mechjeb.max_ao_a = value

#     @property
#     def ao_a_limit_fadeout_pressure(self) -> float:
#         return self.mechjeb.ao_a_limit_fadeout_pressure

#     @ao_a_limit_fadeout_pressure.setter
#     def ao_a_limit_fadeout_pressure(self, value: float):
#         self.mechjeb.ao_a_limit_fadeout_pressure = value

#     @property
#     def corrective_steering(self) -> bool:
#         return self.mechjeb.corrective_steering

#     @corrective_steering.setter
#     def corrective_steering(self, value: bool):
#         self.mechjeb.corrective_steering = value

#     @property
#     def corrective_steering_gain(self) -> float:
#         return self.mechjeb.corrective_steering_gain

#     @corrective_steering_gain.setter
#     def corrective_steering_gain(self, value: float):
#         self.mechjeb.corrective_steering_gain = value

#     @property
#     def autostage(self) -> bool:
#         return self.mechjeb.autostage

#     @autostage.setter
#     def autostage(self, value: bool):
#         self.mechjeb.autostage = value

#     @property
#     def autodeploy_solar_panels(self) -> bool:
#         return self.mechjeb.autodeploy_solar_panels

#     @autodeploy_solar_panels.setter
#     def autodeploy_solar_panels(self, value: bool):
#         self.mechjeb.autodeploy_solar_panels = value

#     @property
#     def auto_deploy_antennas(self) -> bool:
#         return self.mechjeb.auto_deploy_antennas

#     @auto_deploy_antennas.setter
#     def auto_deploy_antennas(self, value: bool):
#         self.mechjeb.auto_deploy_antennas = value

#     @property
#     def skip_circularization(self) -> bool:
#         return self.mechjeb.skip_circularization

#     @skip_circularization.setter
#     def skip_circularization(self, value: bool):
#         self.mechjeb.skip_circularization = value

#     @property
#     def warp_count_down(self) -> int:
#         return self.mechjeb.warp_count_down

#     @warp_count_down.setter
#     def warp_count_down(self, value: int):
#         self.mechjeb.warp_count_down = value

#     @property
#     def launch_lan_difference(self) -> float:
#         return self.mechjeb.launch_lan_difference

#     @launch_lan_difference.setter
#     def launch_lan_difference(self, value: float):
#         self.mechjeb.launch_lan_difference = value

#     @property
#     def launch_phase_angle(self) -> float:
#         return self.mechjeb.launch_phase_angle

#     @launch_phase_angle.setter
#     def launch_phase_angle(self, value: float):
#         self.mechjeb.launch_phase_angle = value


