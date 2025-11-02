from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from edc_identifier.admin_site import edc_identifier_admin
from bhp_personnel.admin_site import bhp_personnel_admin
from timesheet.admin_site import timesheet_admin

from .views import HomeView, AdministrationView


urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('edc_base/', include('edc_base.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('edc_identifier/', include('edc_identifier.urls')),
    path('timesheet/', include('timesheet.urls')),
    path('timesheet_dashboard/', include('timesheet_dashboard.urls')),
    path('bhp_personnel/', include('bhp_personnel.urls')),
    path('bhp_personnel_dashboard/', include('bhp_personnel_dashboard.urls')),
    path('bhp_utility_reports/', include('bhp_utility_reports.urls')),
    path('cms/', include('cms_dashboard.urls')),

    # Default Django admin
    path('admin/', admin.site.urls),
    path('personnel-admin/', bhp_personnel_admin.urls),
    path('identifier-admin/', edc_identifier_admin.urls),
    path('timesheet-admin/', timesheet_admin.urls),

    path('administration/', AdministrationView.as_view(), name='administration_url'),

    path('admin/bhp_personnel/',
         RedirectView.as_view(
             url=reverse_lazy(
                 'admin:app_list', kwargs={'app_label': 'bhp_personnel'}),
             permanent=False
             ),
         name='bhp_personnel_models_url'
         ),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),


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
