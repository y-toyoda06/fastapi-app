# AI Product Manager (AI商品管理API)

FastAPIとGoogle Gemini (生成AI) を活用した，商品在庫管理APIです．
商品を登録すると，AIがその商品の価格や名前に基づいて，自動でキャッチコピーを関西弁で生成・保存します．

##  デモ (Swagger UI)
ブラウザからAPIの動作をテストできます．
**[https://fastapi-app-60i0.onrender.com/docs](https://fastapi-app-60i0.onrender.com/docs)**

## 使用技術 

- **Language:** Python 
- **Framework:** FastAPI
- **Database:** SQLite (SQLAlchemy)
- **AI Model:** Google Gemini API (gemini-2.5-flash)
- **Deployment:** Render
- **Library:** Pydantic (v2), python-dotenv

##  主な機能
1. **商品登録 (Create):** 商品名と価格を送信すると，DB保存と同時にAIがキャッチコピーを生成．
2. **商品一覧取得 (Read):** ページネーション対応．AIが生成したコメントも合わせて取得．
3. **データ永続化:** SQLAlchemyを用いたDB設計．

## ローカルでの実行方法 

```bash
# 1. リポジトリをクローン
git clone [https://github.com/y-toyoda/fastapi-app.git](https://github.com/y-toyoda/fastapi-app.git)
cd fastapi-app

# 2. 仮想環境の作成と有効化 (Windows)
python -m venv venv
.\venv\Scripts\activate

# 3. 依存ライブラリのインストール
pip install -r requirements.txt

# 4. 環境変数の設定 (.envファイルを作成)
# GOOGLE_API_KEY="あなたのAPIキー" を記述

# 5. サーバー起動
uvicorn main:app --reload
```


##  今後の展望 (Roadmap)

以下の実装を計画しています.

- **認証機能の実装:**
  - セキュリティ向上のため，ユーザー登録・ログイン認証機能を実装し，特定のエンドポイントを保護する。
  

-  **CRUD機能の完全実装:**
  - 現在の Create (登録)・Read (参照) 機能に加え，Update (更新)・Delete (削除) 機能を実装し，商品データのライフサイクル管理を完結させる．