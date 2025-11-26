import asyncio
from typing import Optional, Any

from src.tasks import print_data_task


def format_number(n: Optional[Any]) -> str:
    if n is None:
        return "Н/Д"
    if isinstance(n, float):
        return f"{n:+.2f}%"
    try:
        return f"{int(n):,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(n)


def print_region_data(data: list[dict]):
    for item in data:
        print("-" * 50)
        region_name = item.get("Region", "Невідомий регіон")
        print(f"РЕГІОН: {region_name}")
        print(f"Загальне населення: {format_number(item.get('Total Population'))}")
        print("\nНайбільша країна:")
        print(f"  Країна: {item.get('Max Country Name', 'Н/Д')}")
        print(f"  Населення: {format_number(item.get('Max Country Population'))}")
        print("\nНайменша країна:")
        print(f"  Країна: {item.get('Min Country Name', 'Н/Д')}")
        print(f"  Населення: {format_number(item.get('Min Country Population'))}")
    print("-" * 50)


async def run_print_data():
    print("Сервіс 'print_data' запущено. Читаємо дані...")
    try:
        aggregated = await print_data_task()
        if not aggregated:
            print("⚠️ Немає даних для виведення. Спочатку виконайте 'get_data'.")
            return

        print_region_data(aggregated)
    except Exception as e:
        print("Помилка в print_data:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_print_data())
