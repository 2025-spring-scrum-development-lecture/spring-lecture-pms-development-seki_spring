def estimate_calculation(banquet, people, room_name=None):
    if banquet not in ['true', 'false']:
        raise ValueError("宴会の値は 'true' または 'false' でなければなりません")
    
    if people == 0:
        raise ValueError("人数０は無効な数値です")
    else:
        if banquet == 'true':  # 宴会あり
            fee = 24400 * people
        else:  # 宴会なし
            fee = room_calculation(room_name, people)
    return fee

def room_calculation(room_name, people):
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

    if room_name in room_prices:
        fee = room_prices[room_name] * people
    else:
        raise ValueError(f"無効な部屋名: {room_name}")
    return fee