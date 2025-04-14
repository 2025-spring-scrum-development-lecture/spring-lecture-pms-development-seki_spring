def get_room_max_capacity():
    """
    部屋ごとの最大収容人数を返す
    """
    return {
        "見返の間": 2,
        "茶臼の間": 2,
        "七時雨の間": 2,
        "源太の間": 2,
        "黒倉の間": 2,
        "岩手山側 露天風呂付和室（本館）": 5,
        "檜の内風呂和洋室（本館）": 6,
        "岩手山側和室（本館）": 5,
        "和室（本館）": 2,
        "和室28畳（西館）": 10,
        "和室10畳（西館）": 5,
        "洋室10畳（西館）": 2,
        "和洋室7.5畳（西館）": 6,
    }

def get_initial_room_availability():
    """
    部屋の初期空室状況を返す
    """
    # 全体の部屋空室: 宴会なしの場合などに利用
    room_availability_all = {
        "見返の間": 1,
        "茶臼の間": 1,
        "七時雨の間": 1,
        "源太の間": 1,
        "黒倉の間": 1,
        "岩手山側 露天風呂付和室（本館）": 12,
        "檜の内風呂和洋室（本館）": 6,
        "岩手山側和室（本館）": 12,
        "和室（本館）": 3,
        "和室28畳（西館）": 1,
        "和室10畳（西館）": 3,
        "洋室10畳（西館）": 1,
        "和洋室7.5畳（西館）": 1,
    }
    
    # 宴会ありの場合に固定で利用する部屋のみの空室
    room_availability_banquet = {
        "和室28畳（西館）": 1,
        "和室10畳（西館）": 3,
        "洋室10畳（西館）": 1,
        "和洋室7.5畳（西館）": 1,
    }
    
    return room_availability_all, room_availability_banquet

def filter_rooms_by_capacity(rooms, room_max_capacity, people_count):
    """
    指定された人数に対応できる部屋のみをフィルタリングする
    
    Parameters:
    rooms (list): 部屋名のリスト
    room_max_capacity (dict): 部屋ごとの最大収容人数
    people_count (int): 宿泊人数
    
    Returns:
    list: 指定された人数に対応できる部屋のリスト
    """
    return [room for room in rooms if room_max_capacity.get(room, 0) >= people_count]

def check_room_capacity(room_name, people_count, room_max_capacity):
    """
    指定された部屋が指定された人数に対応できるかチェックする
    
    Parameters:
    room_name (str): 部屋名
    people_count (int): 宿泊人数
    room_max_capacity (dict): 部屋ごとの最大収容人数
    
    Returns:
    tuple: (対応可能かどうか, 最大収容人数)
    """
    max_capacity = room_max_capacity.get(room_name, 0)
    return (max_capacity >= people_count, max_capacity)
