from django.urls import path

from core.views.view import *
from core.views.create import *
from core.views.edit import *
from core.views.list import *
from core.views.delete import *
from core.views.home import *

from core.views.document import *
from core.views.export import *
from core.views.action import *

from core.views.api.list import *
from core.views.api.operation import *
from core.views.api.checkpoint import *
from core.views.create_company import *

app_name = "core"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("list/<str:app>/<str:model>", List.as_view(), name="list"),
    path("create/<str:app>/<str:model>", Create.as_view(), name="create"),
    path("edit/<str:app>/<str:model>/<int:pk>", Edit.as_view(), name="edit"),
    path("view/<str:app>/<str:model>/<int:pk>", Overview.as_view(), name="view"),
    path("delete/<str:app>/<str:model>/<int:pk>", Delete.as_view(), name="delete"),

    path("document/<str:app>/<str:model>/<str:template>", Document.as_view(), name="document"),
    path("action/<str:app>/<str:model>/<str:verbose>", Action.as_view(), name="action"),
    path("export/<str:app>/<str:model>", Export.as_view(), name="export"),

    path("check-point-operation/<int:checkpoint>", CheckPointATM.as_view(), name="check-point-operation"),
    path("api-check-point-operation", OperationAPIView.as_view(), name="api-check-point-operation"),
    path("api-list/<str:app>/<str:model>", ListAPI.as_view(), name="api-list"),

    path("create-company", CreateCompany.as_view(), name="create-company")
]
