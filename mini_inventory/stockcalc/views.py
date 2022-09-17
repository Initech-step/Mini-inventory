from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from math import sqrt
from .forms import EOQform, MaximumStockLevelForm, MinimumStockLevelForm, ReorderLevelForm
# Create your views here.


def eoq(request):
    if request.method == 'POST':
        form = EOQform(request.POST)
        if form.is_valid():
            demand_per_anum = form.cleaned_data.get('demand_per_anum')
            ordering_cost = form.cleaned_data.get('ordering_cost_per_order')
            holding_cost = form.cleaned_data.get('holding_cost')
            
            #following the eoq formula
            numerator = 2 * demand_per_anum * ordering_cost 
            bod = numerator/holding_cost
            answer = sqrt(bod) 

            messages.add_message(request, messages.INFO, answer)
            return redirect('eoq')

    form = EOQform(request.POST or None)
    return render(request, 'stockcalc/eoq.html', {'form': form})


def maximum_level(request):
    if request.method == 'POST':
        form = MaximumStockLevelForm(request.POST)
        if form.is_valid():
            reorder_level = form.cleaned_data.get('reorder_level')
            reorder_quantity = form.cleaned_data.get('reorder_quantity')
            minimum_usage_rate = form.cleaned_data.get('minimum_usage_rate')
            minimum_lead_time = form.cleaned_data.get('minimum_lead_time')

            #according to the formula
            part1 = reorder_level + reorder_quantity
            part2 = minimum_lead_time * minimum_usage_rate

            answer = part1 - part2
            messages.add_message(request, messages.INFO, answer)
            return redirect('max_level')

    form = MaximumStockLevelForm(request.POST or None)
    return render(request, 'stockcalc/max_level.html', {'form': form})

def minimum_level(request):
    if request.method == 'POST':
        form = MinimumStockLevelForm(request.POST)
        if form.is_valid():
            reorder_level = form.cleaned_data.get('reorder_level')
            average_usage_rate = form.cleaned_data.get('average_usage_rate')
            average_lead_time = form.cleaned_data.get('average_lead_time')
 
            #follow the formula
            bod = average_usage_rate * average_lead_time
            answer = reorder_level - bod

            messages.add_message(request, messages.INFO, answer)
            return redirect('min_level')

    form = MinimumStockLevelForm(request.POST or None)
    return render(request, 'stockcalc/min_level.html', {'form': form})

def reorder_level(request):
    if request.method == 'POST':
        form = ReorderLevelForm(request.POST)
        if form.is_valid():
            maximum_lead_time = form.cleaned_data.get('maximum_lead_time')
            maximum_usage_rate = form.cleaned_data.get('maximum_usage_rate')

            answer = maximum_lead_time * maximum_usage_rate
            messages.add_message(request, messages.INFO, answer)
            return redirect('rol')

    form = ReorderLevelForm(request.POST or None)
    return render(request, 'stockcalc/rol.html', {'form': form})