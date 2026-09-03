from __future__ import annotations

from apps.web.bills.schemas import (
    BillDetailResponse,
    BillSearchResponse,
    BillSearchRequest,
    BillSummary,
)


class BillsService:
    """
    Business logic for parliamentary bills.
    """

    def __init__(
        self,
        bills_client,
    ):
        self.client = bills_client

    async def search(
        self,
        request: BillSearchRequest,
    ) -> BillSearchResponse:

        results = await self.client.search(
            query=request.query,
            limit=request.limit,
        )

        summaries = []

        for bill in results:

            summaries.append(
                BillSummary(
                    id=bill.id,
                    title=bill.title,
                    description=bill.description,
                    status=bill.status,
                    introduced_date=(
                        bill.introduced_date
                    ),
                    sponsor=bill.sponsor,
                    source_url=bill.source_url,
                )
            )

        return BillSearchResponse(
            query=request.query,
            results=summaries,
        )

    async def get(
        self,
        bill_id: str,
    ) -> BillDetailResponse:

        # This method can later call the
        # Parliament API directly.

        results = await self.client.search(
            query=bill_id,
            limit=1,
        )

        if not results:

            raise ValueError(
                f"Bill not found: {bill_id}"
            )

        bill = results[0]

        return BillDetailResponse(
            id=bill.id,
            title=bill.title,
            description=bill.description,
            status=bill.status,
            introduced_date=bill.introduced_date,
            sponsor=bill.sponsor,
            source_url=bill.source_url,
            house=bill.house,
            subjects=bill.subjects,
            stages=[
                stage.model_dump()
                for stage in bill.stages
            ],
        )
