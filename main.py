import openai
import requests
import random
import os
from datetime import datetime

# --- 設定を環境変数から読み込み ---
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
WORDPRESS_URL = os.environ["WORDPRESS_URL"]
WORDPRESS_USER = os.environ["WORDPRESS_USER"]
WORDPRESS_APP_PASSWORD = os.environ["WORDPRESS_APP_PASSWORD"]

# --- 記者情報 ---
reporters = [
    {"name": "キリンのジェシカ", "theme": "グルメニュース"},
    {"name": "ヒツジのメール", "theme": "政治ニュース"},
    {"name": "ネズミのタップ", "theme": "ちょっとした事件や噂"},
    {"name": "ウサギのラル", "theme": "芸能・アイドルニュース"},
    {"name": "シカのゲイル", "theme": "スポーツ・競技イベント"},
    {"name": "リスのナッツ", "theme": "文化・クラフト"},
    {"name": "イルカのマリン", "theme": "自然・環境の話題"},
]

reporter = random.choice(reporters)

# --- ChatGPTに記事生成 ---
openai.api_key = OPENAI_API_KEY

prompt = f"""
あなたは架空の島「アニマリア」に住む、動物の記者「{reporter['name']}」です。
島の住民は可愛くデフォルメされた動物たちで、8000匹が日本語で暮らしています。
今日の{reporter['theme']}に関するニュース記事を、日本の新聞ブログ風に、500〜2000字で書いてください。
楽しく前向きな内容で、不幸な事件や事故は含まないでください。
記事には見出し（10〜20字）と本文、最後に「記者名：{reporter['name']}」と入れてください。
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9
)

content_raw = response.choices[0].message.content
lines = content_raw.strip().split("\n")
title = lines[0].strip().replace("見出し：", "").strip()
content = "\n".join(lines[1:]).strip()

# --- WordPressへ投稿 ---
post = {
    "title": title,
    "content": content,
    "status": "publish"
}

res = requests.post(
    WORDPRESS_URL,
    auth=(WORDPRESS_USER, WORDPRESS_APP_PASSWORD),
    json=post
)

if res.status_code == 201:
    print("✅ 投稿成功！")
else:
    print("⚠️ 投稿失敗:", res.status_code)
    print(res.text)
