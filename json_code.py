import json
import uuid
from datetime import datetime
import os

# 予約データを保存���るファイル名を定数として定義
RESERVATIONS_FILE = "reservations.json"

# ファイルの絶対パスを取得する関数
def get_reservations_file_path():
    # スクリプトが実行されているディレクトリを基準にする
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, RESERVATIONS_FILE)

def json_storage(name, email, people, room_name, banquet, check_in, check_out, remarks, fee, bus_var=None, plan=None):
    """
    予約情報をJSONファイルに保存する関数
    新しいパラメータ bus_var と plan を追加
    """
    # 予約IDを生成
    reservation_id = str(uuid.uuid4())[:8]
    
    # 現在の日時を取得
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    # 予約情報を辞書形式で作成
    reservation = {
        "id": reservation_id,
        "name": name,
        "email": email,
        "people": people,
        "room_name": room_name,
        "banquet": banquet,
        "check_in": check_in,
        "check_out": check_out,
        "remarks": remarks,
        "fee": fee,
        "created_at": now,
        "bus": bus_var,  # 送迎の有無
        "plan": plan     # 選択されたプラン
    }
    
    # 予約ファイルのパスを取得
    reservations_file = get_reservations_file_path()
    
    try:
        # 既存の予約情報を読み込む
        with open(reservations_file, "r", encoding="utf-8") as f:
            reservations = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # ファイルが存在しない場合や、JSONとして解析できない場合は空のリストを作成
        reservations = []
    
    # 新しい予約情報を追加
    reservations.append(reservation)
    
    # 予約情報をJSONファイルに保存
    with open(reservations_file, "w", encoding="utf-8") as f:
        json.dump(reservations, f, ensure_ascii=False, indent=4)
    
    print(f"予約情報を {reservations_file} に保存しました")
    return reservation_id
