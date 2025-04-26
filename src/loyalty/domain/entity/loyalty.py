from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from loyalty.domain.shared_types import Gender


@dataclass
class Loyalty:
    # Информация о программе лояльности
    loyalty_id: UUID
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime
    
    money_per_bonus: int  # Минимальная cумма для начисления одного бонуса
    
    min_age: int  # Минимальный возраст клинта для участия в программе лояльности
    max_age: int  # Максимальный возраст клиента для участия в программе лояльности
    
    gender: Gender | None = None
    
    @property
    def is_active(self) -> bool:
        current_datetime = datetime.now()
        
        if self.starts_at < current_datetime < self.ends_at:
            return True
        
        return False
            
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
