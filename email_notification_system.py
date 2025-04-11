import tkinter as tk
from tkinter import ttk  # ttkをtkinterからインポート
from mail import send_mail

# 送信ボタンが押されたときに予約情報を収集してメール送信

def email_notification_system(email, last_name, banquet_var, people, room_name, result_label,check_in, check_out, fee, bus_var):
    # Tkinterフォームから情報を取得
    to = email
    name = last_name
    bus = bus_var
    
    # 件名を自動設定
    subject = "ご予約確定のお知らせ"

    # 固定の文面を定義（改行を含めて整形）
    fixed_message = f"""
{name}様

この度はご予約ありがとうございます。
以下の通り、予約内容をご確認ください。\n

"""

    # 予約情報を整形（項目ごとに改行を追加）
    reservation_info = f"""
【予約情報】\n

氏名: {name}\n
宴会有無: {"あり" if banquet_var == 'true' else "なし"} \n
人数: {people}名  \n
部屋: {room_name}  \n
チェックイン日: {check_in}  \n
チェックアウト日: {check_out}  \n
見積もり料金: {fee:,}円  \n
送迎：{bus_var.get()}\n


またのご利用をお待ちしております。
"""

    # メール本文を結合
    body = fixed_message + reservation_info

    try:
        # メール送信処理
        send_mail(to, subject, body)
        result_label.config(text="メールを送信しました！", fg="green")  # 成功の表示
    except Exception as e:
        # エラーハンドリング
        result_label.config(text=f"送信に失敗しました: {str(e)}", fg="red")  # 失敗の表示