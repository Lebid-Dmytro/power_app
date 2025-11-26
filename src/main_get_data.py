import asyncio

from src.tasks import get_data_task


async def run_get_data() -> None:
    print("Сервіс 'get_data' запущено. Готуємо базу даних...")
    try:
        saved = await get_data_task()
        if saved == 0:
            print("Попередження: дані не були отримані.")
            return

        print(f"Усі дані ({saved}) успішно збережено у базу даних.")
    except Exception as e:
        print("Помилка в get_data:", e)
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_get_data())
