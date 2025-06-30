import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from controllers import api_router


app = FastAPI(
    description="API для Сервісу Прокату Велосипедів. Дозволяє керувати велосипедами, локаціями, користувачами, прокатами та знижками.",
    docs_url="/docs"
)

app.include_router(api_router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8900)
