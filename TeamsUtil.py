import json
import requests


class TeamsUtil:
    # Teamsに投稿します。
    @classmethod
    def post_to_teams(cls, title, message, uri):
        # リクエストボディを作成
        text = {
            "@context": "https://schema.org/extensions",
            "@type": "MessageCard",
            "themeColor": "0072C6",
            "title": title,
            "text": message,
        }
        data = json.dumps(text)
        # リクエストを送信
        requests.post(uri, data)
