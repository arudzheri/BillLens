from .ask import router as ask_router
from .bills import router as bills_router
from .dashboard import (
    router as dashboard_router,
)
from .legislation import (
    router as legislation_router,
)
from .mps import router as mps_router


__all__ = [
    "ask_router",
    "bills_router",
    "dashboard_router",
    "legislation_router",
    "mps_router",
]
