"""crm_epic_event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import crm.views
import users.views


router = routers.SimpleRouter()
router.register('users', users.views.UserViewset, basename='users')
router.register('customers', crm.views.CustomerViewset, basename='customers')
router.register('contracts', crm.views.ContractViewset, basename='contracts')
router.register('events', crm.views.EventViewset, basename='events')

users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
users_router.register('customers', crm.views.CustomerViewset, basename='_user_customers')
users_router.register('contracts', crm.views.ContractViewset, basename='user_contracts')
users_router.register('events', crm.views.EventViewset, basename='user_events')

customers_router = routers.NestedSimpleRouter(router, 'customers', lookup='customer')
customers_router.register('contracts', crm.views.ContractViewset, basename='customer_contracts')
customers_router.register('events', crm.views.EventViewset, basename='customer_events')

contracts_router = routers.NestedSimpleRouter(router, 'contracts', lookup='contract')
contracts_router.register('sign', crm.views.EventViewset, basename='contract_sign')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(users_router.urls)),
    path('api/', include(customers_router.urls)),
    path('api/', include(contracts_router.urls))
]
