from __future__ import annotations

from api.assigned_papers_error_mapper import map_assigned_papers_error
from services.assigned_papers_service import AssignedPapersService


def list_assigned_papers(
    service: AssignedPapersService,
    reviewer_id: str | None,
    trace_id: str | None = None,
) -> tuple[int, dict | list[dict]]:
    result = service.list_assigned_papers(reviewer_id=reviewer_id, trace_id=trace_id)

    if result.status == "ok":
        return 200, [
            {"paperId": paper.paper_id, "title": paper.title}
            for paper in (result.papers or [])
        ]

    if result.status == "empty":
        return 200, {"message": result.message, "papers": []}

    return map_assigned_papers_error(result)
