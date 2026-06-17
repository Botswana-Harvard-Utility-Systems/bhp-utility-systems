from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from bhp_personnel.models import Employee, Department
from timesheet.models import MonthlyEntry


class HRReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'bhp_utility_systems/hr_reports.html'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['HR', 'Supervisor']).exists()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        selected_dept = self.request.GET.get('department', '')
        selected_year = self.request.GET.get('year', '2026')

        try:
            year = int(selected_year)
        except ValueError:
            year = 2026

        base_qs = MonthlyEntry.objects.filter(month__year=year)
        emp_qs = Employee.objects.select_related('department', 'supervisor')

        if selected_dept:
            base_qs = base_qs.filter(employee__department__dept_name=selected_dept)
            emp_qs = emp_qs.filter(department__dept_name=selected_dept)

        # 1. Status summary
        status_map = {s['status']: s['count'] for s in
                      base_qs.values('status').annotate(count=Count('id'))}
        ctx['status_summary'] = {
            'draft':     status_map.get('draft', 0),
            'submitted': status_map.get('submitted', 0),
            'approved':  status_map.get('approved', 0),
            'verified':  status_map.get('verified', 0),
            'rejected':  status_map.get('rejected', 0),
            'total':     base_qs.count(),
        }

        # 2. Leave per employee
        ctx['leave_data'] = (
            base_qs
            .values('employee__identifier', 'employee__first_name',
                    'employee__last_name', 'employee__department__dept_name')
            .annotate(
                annual=Sum('annual_leave_taken'),
                sick=Sum('sick_leave_taken'),
                study=Sum('study_leave_taken'),
                compassionate=Sum('compassionate_leave_taken'),
                maternity=Sum('maternity_leave_taken'),
                paternity=Sum('paternity_leave_taken'),
            ).order_by('employee__last_name')
        )

        # 3. Overtime summary
        ctx['overtime_data'] = (
            base_qs
            .values('employee__identifier', 'employee__first_name',
                    'employee__last_name', 'employee__department__dept_name')
            .annotate(total_overtime=Sum('monthly_overtime'))
            .filter(total_overtime__gt=0)
            .order_by('-total_overtime')
        )

        # 4. Employee list
        ctx['employee_list'] = emp_qs.order_by('department__dept_name', 'last_name')

        ctx['departments'] = Department.objects.all().order_by('dept_name')
        ctx['selected_dept'] = selected_dept
        ctx['selected_year'] = str(year)
        ctx['years'] = [str(y) for y in range(2024, 2028)]
        return ctx
