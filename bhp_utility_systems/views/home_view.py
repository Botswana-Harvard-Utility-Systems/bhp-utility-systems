from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'bhp_utility_systems/home.html'
    navbar_name = 'default'
    navbar_selected_item = 'home'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        is_hr = self.request.user.groups.filter(
            name='HR').exists()
        context.update({'is_hr': is_hr})

        return context
