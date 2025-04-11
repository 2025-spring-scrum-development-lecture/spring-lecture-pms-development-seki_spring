import os
import json
from datetime import datetime

def json_storage(name, email, people, room_name, banquet, check_in, check_out, remarks, total, bus, filename="customer_list.json"):
    new_entry = {
        "name": name,
        "email": email,
        "people": people,
        "room_name": room_name,
        "banquet": banquet,
        "check_in": check_in,
        "check_out": check_out,
        "remarks": remarks,
        "total": total,
        "bus": bus
    }
    print(f"現在の作業ディレクトリ: {os.getcwd()}")
    print(new_entry)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_entry)

    try:
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(f"データが{filename}に保存されました")
    except Exception as e:
        print(f"ファイルの保存に失敗しました: {e}")