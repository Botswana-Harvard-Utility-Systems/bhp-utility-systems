"""bhp_utility_systems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from edc_identifier.admin_site import edc_identifier_admin
from edc_data_manager.admin_site import edc_data_manager_admin
from document_tracking.admin_site import document_tracking_admin
from procurement.admin_site import procurement_admin
from bhp_personnel.admin_site import bhp_personnel_admin
from timesheet.admin_site import timesheet_admin

from .views import HomeView, AdministrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', document_tracking_admin.urls),
    path('admin/', procurement_admin.urls),
    path('admin/', bhp_personnel_admin.urls),
    path('admin/', edc_data_manager_admin.urls),
    path('admin/', edc_identifier_admin.urls),
    path('admin/', timesheet_admin.urls),
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('admin/procurement/',
         RedirectView.as_view(url='admin/procurement/'),
         name='procurement_models_url'),
    path('admin/bhp_personnel/',
         RedirectView.as_view(url='admin/bhp_personnel/'),
         name='bhp_personnel_models_url'),
    path('admin/timesheet/',
         RedirectView.as_view(url='admin/timesheet/'),
         name='timesheet_models_url'),

    path('edc_base/', include('edc_base.urls')),
    path('edc_data_manager/', include('edc_data_manager.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('edc_identifier/', include('edc_identifier.urls')),

    path('document_tracking/', include('document_tracking.urls')),
    path('document_tracking_dashboard/', include('document_tracking_dashboard.urls')),

    path('procurement/', include('procurement.urls')),
    path('procurement_dashboard/', include('procurement_dashboard.urls')),

    path('timesheet/', include('timesheet.urls')),
    path('timesheet_dashboard/', include('timesheet_dashboard.urls')),

    path('bhp_personnel/', include('bhp_personnel.urls')),
    path('cms/', include('cms_dashboard.urls')),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
    path('bhp_utility_reports/', include('bhp_utility_reports.urls')),

]

urlpatterns += [
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_reset_change.html',
             success_url='/'),
         name='change_password'
         ),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
