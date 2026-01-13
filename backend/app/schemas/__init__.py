"""
Schemas do sistema - exportação centralizada
"""

# Auth schemas (principal)
from app.schemas.auth import (
    Token,
    TokenData,
    UserLogin,
    UserCreate,
    UserResponse
)

# User schemas (compatibilidade - pode ser removido se não usado)
try:
    from app.schemas.user import (
        UserBase as UserBaseLegacy,
        User as UserLegacy,
        Token as TokenLegacy
    )
except ImportError:
    UserBaseLegacy = None
    UserLegacy = None
    TokenLegacy = None

# Employee schemas
from app.schemas.employee import (
    EmployeeBase,
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse
)

# Access log schemas
from app.schemas.access_log import (
    AccessLogBase,
    AccessLog,
    AccessLogResponse
)

__all__ = [
    # Auth (principal)
    "Token",
    "TokenData",
    "UserLogin",
    "UserCreate",
    "UserResponse",
    # Employee
    "EmployeeBase",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "EmployeeListResponse",
    # Access Log
    "AccessLogBase",
    "AccessLog",
    "AccessLogResponse",
]
