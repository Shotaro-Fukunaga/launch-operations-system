import krpc

def organize_parts(vessel):
    # 段階ごとの辞書を初期化
    stage_parts = {
        0: [],  # 0段目
        1: []   # 1段目
    }
    
    # 0段目の部品（指定された部品）
    first_stage_parts = {
        'fairingSize1', 'fuelTank', 'liquidEngine3.v2','probeCoreOcto2.v2', 'batteryBankMini', 'sasModule', 'commDish', 'solarPanels4'
    }
    
    # 1段目の部品（指定された部品）
    second_stage_parts = {
         'Decoupler.1','fuelTank.long','liquidEngine2.v2','basicFin'
    }

    # 全ての部品を繰り返し、どちらの段階に属するかを識別
    for part in vessel.parts.all:
        # 部品の名前が0段目のリストにある場合
        if part.name in first_stage_parts:
            stage_parts[0].append(part.title)
            print(part.title)
            print(part.mass)
        
        # 部品の名前が1段目のリストにある場合
        elif part.name in second_stage_parts:
            stage_parts[1].append(part.title)
            
    
    return stage_parts

# KSPへの接続を開始
conn = krpc.connect(name='Stage Separation')
vessel = conn.space_center.active_vessel

# 段階ごとの部品を獲得
stages = organize_parts(vessel)

# 結果を出力
# for stage, parts in stages.items():
#     print(f"Stage {stage} Parts:")
#     for part in parts:
#         print(part)
#     print("\n")
