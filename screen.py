import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=800, height=600)
        master.geometry('800x600')
        master.title('予約システム')
        self.pack()

        self.create_widgets()

# ウィジェットを配置して画面を作るメソッド
    def create_widgets(self):
        # お客様のお名前
        self.label_name = tk.Label(self, text="お客様のお名前")
        self.label_name.place(x=10, y=10)

        self.label_last_name = tk.Label(self, text="姓")
        self.label_last_name.place(x=150, y=10)

        self.last_name = tk.Entry(self, width=15)
        self.last_name.place(x=190, y=10)

        self.label_first_name = tk.Label(self, text="名")
        self.label_first_name.place(x=350, y=10)

        self.first_name = tk.Entry(self, width=15)
        self.first_name.place(x=380, y=10)

        # メールアドレス
        self.label_email = tk.Label(self, text="お客様のメールアドレス")
        self.label_email.place(x=10, y=50)

        self.email = tk.Entry(self, width=30)
        self.email.place(x=150, y=50)

        # 宴会の有無
        self.label_banquet = tk.Label(self, text="宴会の有無")
        self.label_banquet.place(x=10, y=90)
        self.banquet_var = tk.StringVar()
        self.radio_button_yes = tk.Radiobutton(self, text="あり", variable=self.banquet_var, value="あり")
        self.radio_button_yes.place(x=150, y=90)
        self.radio_button_no = tk.Radiobutton(self, text="なし", variable=self.banquet_var, value="なし")
        self.radio_button_no.place(x=200, y=90)

        # 人数
        self.label_num_people = tk.Label(self, text="人数")
        self.label_num_people.place(x=10, y=130)

        self.people = ttk.Combobox(self, values=[str(i) for i in range(1, 11)], width=5)
        self.people.place(x=150, y=130)
        self.people.set("1")

        # チェックインの日
        self.label_checkin = tk.Label(self, text="チェックインの日")
        self.label_checkin.place(x=10, y=170)

        self.check_in = DateEntry(self, width=12, mindate=datetime.today())
        self.check_in.place(x=150, y=170)

        # チェックアウトの日
        self.label_checkout = tk.Label(self, text="チェックアウトの日")
        self.label_checkout.place(x=10, y=210)

        self.check_out = DateEntry(self, width=12, mindate=datetime.today())
        self.check_out.place(x=150, y=210)
        
        self.room_prices = {"見返の間": 30000, "茶臼の間": 30000, "七時雨の間": 30000, "源太の間": 27000, "黒倉の間": 27000, 
                        "岩手山側 露天風呂付和室（本館）": 17400, "檜の内風呂和洋室（本館）": 18400, "岩手山側和室（本館）"
                        : 15400, "和室（本館）": 15400, "和室28畳（西館）": 15400, "和室10畳（西館）": 15400, "洋室10畳（西館）"
                        : 15400, "和洋室7.5畳（西館）": 15400}
        self.room_availability = {"見返の間": 1, "茶臼の間": 1, "七時雨の間": 1, "源太の間": 1, "黒倉の間": 1,
                            "岩手山側 露天風呂付和室（本館）": 12, "檜の内風呂和洋室（本館）": 6,
                            "岩手山側和室（本館）": 12, "和室（本館）": 3, "和室28畳（西館）": 1,
                            "和室10畳（西館）": 3, "洋室10畳（西館）": 1, "和洋室7.5畳（西館）": 1}

        # 部屋の名前
        self.label_room = tk.Label(self, text="部屋の名前")
        self.label_room.place(x=10, y=250)

        self.room_name = ttk.Combobox(self, values=["見返の間", "茶臼の間", "七時雨の間", "源太の間", "黒倉の間",
                                                    "岩手山側 露天風呂付和室（本館）", "檜の内風呂和洋室（本館）",
                                                    "岩手山側和室（本館）", "和室（本館）", "和室28畳（西館）",
                                                    "和室10畳（西館）", "洋室10畳（西館）", "和洋室7.5畳（西館）"])
        self.room_name.place(x=150, y=250)

        # 支払方法
        self.label_paymentmethod = tk.Label(self, text="支払方法")
        self.label_paymentmethod.place(x=10, y=290)

        self.text_paymentmethod = tk.Text(self, height=5, width=40)
        self.text_paymentmethod.place(x=150, y=290)

        # 備考
        self.label_remarks = tk.Label(self, text="備考")
        self.label_remarks.place(x=10, y=390)

        self.remarks = tk.Text(self, height=5, width=40)
        self.remarks.place(x=150, y=390)

        # 見積もり料金
        self.label_estimatedfee_text = tk.Label(self, text="見積もり料金")
        self.label_estimatedfee_text.place(x=10, y=490)

        self.fee = tk.Label(self, text="sample")
        self.fee.place(x=150, y=490)

        # 予約ボタン
        self.button_reservation = tk.Button(self, text="予約（確定）")
        self.button_reservation.place(x=10, y=530)

        # 内容をリセットボタン
        self.button_reset = tk.Button(self, text="内容をリセット", command=self.reset_input_contains)
        self.button_reset.place(x=150, y=530)


    def reset_input_contains(self):
        self.last_name.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.check_in.set_date(datetime.now())
        self.check_out.set_date(datetime.now())
        self.room_name.set('')
        self.people.set('1')
        self.banquet_var.set(False)
        self.text_paymentmethod.delete("1.0", tk.END)
        self.remarks.delete("1.0", tk.END)
        self.fee.config(text="-")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()