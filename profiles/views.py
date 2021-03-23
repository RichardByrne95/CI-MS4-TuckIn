from django.shortcuts import render

# Create your views here.
def customer_profile(request):
    context = {}
    return render(request, 'profiles/customer_account.html', context)


def customer_order_history(request):
    context = {}
    return render(request, 'profiles/customer_order_history.html', context)