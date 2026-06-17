from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from bhp_personnel.models import Employee, Supervisor, Department
from timesheet.models import MonthlyEntry


class PendingApprovalsView(LoginRequiredMixin, ListView):
    template_name = 'bhp_utility_systems/pending_approvals.html'
    context_object_name = 'timesheets'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        is_hr = user.groups.filter(name='HR').exists()
        is_supervisor = user.groups.filter(name='Supervisor').exists()

        qs = MonthlyEntry.objects.filter(
            status='submitted'
        ).select_related('employee', 'employee__supervisor', 'employee__department')

        if is_hr:
            pass
        elif is_supervisor:
            sup = Supervisor.objects.filter(email=user.email).first()
            qs = qs.filter(employee__supervisor=sup) if sup else qs.none()
        else:
            qs = qs.none()

        dept = self.request.GET.get('department')
        month = self.request.GET.get('month')
        search = self.request.GET.get('search')

        if dept:
            qs = qs.filter(employee__department__dept_name=dept)
        if month:
            try:
                year, mon = month.split('-')
                qs = qs.filter(month__year=year, month__month=mon)
            except ValueError:
                pass
        if search:
            qs = qs.filter(
                Q(employee__first_name__icontains=search) |
                Q(employee__last_name__icontains=search) |
                Q(employee__identifier__icontains=search)
            )

        return qs.order_by('month', 'employee__last_name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments'] = Department.objects.all().order_by('dept_name')
        ctx['selected_department'] = self.request.GET.get('department', '')
        ctx['selected_month'] = self.request.GET.get('month', '')
        ctx['search'] = self.request.GET.get('search', '')
        ctx['is_hr'] = self.request.user.groups.filter(name='HR').exists()
        ctx['is_supervisor'] = self.request.user.groups.filter(name='Supervisor').exists()
        ctx['total_pending'] = self.get_queryset().count()
        return ctx
