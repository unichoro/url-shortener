import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from src.db import conn as db_conn
import base64

app = FastAPI()


# 데이터베이스 연결
@app.on_event("startup")
async def startup():
    db_conn  # 이 부분은 db.py의 코드를 실행하여 데이터베이스 연결을 설정합니다.

@app.get("/")
def read_root():
    message = {
        "message": "Welcome to the URL shortener API!"
    }
    return JSONResponse(content=message, status_code=200)

@app.post("/")
def shorten_url(original_url: str):
    # 단축 URL 생성 로직
    short_slug=base64.urlsafe_b64encode(original_url.encode()).decode()[:6]
    cursor = db_conn.cursor()
    cursor.execute("SELECT original_url FROM url_shortener WHERE original_url = ?", (original_url,))
    result = cursor.fetchone()
    db_conn.commit()
    if not (original_url.startswith("http://") or original_url.startswith("https://")):
        response_httperror = {
            "error": "Invalid URL format"
        }
        return JSONResponse(content=response_httperror, status_code=400)
    
    elif result!=None:
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM url_shortener WHERE original_url = ?", (original_url,))
        result2 = cursor.fetchone()
        response_content= {
            "original_url": result2[0],
            "short_slug": result2[1],
            "short_url": result2[2]
        }
        return JSONResponse(content=response_content, status_code=200)
    else:
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO url_shortener (original_url, short_slug, short_url) VALUES (?, ?, ?)", (original_url, short_slug, "http://localhost:8000/" + short_slug))
        db_conn.commit()
        response_content2= {"original_url": original_url, "short_slug":short_slug, 'short_url': "http://localhost:8000/" + short_slug}
        return JSONResponse(content=response_content2, status_code=201)


# 리다이렉트 함수
@app.get("/{short_slug}")
async def redirect_to_original_url(short_slug: str):
    # 데이터베이스에서 단축 URL에 해당하는 원본 URL 조회
    cursor = db_conn.cursor()
    cursor.execute("SELECT original_url FROM url_shortener WHERE short_slug = ?", (short_slug,))
    result = cursor.fetchone()
    db_conn.commit()
    
    # 조회된 결과가 없으면 404 에러 반환
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    # 원본 URL로 리다이렉트
    original_url = result[0]
    response = RedirectResponse(url=original_url)
    return response



if __name__ == "__main__":
    # Run the app
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )