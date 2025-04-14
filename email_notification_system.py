import traceback
from mail import send_mail
from datetime import datetime

# デモ用の開発メンバーのメールアドレス（実際のアドレスに変更してください）
DEVELOPER_EMAILS = [
    "a.seki.sys24@morijyobi.ac.jp",  # 開発者1
    "m.kudou.sys24@morijyobi.ac.jp",  # 開発者2（必要に応じて追加）
    "s.sato.sys24@morijyobi.ac.jp",  # 開発者3（必要に応じて追加）
]

# デモモード（True: 開発者にのみ送信、False: ユーザーが入力したアドレスに送信）
DEMO_MODE = True

def email_notification_system(email, last_name, banquet_var, people, room_name, check_in, check_out, fee, result_label, bus_var=None, plan="なし"):
    """
    メール通知システム
    mail.pyのsend_mail関数を使用してメールを送信
    """
    try:
        # 宴会の有無に応じたメッセージ
        banquet_message = "あり" if banquet_var == "あり" else "なし"
        
        # 送迎の有無に応じたメッセージ
        bus_message = "あり" if bus_var == "あり" else "なし"
        
        # 宿泊日数を計算
        check_in_date = datetime.strptime(check_in, "%Y/%m/%d")
        check_out_date = datetime.strptime(check_out, "%Y/%m/%d")
        nights = (check_out_date - check_in_date).days
        nights_message = f"{nights}泊"

        # メール本文の作成（HTML形式）
        body = f"""
        <html>
        <body>
        <p>{last_name} 様</p>
        <p>この度は八幡平ハイツをご予約いただき、誠にありがとうございます。<br>
        以下の内容でご予約を承りました。</p>
        
        <h3>【ご予約内容】</h3>
        <ul>
            <li>お部屋: {room_name}</li>
            <li>宿泊人数: {people}名</li>
            <li>チェックイン日: {check_in}</li>
            <li>チェックアウト日: {check_out}</li>
            <li>宿泊日数: {nights_message}</li>
            <li>宴会: {banquet_message}</li>
            <li>送迎: {bus_message}</li>
            <li>プラン: {plan}</li>
            <li>料金: {fee:,}円</li>
        </ul>
        """

        # デモモードの場合、開発者向けの追加情報を表示
        if DEMO_MODE:
            body += f"""
            <hr>
            <h3>【デモモード - 開発者向け情報】</h3>
            <p>これはデモモードでのメール送信です。実際の運用では、以下のアドレスにメールが送信されます：</p>
            <p><strong>お客様メールアドレス:</strong> {email}</p>
            """

        body += f"""
        <p>ご不明な点がございましたら、お気軽にお問い合わせください。<br>
        お客様のお越しを心よりお待ちしております。</p>
        
        <hr>
        <p>
        <strong>八幡平ハイツ</strong><br>
        〒028-7302<br>
        岩手県八幡平市松尾寄木1-590-4<br>
        TEL: 0195-78-2121<br>
        FAX: 0195-78-2041<br>
        Email: hachimantai_haitu.hotel@gmail.com
        </p>
        </body>
        </html>
        """

        # メールの送信先を決定
        recipients = DEVELOPER_EMAILS if DEMO_MODE else [email]
        
        # 各受信者にメールを送信
        for recipient in recipients:
            subject = "【八幡平ハイツ】ご予約ありがとうございます" + (" [デモモード]" if DEMO_MODE else "")
            send_mail(recipient, subject, body)

        # 送信成功メッセージ
        if DEMO_MODE:
            success_message = f"開発者メールアドレスにメールを送信しました。"
        else:
            success_message = f"メールを送信しました。"
            
        result_label.config(text=success_message, fg="green")
        print(success_message)
        return True

    except Exception as e:
        # エラーメッセージ
        error_message = f"メール送信エラー: {str(e)}"
        result_label.config(text=error_message, fg="red")
        print(error_message)
        print(traceback.format_exc())  # 詳細なエラー情報を出力
        return False
