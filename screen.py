import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from estimate_calculation import estimate_calculation
from email_notification_system import email_notification_system
from json_code import json_storage
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=800, height=600)
        master.geometry("800x600")
        master.title("予約システム")
        self.pack()

        # 全体の部屋空室: 宴会なしの場合などに利用
        self.room_availability_all = {
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
        self.room_availability_banquet = {
            "和室28畳（西館）": 1,
            "和室10畳（西館）": 3,
            "洋室10畳（西館）": 1,
            "和洋室7.5畳（西館）": 1,
        }

        self.create_widgets()

    def create_widgets(self):
        # お客様情報のFrame
        self.frame_customer = tk.LabelFrame(self, text="お客様情報", padx=10, pady=5)
        self.frame_customer.place(x=10, y=10, width=780, height=80)

        self.label_last_name = tk.Label(self.frame_customer, text="姓")
        self.label_last_name.place(x=10, y=10)
        self.last_name = tk.Entry(self.frame_customer, width=15)
        self.last_name.place(x=40, y=10)

        self.label_first_name = tk.Label(self.frame_customer, text="名")
        self.label_first_name.place(x=200, y=10)
        self.first_name = tk.Entry(self.frame_customer, width=15)
        self.first_name.place(x=230, y=10)

        self.label_email = tk.Label(self.frame_customer, text="メールアドレス")
        self.label_email.place(x=350, y=10)
        self.email = tk.Entry(self.frame_customer, width=30)
        self.email.place(x=425, y=10)
        
        self.email_careers = [
            "@docomo.ne.jp",
            "@au.com",
            "@ezweb.ne.jp",
            "@softbank.ne.jp",
            "@i.softbank.jp",
            "@rakumail.jp",
            "@uqmobile.jp",
            "@y-mobile.ne.jp",
            "@morijyobi.ac.jp",
            "@gmail.com",
        ]
        
        self.combobox_email = ttk.Combobox(self.frame_customer, values=self.email_careers)
        self.combobox_email.place(x=610, y=10)
        self.combobox_email.set("@morijyobi.ac.jp")

        # 予約情報のFrame
        self.frame_booking = tk.LabelFrame(self, text="予約情報", padx=10, pady=5)
        self.frame_booking.place(x=10, y=100, width=780, height=150)

        # 宴会の有無
        self.label_banquet = tk.Label(self.frame_booking, text="宴会の有無")
        self.label_banquet.place(x=10, y=10)
        self.banquet_var = tk.StringVar(value="なし")  # 初期値を設定
        # ここでコールバックを設定して、選択変更時に部屋の選択肢を更新する
        self.radio_button_yes = tk.Radiobutton(
            self.frame_booking,
            text="あり",
            variable=self.banquet_var,
            value="あり",
            command=self.update_room_options
        )
        self.radio_button_yes.place(x=100, y=10)
        self.radio_button_no = tk.Radiobutton(
            self.frame_booking,
            text="なし",
            variable=self.banquet_var,
            value="なし",
            command=self.update_room_options
        )
        self.radio_button_no.place(x=150, y=10)

        # 人数
        self.label_num_people = tk.Label(self.frame_booking, text="人数")
        self.label_num_people.place(x=10, y=50)
        self.people = ttk.Combobox(self.frame_booking, values=[str(i) for i in range(1, 11)], width=5)
        self.people.place(x=100, y=50)
        self.people.set("1")

        # チェックイン・チェックアウトの日付
        self.label_checkin = tk.Label(self.frame_booking, text="チェックインの日")
        self.label_checkin.place(x=250, y=10)
        self.check_in = DateEntry(self.frame_booking, width=12, mindate=datetime.today())
        self.check_in.place(x=350, y=10)

        self.label_checkout = tk.Label(self.frame_booking, text="チェックアウトの日")
        self.label_checkout.place(x=250, y=50)
        self.check_out = DateEntry(self.frame_booking, width=12, mindate=datetime.today())
        self.check_out.place(x=350, y=50)

        # 部屋の名前
        self.label_room = tk.Label(self.frame_booking, text="部屋の名前")
        self.label_room.place(x=10, y=90)
        # 初期は宴会なしの全ての部屋が選択できるようにする
        self.all_rooms = [
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
        ]
        self.room_name = ttk.Combobox(self.frame_booking, values=self.all_rooms)
        self.room_name.place(x=100, y=90)
        self.room_name.set("和室28畳（西館）")
        
        self.label_bus = tk.Label(self.frame_booking, text="送迎の有無")
        self.label_bus.place(x=250, y=90)
        
        self.bus_var = tk.StringVar(value="なし")  # 初期値を設定
        # ここでコールバックを設定して、選択変更時に部屋の選択肢を更新する
        self.bus_radio_button_yes = tk.Radiobutton(
            self.frame_booking,
            text="あり",
            variable=self.bus_var,
            value="あり",
        )
        self.bus_radio_button_yes.place(x=350, y=90)
        self.bus_radio_button_no = tk.Radiobutton(
            self.frame_booking,
            text="なし",
            variable=self.bus_var,
            value="なし",
        )
        self.bus_radio_button_no.place(x=400, y=90)
        

        # 支払情報と備考のFrame
        self.frame_misc = tk.LabelFrame(self, text="支払い情報と備考", padx=10, pady=5)
        self.frame_misc.place(x=10, y=260, width=780, height=150)
        self.label_paymentmethod = tk.Label(self.frame_misc, text="支払方法")
        self.label_paymentmethod.place(x=10, y=10)
        self.text_paymentmethod = tk.Text(self.frame_misc, height=5, width=40)
        self.text_paymentmethod.place(x=80, y=10)
        self.label_remarks = tk.Label(self.frame_misc, text="備考")
        self.label_remarks.place(x=370, y=10)
        self.remarks = tk.Text(self.frame_misc, height=5, width=40)
        self.remarks.place(x=430, y=10)

        # 見積もり料金とその他ボタン
        self.button_estimatedfee_text = tk.Button(
            self, text="見積もり料金", command=self.calculate_fee, bg="#4a90e2", fg="white"
        )
        self.button_estimatedfee_text.place(x=10, y=430)
        self.fee = tk.Label(self, text="0円")
        self.fee.place(x=150, y=430)
        self.result_label = tk.Label(self, text="", fg="black")
        self.result_label.place(x=10, y=560)
        self.button_reservation = tk.Button(
            self, text="予約（確定）", command=self.process_reservation, bg="#4a90e2", fg="white"
        )
        self.button_reservation.place(x=10, y=480)
        self.button_reset = tk.Button(
            self, text="内容をリセット", command=self.reset_input_contains, bg="#e74c3c", fg="white"
        )
        self.button_reset.place(x=150, y=480)

    def update_room_options(self):
        """
        ラジオボタンで宴会の有無が変更されたとき、
        宴会が「あり」なら、部屋の選択肢を固定の4つに更新し、
        「なし」の場合は全体の選択肢に戻す
        """
        if self.banquet_var.get() == "あり":
            allowed_rooms = list(self.room_availability_banquet.keys())
            self.room_name.config(values=allowed_rooms)
            # 現在の選択が allowed_rooms になければ、最初の部屋に設定する
            if self.room_name.get() not in allowed_rooms:
                self.room_name.set(allowed_rooms[0])
        else:
            self.room_name.config(values=self.all_rooms)
            # 必要に応じて初期値を設定（ここでは元の選択肢の最初の値に戻す）
            if self.room_name.get() not in self.all_rooms:
                self.room_name.set(self.all_rooms[0])

    def reset_input_contains(self):
        self.last_name.delete(0, tk.END)
        self.first_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.check_in.set_date(datetime.now())
        self.check_out.set_date(datetime.now())
        self.room_name.set("")
        self.people.set("1")
        # ラジオボタンは文字列 "あり" / "なし" を使っているので、clearなら "なし"
        self.banquet_var.set("なし")
        self.text_paymentmethod.delete("1.0", tk.END)
        self.remarks.delete("1.0", tk.END)
        self.fee.config(text="-")
        # 予約時の部屋選択肢もリセット
        self.room_name.config(values=self.all_rooms)
        self.room_name.set("和室28畳（西館）")
        self.bus_var.set("なし")

    def calculate_fee(self):
        try:
            # チェックイン日付を取得
            check_in_date_str = self.check_in.get()  # tkinterフォームから取得

            # 入力値を取得
            banquet = "true" if self.banquet_var.get() == "あり" else "false"
            people = int(self.people.get())
            room_name = self.room_name.get()
            
             # 見積もり料金を計算（チェックイン日付を追加）
            fee = estimate_calculation(banquet, people, check_in_date_str, room_name)
            self.fee.config(text=f"{fee:,}円")
        except ValueError as e:
            self.fee.config(text=f"エラー: {e}")
            

    def process_reservation(self):
        try:
            # ① 入力値の取得と空白除去
            last = self.last_name.get().strip()
            first = self.first_name.get().strip()
            email_user = self.email.get().strip()
            email_domain = self.combobox_email.get().strip
            full_email = f"{email_user}{email_domain}"
            check_in = self.check_in.get().strip()
            check_out = self.check_out.get().strip()
            room_name = self.room_name.get().strip()
            people = self.people.get().strip()

            # ② 必須項目の入力チェック
            if not last or not first:
                messagebox.showerror("入力エラー", "姓と名は必ず入力してください。")
                return

            if not email_user:
                messagebox.showerror("入力エラー", "メールアドレスを入力してください。")
                return

            if not (check_in and check_out and room_name and people):
                messagebox.showerror("入力エラー", "すべての項目を入力してください。")
                return

            # ③ 日付の妥当性チェック（例: check_inがcheck_outより前であるか）
            # ※日付の型が文字列の場合は、適切な日付型に変換して比較してください
            # ここでは例として、日付フォーマットが "YYYY/MM/DD" であると仮定
            from datetime import datetime
            check_in_date = datetime.strptime(check_in, "%Y/%m/%d")
            check_out_date = datetime.strptime(check_out, "%Y/%m/%d")
            if check_in_date >= check_out_date:
                messagebox.showerror("日付エラー", "チェックイン日はチェックアウト日より前である必要があります。")
                return

            # ④ 部屋の空室チェックと更新
            if self.banquet_var.get() == "あり":
                rooms_available = self.room_availability_banquet
                # 許可されている部屋かどうか
                if room_name not in rooms_available:
                    messagebox.showerror(
                        "エラー",
                        "宴会の場合、選択できる部屋は「和室28畳（西館）」「和室10畳（西館）」「洋室10畳（西館）」「和洋室7.5畳（西館）」に限定されています。"
                    )
                    return
                # 空室があるか確認
                if rooms_available[room_name] <= 0:
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
                    return
            else:
                rooms_available = self.room_availability_all
                if rooms_available.get(room_name, 0) <= 0:
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
                    return

            # 空室が確認できたので、更新
            rooms_available[room_name] -= 1

            # ⑤ 予約情報の組み立てと永続化（JSON保存）
            name = f"{last} {first}"
            total = self.fee.cget("text")
            remarks = self.remarks.get("1.0", "end").strip()
            json_storage(
                name, full_email, people, room_name,
                self.banquet_var.get(), check_in, check_out,
                remarks, total,
                self.bus_var.get()
            )
            print("予約情報が保存されました！")

            # ⑥ 予約完了のメッセージ表示
            messagebox.showinfo("予約完了", "予約が完了しました！メールを送信しました。")

            # # ⑦ メール送信（入力値を直接渡す）
            email_notification_system(
                email=self.email.get().strip(),       # 値を取得する
                last_name=self.last_name.get().strip(),  # `get()`を使って入力値を取得
                banquet_var=self.banquet_var.get(),      # BooleanVar/StringVarから値を取得
                people=self.people.get().strip(),        # `get()`を追加
                room_name=self.room_name.get().strip(),  # `get()`を追加
                result_label=self.result_label,
                check_in=self.check_in.get().strip(),    # 正しい日付値を取得
                check_out=self.check_out.get().strip(),
                fee=int(self.fee.cget("text").replace(",", "").strip("円")),
                bus_var=self.bus_var,
            )

        except ValueError as e:
            messagebox.showerror("入力エラー", f"入力エラー: {e}")
        except Exception as e:
            messagebox.showerror("エラー", f"予約処理中にエラーが発生しました: {e}")
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()