from datetime import datetime

def room_calculation(room_name, people, check_in):
    """
    部屋タイプ、人数、チェックイン日に基づいて基本料金を計算する
    土曜日チェックインの場合は追加料金あり
    """
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
    
    if room_name not in room_prices:
        raise ValueError(f"無効な部屋名: {room_name}")

    fee = room_prices[room_name] * people

    # 曜日判定：チェックインが土曜日なら追加料金を加算
    if check_in:
        day_of_week = check_in.strftime('%A')  # 英語で曜日を取得
        print(f"チェックイン日の曜日: {day_of_week}")  # デバッグ用
        if day_of_week == 'Saturday':  # 土曜日の場合
            fee += 2000 * people

    return fee

# プラン料金の定義（1人あたり）
PLAN_PRICES = {
    "なし": 0,
    "前沢牛の網焼きとロースト前沢牛の握り付き和食膳プラン": 3000,
    "【前沢牛】【HP予約特典付き】≪ちょっと贅沢なご夕食≫　前沢牛の網焼きとロースト前沢牛の握り付き和食膳プラン": 3000,
    "前沢牛＆伊勢海老＆あわび＆ズワイガニのおまねきプラン": 6600,
    "前沢牛・伊勢海老・あわび・ズワイガニの豪華和食膳プラン": 6000,
    "【お誕生・記念日プラン】(*≧∇≦)/　　ホールケーキ付♪サプライズでお祝いしましょ♪": 4200,
}

def estimate_calculation(banquet, people, check_in, room_name=None, plan="なし", check_out_date=None):
    """
    予約の総料金を計算する
    
    Parameters:
    banquet (str): 宴会の有無 ("true" または "false")
    people (int): 宿泊人数
    check_in (datetime/str): チェックイン日
    room_name (str, optional): 部屋名
    plan (str, optional): 選択されたプラン
    check_out_date (datetime/str, optional): チェックアウト日
    
    Returns:
    int: 計算された料金
    """
    banquet = str(banquet).lower()
    if banquet not in ['true', 'false']:
        raise ValueError("宴会の値は 'true' または 'false' でなければなりません")
    
    # check_inをdatetime型に変換（文字列の場合）
    if isinstance(check_in, str):
        try:
            if '/' in check_in:
                check_in = check_in.replace('/', '-')
            check_in = datetime.strptime(check_in, "%Y-%m-%d")
        except ValueError:
            raise ValueError("check_inの日付形式が不正です。YYYY-MM-DD形式で入力してください。")
    
    if not isinstance(check_in, datetime):
        raise ValueError("check_inはdatetimeオブジェクトでなければなりません")
    
    if people == 0:
        raise ValueError("人数０は無効な数値です")
    
    # 宴会の場合
    if banquet == 'true':
        fee = 24400 * people
    else:
        fee = room_calculation(room_name, people, check_in)
        # 追加プラン料金の加算
        if plan not in PLAN_PRICES:
            raise ValueError(f"無効なプラン名: {plan}")
        fee += PLAN_PRICES[plan] * people  # 1人あたりのプラン料金を人数分加算

    # 宿泊日数を計算（check_out_dateが指定されている場合）
    if check_out_date:
        # check_out_dateをdatetime型に変換（文字列の場合）
        if isinstance(check_out_date, str):
            try:
                if '/' in check_out_date:
                    check_out_date = check_out_date.replace('/', '-')
                check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("check_out_dateの日付形式が不正です。YYYY-MM-DD形式で入力してください。")
        
        # 宿泊日数を計算
        nights = (check_out_date - check_in).days
        if nights <= 0:
            nights = 1
        
        # 宿泊日数に応じた料金計算
        fee = fee * nights
        
        # 長期滞在割引（オプション）
        if nights >= 7:
            # 7泊以上の場合、10%割引
            fee = int(fee * 0.9)
        elif nights >= 3:
            # 3泊以上の場合、5%割引
            fee = int(fee * 0.95)

    return fee
