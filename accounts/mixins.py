from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.userprofile.role == 'teacher'

    def handle_no_permission(self):
        return redirect('dashboard')