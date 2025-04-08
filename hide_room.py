# 宴会の際部屋表示を非表示にする
def hide_room(banquet_var, label_room, room_name):
    banquet = banquet_var.get()  # 宴会の有無を取得
    if banquet == 'あり':  # 宴会「あり」の場合
        label_room.place_forget()  # ラベルを非表示にする
        room_name.place_forget()  # プルダウンを非表示にする
        room_name.config(state="disabled")  # プルダウンの選択を不可にする
    else:  # 宴会「なし」の場合
        label_room.place(x=10, y=250)  # ラベルを再表示
        room_name.place(x=150, y=250)  # プルダウンを再表示
        room_name.config(state="normal")  # プルダウンの選択を可能にする
