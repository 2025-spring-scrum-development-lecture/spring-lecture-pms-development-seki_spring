import json
from datetime import datetime
from tkinter import messagebox
from json_code import get_reservations_file_path

def load_reservations(reservations_file=None):
    """予約データを読み込む"""
    if reservations_file is None:
        reservations_file = get_reservations_file_path()
        
    try:
        with open(reservations_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # ファイルが存在しない場合は空のリストを作成
        reservations = []
        with open(reservations_file, 'w', encoding='utf-8') as f:
            json.dump(reservations, f, ensure_ascii=False, indent=4)
        return reservations

def update_room_availability(app, reservations):
    """予約データに基づいて部屋の空室状況を更新する"""
    # 部屋の空室状況を初期化
    app.reset_room_availability()
    
    # 現在の日付
    current_date = datetime.now().strftime("%Y/%m/%d")
    current_date_obj = datetime.strptime(current_date, "%Y/%m/%d")
    
    # 各予約をチェックし、チェックイン日が現在日付以前でチェックアウト日が現在日付より後の場合、
    # その部屋は現在使用中と見なす
    for reservation in reservations:
        # チェックアウト済みの予約は空室状況に影響しない
        if reservation.get("status") == "チェックアウト済":
            continue
            
        check_in = reservation.get("check_in")
        check_out = reservation.get("check_out")
        room_name = reservation.get("room_name")
        banquet = reservation.get("banquet") == "あり"
        
        # 日付の比較
        if check_in and check_out and room_name:
            # 文字列を日付オブジェクトに変換
            check_in_date = datetime.strptime(check_in, "%Y/%m/%d")
            check_out_date = datetime.strptime(check_out, "%Y/%m/%d")
            
            # 現在の日付がチェックイン日以降かつチェックアウト日より前の場合、部屋は使用中
            if check_in_date <= current_date_obj < check_out_date:
                # 部屋の空室数を減らす
                if banquet:
                    if room_name in app.room_availability_banquet and app.room_availability_banquet[room_name] > 0:
                        app.room_availability_banquet[room_name] -= 1
                else:
                    if room_name in app.room_availability_all and app.room_availability_all[room_name] > 0:
                        app.room_availability_all[room_name] -= 1
    
    print("予約データを読み込み、部屋の空室状況を更新しました。")

def process_checkout(reservation_id, reservations, reservations_file=None):
    """チェックアウト処理を行う"""
    if reservations_file is None:
        reservations_file = get_reservations_file_path()
        
    # 予約データを更新
    updated = False
    for reservation in reservations:
        if reservation.get("id") == reservation_id:
            # チェックアウト済みのステータスを追加
            reservation["status"] = "チェックアウト済"
            updated = True
            break
    
    if updated:
        # 予約データを保存
        with open(reservations_file, 'w', encoding='utf-8') as f:
            json.dump(reservations, f, ensure_ascii=False, indent=4)
        return True
    else:
        return False

def get_reservation_status(reservation, current_date_obj, active_rooms=None):
    """
    予約の状態を判定する
    
    Parameters:
    reservation (dict): 予約情報
    current_date_obj (datetime): 現在の日付
    active_rooms (dict, optional): 部屋の使用状況を追跡する辞書
    
    Returns:
    str: 予約状態 ("チェックアウト済", "滞在中", "予約済")
    """
    # すでにチェックアウト済みの場合
    if "status" in reservation and reservation["status"] == "チェックアウト済":
        return "チェックアウト済"
    
    # 日付に基づいて状態を判定
    check_in = reservation.get("check_in")
    check_out = reservation.get("check_out")
    room_name = reservation.get("room_name")
    
    if check_in and check_out:
        check_in_date = datetime.strptime(check_in, "%Y/%m/%d")
        check_out_date = datetime.strptime(check_out, "%Y/%m/%d")
        
        if current_date_obj >= check_out_date:
            # 自動的にチェックアウト済みとして更新
            reservation["status"] = "チェックアウト済"
            return "チェックアウト済"
        elif current_date_obj >= check_in_date:
            # 部屋の使用状況を追跡
            if active_rooms is not None and room_name:
                # この部屋がすでに使用中かどうかをチェック
                if room_name in active_rooms:
                    # 同じ部屋が使用中の場合、予約の日付を比較
                    active_check_in = active_rooms[room_name]["check_in"]
                    active_check_out = active_rooms[room_name]["check_out"]
                    
                    # 現在の予約が既存の予約と重複しない場合のみ「滞在中」とする
                    if check_in_date >= active_check_out or check_out_date <= active_check_in:
                        return "予約済"
                else:
                    # この部屋はまだ使用されていないので、使用中としてマーク
                    active_rooms[room_name] = {
                        "check_in": check_in_date,
                        "check_out": check_out_date
                    }
            
            return "滞在中"
    
    return "予約済"
