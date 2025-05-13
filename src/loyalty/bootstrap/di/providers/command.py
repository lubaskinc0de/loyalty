from dishka import Provider, Scope, provide, provide_all

from loyalty.application.bonus.discount import CalcDiscount
from loyalty.application.bonus.read import ReadBonuses
from loyalty.application.business.create import CreateBusiness
from loyalty.application.business.read import ReadBusiness
from loyalty.application.business_branch.create import CreateBusinessBranch
from loyalty.application.business_branch.delete import DeleteBusinessBranch
from loyalty.application.business_branch.read import ReadBusinessBranch, ReadBusinessBranches
from loyalty.application.business_branch.update import UpdateBusinessBranch
from loyalty.application.client.create import CreateClient
from loyalty.application.client.read import ReadClient
from loyalty.application.loyalty.create import CreateLoyalty
from loyalty.application.loyalty.delete import DeleteLoyalty
from loyalty.application.loyalty.read import ReadLoyalties, ReadLoyalty
from loyalty.application.loyalty.update import UpdateLoyalty
from loyalty.application.membership.create import CreateMembership
from loyalty.application.membership.delete import DeleteMembership
from loyalty.application.membership.read import ReadMembership, ReadMemberships
from loyalty.application.payment.create import CreatePayment
from loyalty.application.payment.delete import DeletePayment
from loyalty.application.ping import Ping
from loyalty.application.user.create import CreateUser
from loyalty.application.user.read import ReadUser
from loyalty.presentation.web.controller.login import WebLogin
from loyalty.presentation.web.controller.logout import Logout


class CommandProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser, scope=Scope.ACTION)
    commands = provide_all(
        Ping,
        ReadClient,
        CreateClient,
        CreateBusiness,
        ReadBusiness,
        ReadBusinessBranch,
        ReadBusinessBranches,
        CreateBusinessBranch,
        UpdateBusinessBranch,
        DeleteBusinessBranch,
        CreateLoyalty,
        ReadLoyalty,
        ReadLoyalties,
        UpdateLoyalty,
        DeleteLoyalty,
        ReadUser,
        ReadMembership,
        CreateMembership,
        DeleteMembership,
        ReadMemberships,
        CreatePayment,
        ReadBonuses,
        CalcDiscount,
        DeletePayment,
    )
    controllers = provide_all(
        WebLogin,
        Logout,
    )
