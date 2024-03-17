
import krpc
import math
conn = krpc.connect(name='Stage 1 Status')
vessel = conn.space_center.active_vessel

def get_kPa():
  return
def delta_v(fuel_amount:int,isp:int,m0:int):
  # 地球の重力加速度（m/s²）
  g0 = 9.80665
  
  # 宇宙船の初期質量（kg）
  m0 = m0

  # LiquidFuelの密度（トン/単位）
  fuel_density = 0.005  # この値はKSP内でのLiquidFuelの密度に基づいています
  
  # 燃料の質量（kg）
  fuel_mass = fuel_amount * fuel_density * 1000  # トンからkgへ変換

  # 燃料を消費した後の質量（kg）
  mf = m0 - fuel_mass

  # Delta-Vの計算
  result = isp * g0 * math.log(m0 / mf)
  return result

# for part in vessel.parts.all:
#   print(part.name)
#   print(part.title)
# second_engine = vessel.parts.engines[1]
# print(second_engine.specific_impulse)
# print(second_engine.vacuum_specific_impulse)

def get_tank_resources(tank):
  liquid_fuel_amount = tank.resources.amount('LiquidFuel')
  oxidizer_amount = tank.resources.amount('Oxidizer')
  return liquid_fuel_amount,oxidizer_amount

# 'fuelTank.long'か'fuelTank'
fuel_tank_long_parts = [part for part in vessel.parts.all if part.name == 'fuelTank']

fuel_amount = 0
# 見つかった燃料タンクから燃料の量を取得
for tank in fuel_tank_long_parts:
    liquid_fuel_amount = tank.resources.amount('LiquidFuel')
    oxidizer_amount = tank.resources.amount('Oxidizer')
    fuel_amount = liquid_fuel_amount + oxidizer_amount
    print(f"{tank.title} contains {liquid_fuel_amount} units of LiquidFuel and {oxidizer_amount} units of Oxidizer")


second_engine = vessel.parts.engines[0]
isp = second_engine.specific_impulse

# 宇宙船の初期質量（kg）
m0 = 3130


print(f"Mass:{m0}")
print(f"Dry Mass:{vessel.dry_mass}")
print(f"Delta-V: {delta_v(fuel_amount,isp,m0)} m/s")

# stage_number = 1
# stage_parts = [part for part in vessel.parts.all if part.stage == stage_number]
# stage_dry_mass = sum(part.dry_mass for part in stage_parts)
# print(stage_dry_mass)
# for part in vessel.parts.all:
#   print(part.title)
#   print(part.dry_mass)
#   print(part.stage)
# stage1_mass = sum(mass for part.mas in stage_1_parts)
# stage_number = 0
# engines = [engine for engine in vessel.parts.engines if engine.part.stage == stage_number]
# fuel_tanks = [tank for tank in vessel.parts.all if tank.stage == stage_number and 'LiquidFuel' in tank.resources.names]

# # 燃料の密度と量をもとに燃料の質量を計算
# liquid_fuel_mass = sum(tank.resources.amount('LiquidFuel') * fuel_density * 1000 for tank in fuel_tanks if tank.resources.has_resource('LiquidFuel'))
# oxidizer_mass = sum(tank.resources.amount('Oxidizer') * fuel_density * 1000 for tank in fuel_tanks if tank.resources.has_resource('Oxidizer'))

# # 燃料の総質量を計算（LiquidFuel と Oxidizer）
# total_fuel_mass = liquid_fuel_mass + oxidizer_mass

# # ステージ1のISPを取得（複数のエンジンがある場合は平均ISPを使用するか、主エンジンのISPを使用）
# isp = engines[0].specific_impulse

# # ステージ1の初期質量と乾燥質量
# m0 = vessel.mass  # 初期質量
# mf = vessel.dry_mass + fuel_mass  # 乾燥質量 + ステージ1の燃料質量

# # デルタVの計算
# delta_v = isp * g0 * math.log(m0 / mf)

# print(f"Stage {stage_number} Delta-V: {delta_v} m/s")