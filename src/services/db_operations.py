from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List, Dict, Any, Optional

from src.models import Region, Country


class DBOperations:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_population_data(self, parsed_rows: List[Dict[str, Any]]):
        for row in parsed_rows:
            region_name = (row.get("region_name") or "").strip()
            country_name = (row.get("country_name") or "").strip()
            population = int(row.get("population") or 0)

            if not region_name or not country_name:
                continue

            q = await self.session.execute(select(Region).where(Region.name == region_name))
            region: Optional[Region] = q.scalars().first()

            if not region:
                region = Region(name=region_name)
                self.session.add(region)
                await self.session.flush()

            q2 = await self.session.execute(select(Country).where(Country.name == country_name))
            country: Optional[Country] = q2.scalars().first()

            if country:
                country.population = population
                country.region = region
            else:
                country = Country(name=country_name, population=population, region=region)
                self.session.add(country)

        await self.session.commit()

    async def get_aggregated_region_data(self) -> List[Dict[str, Any]]:
        sql = text(
            """
            SELECT
                r.name AS "Region",
                COALESCE(SUM(c.population), 0) AS "Total Population",
                (
                    SELECT c2.name
                    FROM countries c2
                    WHERE c2.region_id = r.id
                    ORDER BY c2.population DESC
                    LIMIT 1
                ) AS "Max Country Name",
                (
                    SELECT c2.population
                    FROM countries c2
                    WHERE c2.region_id = r.id
                    ORDER BY c2.population DESC
                    LIMIT 1
                ) AS "Max Country Population",
                (
                    SELECT c3.name
                    FROM countries c3
                    WHERE c3.region_id = r.id
                    ORDER BY c3.population ASC
                    LIMIT 1
                ) AS "Min Country Name",
                (
                    SELECT c3.population
                    FROM countries c3
                    WHERE c3.region_id = r.id
                    ORDER BY c3.population ASC
                    LIMIT 1
                ) AS "Min Country Population"
            FROM regions r
            JOIN countries c ON c.region_id = r.id
            GROUP BY r.id, r.name
            ORDER BY r.name;
            """
        )

        res = await self.session.execute(sql)
        rows = res.mappings().all()

        result: List[Dict[str, Any]] = []
        for row in rows:
            result.append(
                {
                    "Region": row["Region"],
                    "Total Population": row["Total Population"],
                    "Max Country Name": row["Max Country Name"],
                    "Max Country Population": row["Max Country Population"],
                    "Min Country Name": row["Min Country Name"],
                    "Min Country Population": row["Min Country Population"],
                }
            )
        return result
