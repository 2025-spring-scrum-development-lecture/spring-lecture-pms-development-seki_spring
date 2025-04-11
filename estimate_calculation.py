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
    plan_price = {
        "前沢牛の網焼きとロースト前沢牛の握り付き和食膳プラン": 3000,
        "【前沢牛】【HP予約特典付き】≪ちょっと贅沢なご夕食≫　前沢牛の網焼きとロースト前沢牛の握り付き和食膳プラン": 3000,
        "前沢牛＆伊勢海老＆あわび＆ズワイガニのおまねきプラン": 6600,
        "前沢牛・伊勢海老・あわび・ズワイガニの豪華和食膳プラン": 6000,
        "【お誕生・記念日プラン】(*≧∇≦)/　　ホールケーキ付♪サプライズでお祝いしましょ♪": 4200,
        
    }
    if room_name in room_prices:
        fee = room_prices[room_name] * people
    else:
        raise ValueError(f"無効な部屋名: {room_name}")

    fee = room_prices[room_name] * people

    # 曜日判定
    if check_in:
        day_of_week = check_in.strftime('%A')  # 英語で曜日を取得
        print(f"チェックイン日の曜日: {day_of_week}")  # デバッグ用
        if day_of_week == 'Saturday':  # 土曜日の場合
            fee += 2000 * people  # 土曜追加料金

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

def estimate_calculation(banquet, people, check_in, room_name=None, plan="なし"):
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

    return fee