from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Transaction, Categories
import plotly.express as px
from django.db.models import Sum
import pandas as pd


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    categories = Categories.objects.all()

    category_sums = (
        Transaction.objects.filter(user=request.user)
        .values("category__name")
        .annotate(total_amount=Sum("amount"))
    )

    category_sums_list = list(category_sums)
    if category_sums_list:
        df = pd.DataFrame(category_sums_list)
        df.columns = [
            "Category",
            "Total Amount",
        ]

        fig = px.bar(
            df,
            x="Category",
            y="Total Amount",
            labels={"Category": "Category", "Total Amount": "Total Amount"},
        )
        plot_div = fig.to_html(full_html=False)
    else:
        plot_div = "<p>No data available to display the chart.</p>"

    context = {
        "transactions": transactions,
        "categories": categories,
        "plot_div": plot_div,
    }

    return render(request, "dashboard/dashboard.html", context)
