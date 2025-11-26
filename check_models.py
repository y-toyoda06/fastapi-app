import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyDT6f0RHaZx7ocE5WMzg9mgHBYEcsliomE"
genai.configure(api_key=GOOGLE_API_KEY)

print("=== あなたが使えるモデル一覧 ===")
try:
    for m in genai.list_models():
        # "generateContent" (会話機能) が使えるモデルだけ表示
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"一覧取得エラー: {e}")