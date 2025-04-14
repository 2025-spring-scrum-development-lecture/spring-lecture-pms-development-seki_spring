import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
import json
import os

# 新しく作成したモジュールをインポート
from room_capacity import (
    get_room_max_capacity, get_initial_room_availability, 
    filter_rooms_by_capacity, check_room_capacity
)
from reservation_processor import (
    load_reservations, update_room_availability,
    process_checkout, get_reservation_status
)
from email_notification_system import email_notification_system, DEMO_MODE
from json_code import json_storage, get_reservations_file_path
from estimate_calculation import estimate_calculation, PLAN_PRICES

# メール送信用の環境変数を設定
# 実際の運用では、アプリケーション起動前に環境変数を設定するか、
# 設定ファイルから読み込むなどの方法が推奨されます
if 'MAIL_PASS' not in os.environ:
    # 開発環境用のダミーパスワード（実際の運用では使用しないでください）
    os.environ['MAIL_PASS'] = 'your_password_here'

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=800, height=600)
        master.geometry("800x600")
        master.title("予約システム" + (" [デモモード]" if DEMO_MODE else ""))
        self.pack()

        # 部屋ごとの最大収容人数を取得
        self.room_max_capacity = get_room_max_capacity()

        # 部屋の空室状況を初期化
        self.room_availability_all, self.room_availability_banquet = get_initial_room_availability()
        
        # 予約データを保存するファイル名
        self.reservations_file = get_reservations_file_path()
        
        # 予約データを読み込み、部屋の空室状況を更新
        self.reservations = load_reservations(self.reservations_file)
        update_room_availability(self, self.reservations)

        # メールドメインのリスト
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

        # 全ての部屋のリスト
        self.all_rooms = list(self.room_max_capacity.keys())
        
        # プランのリスト
        self.all_plans = ["なし"] + list(PLAN_PRICES.keys())

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
        
        # デモモードの場合、メールアドレス入力欄に注意書きを表示
        if DEMO_MODE:
            self.demo_label = tk.Label(self.frame_customer, text="※デモモード: メールは開発者に送信されます", fg="red")
            self.demo_label.place(x=425, y=35)
        
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
        # 人数が変更されたときに部屋の選択肢を更新するコールバックを設定
        self.people.bind("<<ComboboxSelected>>", self.update_room_options_by_people)

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
        self.room_name = ttk.Combobox(self.frame_booking, values=self.all_rooms)
        self.room_name.place(x=100, y=90)
        self.room_name.set("和室28畳（西館）")
        
        # プラン選択
        self.plan_label = tk.Label(self.frame_booking, text="プラン")
        self.plan_label.place(x=250, y=90)
        self.plans = ttk.Combobox(self.frame_booking, values=self.all_plans, width=30)
        self.plans.place(x=350, y=90)
        self.plans.set("なし")
        
        # 送迎の有無
        self.label_bus = tk.Label(self.frame_booking, text="送迎の有無")
        self.label_bus.place(x=550, y=10)
        
        self.bus_var = tk.StringVar(value="なし")  # 初期値を設定
        self.bus_radio_button_yes = tk.Radiobutton(
            self.frame_booking,
            text="あり",
            variable=self.bus_var,
            value="あり",
        )
        self.bus_radio_button_yes.place(x=650, y=10)
        self.bus_radio_button_no = tk.Radiobutton(
            self.frame_booking,
            text="なし",
            variable=self.bus_var,
            value="なし",
        )
        self.bus_radio_button_no.place(x=700, y=10)

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
        
        # 予約管理ボタンを追加
        self.button_manage = tk.Button(
            self, text="予約管理", command=self.open_reservation_manager, bg="#2ecc71", fg="white"
        )
        self.button_manage.place(x=300, y=480)

    def update_room_options(self):
        """
        ラジオボタンで宴会の有無が変更されたとき、
        宴会が「あり」なら、部屋の選択肢を固定の4つに更新し、
        「なし」の場合は全体の選択肢に戻す
        """
        # 現在選択されている人数を取得
        try:
            selected_people = int(self.people.get())
        except ValueError:
            selected_people = 1  # デフォルト値

        if self.banquet_var.get() == "あり":
            # 宴会ありの場合、固定の部屋から人数制限に合う部屋のみを表示
            allowed_rooms = filter_rooms_by_capacity(
                self.room_availability_banquet.keys(), 
                self.room_max_capacity, 
                selected_people
            )
            
            if not allowed_rooms:
                messagebox.showwarning("警告", f"{selected_people}人に対応できる宴会用の部屋がありません。人数を減らすか、宴会なしで予約してください。")
                # 人数を1人に戻す
                self.people.set("1")
                # 再度部屋の選択肢を更新
                allowed_rooms = list(self.room_availability_banquet.keys())
            
            self.room_name.config(values=allowed_rooms)
            # 現在の選択が allowed_rooms になければ、最初の部屋に設定する
            if self.room_name.get() not in allowed_rooms and allowed_rooms:
                self.room_name.set(allowed_rooms[0])
        else:
            # 宴会なしの場合、全部屋から人数制限に合う部屋のみを表示
            allowed_rooms = filter_rooms_by_capacity(
                self.all_rooms, 
                self.room_max_capacity, 
                selected_people
            )
            
            if not allowed_rooms:
                messagebox.showwarning("警告", f"{selected_people}人に対応できる部屋がありません。人数を減らしてください。")
                # 人数を1人に戻す
                self.people.set("1")
                # 再度部屋の選択肢を更新
                allowed_rooms = self.all_rooms
            
            self.room_name.config(values=allowed_rooms)
            # 現在の選択が allowed_rooms になければ、最初の部屋に設定する
            if self.room_name.get() not in allowed_rooms and allowed_rooms:
                self.room_name.set(allowed_rooms[0])

    def update_room_options_by_people(self, event=None):
        """人数が変更されたときに部屋の選択肢を更新する"""
        self.update_room_options()  # 既存の関数を再利用

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
        self.bus_var.set("なし")
        self.plans.set("なし")
        self.text_paymentmethod.delete("1.0", tk.END)
        self.remarks.delete("1.0", tk.END)
        self.fee.config(text="-")
        # 予約時の部屋選択肢もリセット
        self.update_room_options()  # 人数とバンケットの状態に基づいて部屋の選択肢を更新

    def calculate_fee(self):
        try:
            # チェックイン日付とチェックアウト日付を取得
            check_in_date_str = self.check_in.get()
            check_out_date_str = self.check_out.get()

            # 入力値を取得
            banquet = "true" if self.banquet_var.get() == "あり" else "false"
            people = int(self.people.get())
            room_name = self.room_name.get()
            plan = self.plans.get()
        
            # 見積もり料金を計算（チェックイン日付とチェックアウト日付を追加）
            fee = estimate_calculation(banquet, people, check_in_date_str, room_name, plan, check_out_date_str)
            self.fee.config(text=f"{fee:,}円")
        except ValueError as e:
            self.fee.config(text=f"エラー: {e}")
    
    def load_reservations_and_update_availability(self):
        """予約データを読み込み、現在の日付に基づいて部屋の空室状況を更新する"""
        try:
            # 予約データを読み込む
            self.reservations = load_reservations(self.reservations_file)
            
            # 部屋の空室状況を更新
            update_room_availability(self, self.reservations)
            
        except Exception as e:
            print(f"予約データの読み込み中にエラーが発生しました: {e}")
    
    def reset_room_availability(self):
        """部屋の空室状況を初期値にリセットする"""
        # 初期の部屋空室状況を取得
        self.room_availability_all, self.room_availability_banquet = get_initial_room_availability()

    def check_room_capacity(self, room_name, people_count):
        """部屋の最大収容人数をチェックする"""
        return check_room_capacity(room_name, people_count, self.room_max_capacity)

    def process_reservation(self):
        """予約処理を行う"""
        try:
            # ① 入力値の取得と空白除去
            last = self.last_name.get().strip()
            first = self.first_name.get().strip()
            email_user = self.email.get().strip()
            email_domain = self.combobox_email.get()
            full_email = f"{email_user}{email_domain}"
            check_in = self.check_in.get().strip()
            check_out = self.check_out.get().strip()
            room_name = self.room_name.get().strip()
            people = self.people.get().strip()
            bus_var = self.bus_var.get()
            plan = self.plans.get()  # プラン情報を取得

            # ② 必須項目の入力チェック
            if not last or not first:
                messagebox.showerror("入力エラー", "姓と名は必ず入力してください。")
                return False

            if not email_user:
                messagebox.showerror("入力エラー", "メールアドレスを入力してください。")
                return False

            if not (check_in and check_out and room_name and people):
                messagebox.showerror("入力エラー", "すべての項目を入力してください。")
                return False

            # ③ 日付の妥当性チェック
            check_in_date = datetime.strptime(check_in, "%Y/%m/%d")
            check_out_date = datetime.strptime(check_out, "%Y/%m/%d")
            if check_in_date >= check_out_date:
                messagebox.showerror("日付エラー", "チェックイン日はチェックアウト日より前である必要があります。")
                return False

            # 人数と部屋の最大収容人数をチェック
            people_count = int(people)
            is_valid, max_capacity = self.check_room_capacity(room_name, people_count)
            if not is_valid:
                messagebox.showerror(
                    "人数エラー", 
                    f"選択された部屋「{room_name}」の最大収容人数は{max_capacity}人です。"
                )
                return False

            # ④ 部屋の空室チェックと更新
            if self.banquet_var.get() == "あり":
                rooms_available = self.room_availability_banquet
                # 許可されている部屋かどうか
                if room_name not in rooms_available:
                    messagebox.showerror(
                        "エラー",
                        "宴会の場合、選択できる部屋は「和室28畳（西館）」「和室10畳（西館）」「洋室10畳（西館）」「和洋室7.5畳（西館）」に限定されています。"
                    )
                    return False
                # 空室があるか確認
                if rooms_available[room_name] <= 0:
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
                    return False
            else:
                rooms_available = self.room_availability_all
                if rooms_available.get(room_name, 0) <= 0:
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
                    return False

            # 空室が確認できたので、更新
            rooms_available[room_name] -= 1

            # 料金を計算（チェックイン日とチェックアウト日を考慮）
            banquet_str = "true" if self.banquet_var.get() == "あり" else "false"
            fee = estimate_calculation(banquet_str, people_count, check_in, room_name, plan, check_out)
            fee_str = f"{fee:,}円"

            # ⑤ 予約情報の組み立てと永続化（JSON保存）
            name = f"{last} {first}"
            remarks_text = self.remarks.get("1.0", "end").strip()
            reservation_id = json_storage(
                name, full_email, people, room_name,
                self.banquet_var.get(), check_in, check_out,
                remarks_text, fee_str, bus_var, plan
            )
            print("予約情報が保存されました！")

            # ⑥ 予約完了のメッセージ表示
            if DEMO_MODE:
                messagebox.showinfo("予約完了", f"予約が完了しました！予約ID: {reservation_id}\n開発者メールアドレスにメールを送信しました。")
            else:
                messagebox.showinfo("予約完了", f"予約が完了しました！予約ID: {reservation_id}\nメールを送信しました。")

            # ⑦ メール送信
            email_notification_system(
                email=full_email,          # メールアドレスの値を渡す
                last_name=last,       # 姓を渡す
                banquet_var=self.banquet_var.get(),      # 宴会有無を渡す
                people=people,        # 人数を渡す
                room_name=room_name,  # 部屋名を渡す
                check_in=check_in,    # チェックイン日
                check_out=check_out,  # チェックアウト日
                fee=fee,        # 合計料金を整形
                result_label=self.result_label,      # 結果表示用ラベル
                bus_var=bus_var,       # 送迎の有無
                plan=plan              # 選択されたプラン
            )
            
            # 予約が成功したら入力をリセットし、予約データを再読み込み
            self.reset_input_contains()
            # 予約データを再読み込み
            self.reservations = load_reservations(self.reservations_file)
            
            return True

        except ValueError as e:
            messagebox.showerror("入力エラー", f"入力エラー: {e}")
            return False
        except Exception as e:
            messagebox.showerror("エラー", f"予約処理中にエラーが発生しました: {e}")
            print(f"エラーが発生しました: {e}")
            return False
    
    def open_reservation_manager(self):
        """予約管理画面を開く"""
        reservation_manager = tk.Toplevel(self.master)
        reservation_manager.title("予約管理")
        reservation_manager.geometry("800x600")
        
        # 予約データを再読み込み（最新の状態を確実に取得するため）
        self.reservations = load_reservations(self.reservations_file)
        
        # 予約一覧を表示するTreeview
        columns = ("id", "name", "room", "check_in", "check_out", "plan", "status")
        tree = ttk.Treeview(reservation_manager, columns=columns, show="headings")
        
        # 列の設定
        tree.heading("id", text="予約ID")
        tree.heading("name", text="お客様名")
        tree.heading("room", text="部屋名")
        tree.heading("check_in", text="チェックイン")
        tree.heading("check_out", text="チェックアウト")
        tree.heading("plan", text="プラン")
        tree.heading("status", text="状態")
        
        tree.column("id", width=80)
        tree.column("name", width=150)
        tree.column("room", width=150)
        tree.column("check_in", width=100)
        tree.column("check_out", width=100)
        tree.column("plan", width=150)
        tree.column("status", width=100)
        
        # スクロールバーの設定
        scrollbar = ttk.Scrollbar(reservation_manager, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # ツリービューとスクロールバーの配置
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # 現在の日付
        current_date = datetime.now().strftime("%Y/%m/%d")
        current_date_obj = datetime.strptime(current_date, "%Y/%m/%d")
        
        # 部屋ごとの使用状況を追跡するための辞書
        active_rooms = {}
        
        # 予約データをTreeviewに追加（チェックイン日でソート）
        sorted_reservations = sorted(
            self.reservations, 
            key=lambda r: (
                datetime.strptime(r.get("check_in", "2099/12/31"), "%Y/%m/%d"),
                datetime.strptime(r.get("check_out", "2099/12/31"), "%Y/%m/%d")
            )
        )
        
        for reservation in sorted_reservations:
            reservation_id = reservation.get("id", "")
            name = reservation.get("name", "")
            room_name = reservation.get("room_name", "")
            check_in = reservation.get("check_in", "")
            check_out = reservation.get("check_out", "")
            plan = reservation.get("plan", "なし")
            
            # 予約状態の判定（部屋の使用状況を考慮）
            status = get_reservation_status(reservation, current_date_obj, active_rooms)
            
            tree.insert("", tk.END, values=(reservation_id, name, room_name, check_in, check_out, plan, status))
        
        # ボタンフレーム
        button_frame = tk.Frame(reservation_manager)
        button_frame.pack(pady=10)
        
        # チェックアウト処理ボタン
        def handle_checkout():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("エラー", "チェックアウトする予約を選択してください。")
                return
            
            item_values = tree.item(selected_item[0], "values")
            reservation_id = item_values[0]
            status = item_values[6]  # statusは7番目の列
            
            if status == "チェックアウト済":
                messagebox.showinfo("情報", "この予約はすでにチェックアウト済みです。")
                return
            
            # チェックアウト処理を実行
            if process_checkout(reservation_id, self.reservations, self.reservations_file):
                # 部屋の空室状況を更新
                update_room_availability(self, self.reservations)
                
                # ツリービューを更新
                tree.item(selected_item[0], values=(
                    item_values[0], item_values[1], item_values[2], 
                    item_values[3], item_values[4], item_values[5], "チェックアウト済"
                ))
                
                messagebox.showinfo("成功", "チェックアウト処理が完了しました。")
            else:
                messagebox.showerror("エラー", "予約データの更新に失敗しました。")
        
        checkout_button = tk.Button(
            button_frame, 
            text="チェックアウト処理", 
            command=handle_checkout,
            bg="#e74c3c", 
            fg="white"
        )
        checkout_button.pack(side=tk.LEFT, padx=5)
        
        # 予約状況更新ボタン
        def refresh_reservations():
            # ツリービューをクリア
            for item in tree.get_children():
                tree.delete(item)
            
            # 予約データを再読み込み
            self.reservations = load_reservations(self.reservations_file)
            
            # 部屋の空室状況を更新
            update_room_availability(self, self.reservations)
            
            # 部屋ごとの使用状況を追跡するための辞書をリセット
            active_rooms.clear()
            
            # 予約データをツリービューに追加（チェックイン日でソート）
            sorted_reservations = sorted(
                self.reservations, 
                key=lambda r: (
                    datetime.strptime(r.get("check_in", "2099/12/31"), "%Y/%m/%d"),
                    datetime.strptime(r.get("check_out", "2099/12/31"), "%Y/%m/%d")
                )
            )
            
            for reservation in sorted_reservations:
                reservation_id = reservation.get("id", "")
                name = reservation.get("name", "")
                room_name = reservation.get("room_name", "")
                check_in = reservation.get("check_in", "")
                check_out = reservation.get("check_out", "")
                plan = reservation.get("plan", "なし")
                
                # 予約状態の判定（部屋の使用状況を考慮）
                status = get_reservation_status(reservation, current_date_obj, active_rooms)
                
                tree.insert("", tk.END, values=(reservation_id, name, room_name, check_in, check_out, plan, status))
            
            messagebox.showinfo("情報", "予約状況を更新しました。")
        
        refresh_button = tk.Button(
            button_frame, 
            text="予約状況更新", 
            command=refresh_reservations,
            bg="#2ecc71", 
            fg="white"
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 閉じるボタン
        close_button = tk.Button(
            button_frame, 
            text="閉じる", 
            command=reservation_manager.destroy,
            bg="#3498db", 
            fg="white"
        )
        close_button.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()
