from tkinter import messagebox
import tkinter as tk
def reservation_confirmed(last_name,email, check_in,check_out,room_name,people,room_availability,room_prices,banquet_var):
            name = last_name.get() 
            email = email.get()
            checkin = check_in.get()
            checkout = check_out.get()
            room = room_name.get()
            num_people = people.get()
            
            if name and email and checkin and checkout and room and num_people:
                available = room_availability.get(room, 0)
                if available > 0:
                    room_availability[room] -= 1  # 空室があるので、部屋の空きを1つ減らす
                    price = room_prices.get(room, 0) * int(num_people)
                    banquet_text = "あり" if self.banquet_var.get() else "なし"
                    if banquet_var.get():
                        price += 22400
                    # reservation = f"{name}: {checkin} - {checkout}, {room} ({price}円), 人数: {num_people}, 宴会: {banquet_text}"
                    # reservations.append(reservation)
                    # self.reservations_listbox.insert(tk.END, reservation)
                    # send_email メソッドでメール送信 (ここでは詳細は省略)
                    # self.send_email(name, email, checkin, checkout, room, price, num_people, banquet_text)
                    messagebox.showinfo("予約完了", "予約が完了しました！メールを送信しました。")
                else:
                    # 空きがない場合は「満室です」というエラーメッセージを表示
                    messagebox.showerror("満室", "申し訳ありません。選択された部屋は満室です。")
            else:
                messagebox.showerror("エラー", "すべての項目を入力してください")