from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Transaction, Categories, WishlistItem
import plotly.express as px
from django.db.models import Sum
from .forms import TransactionForm, WishlistItemForm
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot


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
        Transaction.objects.filter(user=request.user,transaction_type="withdrawal")
        .values("category__name")
        .annotate(total_amount=Sum("amount"))
    )

  #
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


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    total_spendings = sum(t.amount for t in transactions if t.transaction_type == 'spending')
    total_depo = sum(t.amount for t in transactions if t.transaction_type == 'deposit')
    balance = total_depo - total_spendings
    total_wishlist = sum(item.item_price for item in wishlist_items)
    difference = total_depo - total_wishlist  # Obliczanie różnicy jako suma z transactions minus suma z wishlisty

    if request.method == 'POST':
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.save()
            return redirect('dashboard')
    else:
        form = WishlistItemForm()

    # Generowanie wykresu
    categories = [t.category.name for t in transactions]
    amounts = [t.amount for t in transactions]

    fig = go.Figure([go.Bar(x=categories, y=amounts)])
    plot_div = plot(fig, output_type='div')

    context = {
        'transactions': transactions,
        'wishlist_items': wishlist_items,
        'total_spendings': total_spendings,
        'total_depo': total_depo,
        'balance': balance,
        'total_wishlist': total_wishlist,
        'difference': difference,
        'form': form,
        'plot_div': plot_div,  # Przekazanie wykresu do kontekstu
    }
    return render(request, 'dashboard/dashboard.html', context)
