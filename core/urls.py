from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from django.urls import path

from core.views.create import *
from core.views.edit import *
from core.views.list import *
from core.views.delete import *
from core.views.home import *

from core.views.document import *
from core.views.export import *
from core.views.action import *

app_name = "core"

urlpatterns = [
    # apply cache with memcached
    # path("", cache_page(60*60)(login_required(Home.as_view())), name="home"),
    # path("create/<str:app>/<str:model>", cache_page(60*60)(Create.as_view()), name="create"),

    path("", login_required(Home.as_view()), name="home"),
    path("create/<str:app>/<str:model>", login_required(Create.as_view()), name="create"),
    path("edit/<str:app>/<str:model>/<int:pk>", login_required(Edit.as_view()), name="edit"),
    path("list/<str:app>/<str:model>/<int:page>", login_required(List.as_view()), name="list"),
    path("delete/<str:app>/<str:model>/<int:pk>", login_required(Delete.as_view()), name="delete"),

    path("document/<str:app>/<str:model>/<str:template>", login_required(Document.as_view()), name="document"),
    path("action/<str:app>/<str:model>", login_required(Action.as_view()), name="action"),
    path("export/<str:app>/<str:model>", login_required(Export.as_view()), name="export")
]
