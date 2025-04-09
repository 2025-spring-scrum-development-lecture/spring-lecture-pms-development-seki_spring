import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from estimate_calculation import estimate_calculation
from hide_room import hide_room
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_notification_system import email_notification_system
from json_code import json_storage
import json
import os
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=800, height=600)
        master.geometry("800x600")
        master.title("予約システム")
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
        self.banquet_var = tk.StringVar(value="なし")  # 初期値を設定
        self.radio_button_yes = tk.Radiobutton(
            self,
            text="あり",
            variable=self.banquet_var,
            value="あり",
            command=lambda: hide_room(
                self.banquet_var, self.label_room, self.room_name
            ),
        )
        self.radio_button_yes.place(x=150, y=90)
        self.radio_button_no = tk.Radiobutton(
            self,
            text="なし",
            variable=self.banquet_var,
            value="なし",
            command=lambda: hide_room(
                self.banquet_var, self.label_room, self.room_name
            ),
        )
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

        self.room_prices = {
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
            "和洋室7.5畳（西館）": 15400,
        }
        self.room_availability = {
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

        # 部屋の名前
        self.label_room = tk.Label(self, text="部屋の名前")
        self.label_room.place(x=10, y=250)

        self.room_name = ttk.Combobox(
            self,
            values=[
                "見返の間",
                "茶臼の間",
                "七時雨の間",
                "源太の間",
                "黒倉の間",
                "岩手山側 露天風呂付和室（本館）",
                "檜の内風呂和洋室（本館）",
                "岩手山側和室（本館）",
                "和室（本館）",
                "和室28畳（西館）",
                "和室10畳（西館）",
                "洋室10畳（西館）",
                "和洋室7.5畳（西館）",
            ],
        )
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
        self.button_estimatedfee_text = tk.Button(
            self, text="見積もり料金", command=self.calculate_fee
        )
        self.button_estimatedfee_text.place(x=10, y=490)

        self.fee = tk.Label(self, text="0円")
        self.fee.place(x=150, y=490)

        # メール送信結果を表示するラベル
        self.result_label = tk.Label(self, text="", fg="black")
        self.result_label.place(x=10, y=560)
        
        self.button_reservation = tk.Button(self, text="予約（確定）", command=self.process_reservation)

        self.button_reservation.place(x=10, y=530)

        # 内容をリセットボタン
        self.button_reset = tk.Button(
            self, text="内容をリセット", command=self.reset_input_contains
        )
        self.button_reset.place(x=150, y=530)

    def reset_input_contains(self):
        self.last_name.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.check_in.set_date(datetime.now())
        self.check_out.set_date(datetime.now())
        self.room_name.set("")
        self.people.set("1")
        self.banquet_var.set(False)
        self.text_paymentmethod.delete("1.0", tk.END)
        self.remarks.delete("1.0", tk.END)
        self.fee.config(text="-")

    def calculate_fee(self):
        try:
            # 入力値を取得
            banquet = "true" if self.banquet_var.get() == "あり" else "false"
            people = int(self.people.get())
            room_name = self.room_name.get()

            # 見積もり計算
            fee = estimate_calculation(banquet, people, room_name)

            # 見積もり料金を表示
            self.fee.config(text=f"{fee:,}円")
        except ValueError as e:
            self.fee.config(text=f"エラー: {e}")
            
    def process_reservation(self):
        try:
            # ウィジェットから値を取得
            name = self.last_name.get() + " " + self.first_name.get()
            email = self.email.get()
            people = self.people.get()
            room_name = self.room_name.get()
            banquet = self.banquet_var.get()
            check_in = self.check_in.get()
            check_out = self.check_out.get()
            remarks = self.remarks.get("1.0", "end").strip()
            total = self.fee.cget("text")

            # JSON保存
            json_storage(name, email, people, room_name, banquet, check_in, check_out, remarks, total)
            print("予約情報がJSONファイルに保存されました！")
            
            if name and email and check_in and check_out and room_name and people:
                available = self.room_availability.get(room_name, 0)
                if available > 0:
                    self.room_availability[room_name] -= 1  # 空室があるので、部屋の空きを1つ減らす
                    price = self.room_prices.get(room_name, 0) * int(people)
                    banquet_text = "あり" if self.banquet_var.get() else "なし"
                    if self.banquet_var.get():
                        price += 22400
                    messagebox.showinfo("予約完了", "予約が完了しました！メールを送信しました。")
                else:
                    # 空きがない場合は「満室です」というエラーメッセージを表示
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
            else:
                messagebox.showerror("エラー", "すべての項目を入力してください")

            # メール送信
            email_notification_system(
                email=self.email,            # ウィジェットそのものを渡す
                last_name=self.last_name,
                banquet_var=self.banquet_var,
                people=self.people,
                room_name=self.room_name,
                result_label=self.result_label,
            )
            print("メールが送信されました！")
        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
