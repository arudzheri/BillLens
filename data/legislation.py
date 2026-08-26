from __future__ import annotations

import httpx

from billlens.models import (
    Legislation,
    LegislationSection,
)


class LegislationClient:

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

    async def get(
        self,
        legislation_id: str,
    ) -> Legislation:

        endpoint = (
            f"{self.base_url}"
            f"/legislation/{legislation_id}"
        )

        async with httpx.AsyncClient(
            timeout=self.timeout
        ) as client:

            response = await client.get(
                endpoint
            )

            response.raise_for_status()

            data = response.json()

        return self._parse(data)

    @staticmethod
    def _parse(
        data: dict,
    ) -> Legislation:

        sections = []

        for item in data.get(
            "sections",
            [],
        ):

            sections.append(
                LegislationSection(
                    id=str(
                        item.get("id", "")
                    ),
                    title=item.get(
                        "title",
                        "",
                    ),
                    number=item.get(
                        "number"
                    ),
                    text=item.get(
                        "text",
                        "",
                    ),
                    source_url=item.get(
                        "url"
                    ),
                )
            )

        return Legislation(
            id=str(
                data.get(
                    "id",
                    "",
                )
            ),
            title=data.get(
                "title",
                "",
            ),
            year=data.get("year"),
            legislation_type=data.get(
                "type"
            ),
            status=data.get(
                "status"
            ),
            description=data.get(
                "description"
            ),
            source_url=data.get(
                "url"
            ),
            sections=sections,
        )
