from fastapi import FastAPI, HTTPException

from src.tasks import get_data_task, print_data_task


app = FastAPI(
    title="Population Aggregation Service",
    description="Асинхронний сервіс для завантаження даних про населення країн та "
                "агрегації їх по регіонах.",
    version="1.0.0",
)


@app.post("/get-data", summary="Завантажити та зберегти свіжі дані з Wikipedia")
async def get_data():
    saved = await get_data_task()
    if saved == 0:
        raise HTTPException(status_code=500, detail="Дані не були отримані або не вдалося їх зберегти.")
    return {"status": "ok", "rows_saved": saved}


@app.get("/regions", summary="Отримати агреговані дані по регіонах")
async def get_regions():
    data = await print_data_task()
    if not data:
        raise HTTPException(status_code=404, detail="Немає даних у базі. Спочатку виконайте завантаження.")
    return data
