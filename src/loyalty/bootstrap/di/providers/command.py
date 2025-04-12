from dishka import Provider, Scope, provide, provide_all

from loyalty.application.business.create import CreateBusiness
from loyalty.application.business.read import ReadBusiness, ReadBusinessBranches
from loyalty.application.business_branch.create import CreateBusinessBranch
from loyalty.application.business_branch.delete import DeleteBusinessBranch
from loyalty.application.business_branch.read import ReadBusinessBranch
from loyalty.application.business_branch.update import UpdateBusinessBranch
from loyalty.application.client.create import CreateClient
from loyalty.application.client.read import ReadClient
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
        ReadUser,
    )
    controllers = provide_all(
        WebLogin,
        Logout,
    )
