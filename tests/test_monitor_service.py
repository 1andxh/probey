import pytest

from src.exceptions import DuplicateMonitorError
from src.monitor.schemas import MonitorCreate
from src.monitor.services import MonitorService


@pytest.mark.asyncio
async def test_create_monitor_success(db_session, test_user):
    service = MonitorService(db_session)

    data = MonitorCreate(
        name="Test-monitor", url="https://example.com", check_interval=30
    )

    monitor = await service.create_monitor(data, test_user.id)

    assert monitor.id is not None
    assert monitor.url == "https://example.com"
    assert monitor.name == "Test-monitor"
    assert monitor.owner_id == test_user.id


@pytest.mark.asyncio
async def test_create_monitor_duplicate(db_session, test_user):
    service = MonitorService(db_session)

    data = MonitorCreate(
        name="Test-monitor", url="https://example.com", check_interval=30
    )

    await service.create_monitor(data, test_user.id)

    with pytest.raises(DuplicateMonitorError):
        await service.create_monitor(data, test_user.id)


@pytest.mark.asyncio
async def test_create_monitor_normalizes_url(db_session, test_user):
    service = MonitorService(db_session)

    data = MonitorCreate(
        name="Test-monitor", url=" HTTPS://Example.com/ ", check_interval=30
    )

    monitor = await service.create_monitor(data, test_user.id)

    assert monitor.url == "https://example.com"
