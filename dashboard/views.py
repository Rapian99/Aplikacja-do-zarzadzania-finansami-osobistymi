from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def dashboard(request):
    if (
        hasattr(request.user, "userprofile")
        and request.user.userprofile.must_change_password
    ):
        return redirect("change_password")
    return render(request, "dashboard/dashboard.html", {"user": request.user})
