from dataclasses import dataclass

from loyalty.application.common.gateway.statistic import StatisticsGateway
from loyalty.application.statistic.dto import Statistics

DEFAULT_LOYALTIES_PAGE_LIMIT = 10


@dataclass(slots=True, frozen=True)
class ReadStatistics:
    gateway: StatisticsGateway

    def execute(self) -> Statistics:
        total_payments = self.gateway.get_total_payments()
        total_clients = self.gateway.get_total_clients()
        total_businesses = self.gateway.get_total_businesses()

        return Statistics(
            total_payments=total_payments,
            total_clients=total_clients,
            total_businesses=total_businesses,
        )
