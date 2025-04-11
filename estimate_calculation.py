from datetime import datetime  # datetimeモジュールをインポート

def room_calculation(room_name, people, check_in):
    room_prices = {
        "見返の間": 30000,
        "茶臼の間": 30000,
        "七時雨の間": 30000,
        "源太の間": 27000,
        "黒倉の間": 27000,
        "岩手山側 露天風呂付和室（本館）": 17400,
        "檜の内風呂和洋室（本館）": 18400,
        "岩手山側和室（本館）": 15400,
        "和室（本館）": 15400,
        "和室28畳（西館）": 15400,
        "和室10畳（西館）": 15400,
        "洋室10畳（西館）": 15400,
        "和洋室7.5畳（西館）": 15400
    }

    if not room_name:
        raise ValueError("部屋名が選択されていません")
    room_name = room_name.strip()

    if room_name not in room_prices:
        raise ValueError(f"無効な部屋名: {room_name}")

    fee = room_prices[room_name] * people

    # 曜日判定
    if check_in:
        day_of_week = check_in.strftime('%A')  # 英語で曜日を取得
        print(f"チェックイン日の曜日: {day_of_week}")  # デバッグ用
        if day_of_week == 'Saturday':  # 土曜日の場合
            fee += 2000 * people

    return fee

def estimate_calculation(banquet, people, check_in, room_name=None):
    banquet = str(banquet).lower()
    if banquet not in ['true', 'false']:
        raise ValueError("宴会の値は 'true' または 'false' でなければなりません")

    # check_inをdatetime型に変換
    if isinstance(check_in, str):  # 文字列の場合
        try:
            # スラッシュ形式の日付をハイフン形式に変換
            if '/' in check_in:
                check_in = check_in.replace('/', '-')
            check_in = datetime.strptime(check_in, "%Y-%m-%d")
        except ValueError:
            raise ValueError("check_inの日付形式が不正です。YYYY-MM-DD形式で入力してください。")

    if not isinstance(check_in, datetime):
        raise ValueError("check_inはdatetimeオブジェクトでなければなりません")

    if people == 0:
        raise ValueError("人数０は無効な数値です")

    if banquet == 'true':  # 宴会あり
        fee = 24400 * people
    else:  # 宴会なし
        fee = room_calculation(room_name, people, check_in)

    return fee