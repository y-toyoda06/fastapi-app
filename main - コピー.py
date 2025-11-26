from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import google.generativeai as genai

# データベースの設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemModel(Base): # Baseを継承させるとDB判定（テーブルとして登録，CREATE TABLE）
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    is_offer = Column(Boolean, default=False)
    
Base.metadata.create_all(bind=engine)    # Baseを継承しているクラスのテーブルを作成

class ItemCreate(BaseModel): # BaseModelは型のvalidation，これがDTOの入力
    name: str
    price: int
    is_offer: bool = None

class ItemResponse(ItemCreate): # これがDTOの出力
    id: int
    ai_comment: str = None
    
    class Config:
        orm_mode = True
        
        
app = FastAPI()

GOOGLE_API_KEY = "AIzaSyDT6f0RHaZx7ocE5WMzg9mgHBYEcsliomE"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


    
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    
    # AI処理を try-except で囲む（防波堤を作る）
    try:
        prompt = f"ユーザーが「{item.name}」というタスクを登録しました。関西弁で短くツッコミか励ましを入れて。"
        response = model.generate_content(prompt)
        ai_comment = response.text
    except Exception as e:
        # エラーが起きてもアプリを止めず、ログに出してあげる
        print(f"AIエラー発生: {e}")
        ai_comment = "（AIはお休み中です...）"
        
    db_item = ItemModel(name=item.name, price=item.price, is_offer=item.is_offer)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    db_item.ai_comment = ai_comment
    return db_item

@app.get("/items/", response_model=list[ItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(ItemModel).offset(skip).limit(limit).all()
    return items