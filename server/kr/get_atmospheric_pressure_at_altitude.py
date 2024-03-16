import krpc

# conn = krpc.connect()
# space_center = conn.space_center
# vessel = space_center.active_vessel
# body = vessel.orbit.body

# 高度をメートル単位で指定（例：地表から1000mの高度）
altitude = 0

# 惑星の大気圧を高度から推定する関数（この関数は概算であり、実際の大気モデルには依存します）
def get_atmospheric_pressure_at_altitude(altitude):
    # Kerbinの大気モデルを基にした概算例。他の惑星ではパラメータが異なります。
   
    #https://wiki.kerbalspaceprogram.com/wiki/Kerbin#:~:text=Kerbin%20has%20a%20thick%2C%20warm,a%20depth%20of%2070%2C000%20meters.
    sea_level_pressure = 101.325  # Kerbinの海面圧力（kPa）
    
    # https://wiki.kerbalspaceprogram.com/wiki/Atmosphere#:~:text=The%20scale%20height%20of%20an,time%20you%20go%205600m%20higher.
    scale_height = 5600.0  # Kerbinの大気のスケール高度（m）
    
    pressure = sea_level_pressure * (2.718281828459 ** (-altitude / scale_height))
    return pressure


# 指定した高度での大気圧を取得
pressure_at_altitude = get_atmospheric_pressure_at_altitude(altitude)
print(f'Altitude: {altitude}m, Pressure: {pressure_at_altitude}kPa')

