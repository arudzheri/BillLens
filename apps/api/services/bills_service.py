from __future__ import annotations

from typing import Any

from apps.web.bills.schemas import (
    BillDetailResponse,
    BillSearchRequest,
    BillSearchResponse,
    BillSummary,
)


class BillsService:
    """
    Application service for parliamentary bills.
    """

    def __init__(self, bills_client: Any):
        self.client = bills_client

    async def search(
        self,
        request: BillSearchRequest,
    ) -> BillSearchResponse:

        results = await self.client.search(
            query=request.query,
            limit=request.limit,
        )

        bills = []

        for bill in results:

            bills.append(
                BillSummary(
                    id=bill.id,
                    title=bill.title,
                    description=getattr(
                        bill,
                        "description",
                        None,
                    ),
                    status=getattr(
                        bill,
                        "status",
                        None,
                    ),
                    introduced_date=getattr(
                        bill,
                        "introduced_date",
                        None,
                    ),
                    sponsor=getattr(
                        bill,
                        "sponsor",
                        None,
                    ),
                    source_url=getattr(
                        bill,
                        "source_url",
                        None,
                    ),
                )
            )

        return BillSearchResponse(
            query=request.query,
            results=bills,
        )

    async def get(
        self,
        bill_id: str,
    ) -> BillDetailResponse:

        bill = await self.client.get(
            bill_id
        )

        if bill is None:
            raise ValueError(
                f"Bill not found: {bill_id}"
            )

        return BillDetailResponse(
            id=bill.id,
            title=bill.title,
            description=getattr(
                bill,
                "description",
                None,
            ),
            status=getattr(
                bill,
                "status",
                None,
            ),
            introduced_date=getattr(
                bill,
                "introduced_date",
                None,
            ),
            sponsor=getattr(
                bill,
                "sponsor",
                None,
            ),
            source_url=getattr(
                bill,
                "source_url",
                None,
            ),
            house=getattr(
                bill,
                "house",
                None,
            ),
            subjects=getattr(
                bill,
                "subjects",
                [],
            ),
            stages=[
                stage.model_dump()
                if hasattr(stage, "model_dump")
                else stage
                for stage in getattr(
                    bill,
                    "stages",
                    [],
                )
            ],
        )
