from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Transaction, Categories
import plotly.express as px
from django.db.models import Sum
from .forms import TransactionForm
import pandas as pd


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    categories = Categories.objects.all()

##Funkcja do sumowania wszystkich wydatków użytkownika
    def SpendingsSum(transactions):
        total=0
        for transaction in transactions:
            if(transaction.transaction_type=="withdrawal"):
                total+=transaction.amount
        return total
##Funkcja do sumowania depozytów
    def DepositSum(transactions):
        total = 0
        for transaction in transactions:
            if (transaction.transaction_type == "deposit"):
                total += transaction.amount
        return total
##Funkcja do wyliczania balansu
    def Balance(withdraws,deposits):
        return total_deposit-total_spendings

    total_spendings = SpendingsSum(transactions)
    total_deposit=DepositSum(transactions)
    balance=Balance(total_spendings,total_deposit)

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
        "total_spendings":total_spendings,
        "total_depo":total_deposit,
        "balance": balance,
        "plot_div": plot_div,
    }

    return render(request, "dashboard/dashboard.html", context)
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')  # Zmien ścieżkę na właściwy widok po zapisaniu
    else:
        form = TransactionForm()
    return render(request, 'dashboard/create_transaction.html', {'form': form})
