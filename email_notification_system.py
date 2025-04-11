import tkinter as tk
from tkinter import ttk  # ttkをtkinterからインポート
from mail import send_mail  # あなたの独自のメール送信モジュール

# 送信ボタンが押されたときに予約情報を収集してメール送信
def email_notification_system(email, last_name, banquet_var, people, room_name, result_label, check_in, check_out, fee, bus_var):
    # 予約情報を取得し、メールの本文を生成
    try:
        # 必要な情報を整形して取得
        to = email.strip()
        name = last_name.strip() if last_name else "未入力"
        bus = bus_var.get()  # 送迎オプション
        subject = "ご予約確定のお知らせ"

        # 固定メッセージ部分
        fixed_message = f"""{name}様\n\nこの度はご予約ありがとうございます。\n以下の通り、予約内容をご確認ください。\n\n"""

        # 予約情報を整形
        reservation_info = f"""\
【予約情報】

氏名: {name}
宴会有無: {"あり" if banquet_var == 'true' else "なし"}
人数: {people.strip()}名
部屋: {room_name.strip()}
チェックイン日: {check_in.strip()}
チェックアウト日: {check_out.strip()}
見積もり料金: {fee:,}円
送迎: {bus}

またのご利用をお待ちしております。
"""

        # メール本文を生成
        body = fixed_message + reservation_info
        print(body)  # デバッグ用に内容確認

        # メール送信
        send_mail(to, subject, body)  # メール送信処理を実行
        result_label.config(text="メールを送信しました！", fg="green")
    
    except Exception as e:
        # エラー処理
        result_label.config(text=f"送信に失敗しました: {str(e)}", fg="red")