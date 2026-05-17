import uuid

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.monitor.services import MonitorService
from src.probe.models import Probe


class ProbeService:
    def __init__(self, session: AsyncSession, monitor_service: MonitorService) -> None:
        self.session = session
        self.monitor_service = monitor_service

    async def get_latest_probes(
        self, monitor_id: uuid.UUID, user_id: uuid.UUID, limit: int = 50
    ):
        await self.monitor_service.get_monitor_by_id(monitor_id, user_id)
        stmt = await self.session.execute(
            select(Probe)
            .where(Probe.monitor_id == monitor_id)
            .order_by(desc(Probe.timestamp))
            .limit(limit)
        )
        probes = stmt.scalars().all()
        if not probes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No probe history found for this monitor",
            )
        return {
            "monitor_id": monitor_id,
            "latest_status": probes[0].is_up,
            "history": probes,
        }
