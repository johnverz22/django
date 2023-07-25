from django.shortcuts import render
from django.db import models
from sales.models import Sale
from django.db.models.functions import ExtractYear
from django.db.models.functions import ExtractMonth
from calendar import month_name
import json

def home(request):
     return render(request, 'home.html')

def pie_chart(request):
    data = Sale.objects.values('region').annotate(total_profit=models.Sum('total_profit'))
    labels = [item['region'] for item in data]
    total_profits = [float(item['total_profit']) for item in data]

    context = {
        'labels': json.dumps(labels),
        'total_profits': json.dumps(total_profits),
    }
    return render(request, 'pie_chart.html', context)

'''def bar_chart(request):
    region_filter = request.GET.get('region', '')
    data = Sale.objects.filter(region=region_filter).values('country').annotate(total_profit=models.Sum('total_profit')).order_by('country')
    labels = [item['country'] for item in data]
    total_profits = [float(item['total_profit']) for item in data]

    context = {
        'labels': labels,
        'total_profits': total_profits,
    }
    return render(request, 'bar_chart.html', context)
'''
def bar_chart(request):
    region_filter = request.GET.get('region', '')

    data = Sale.objects.filter(region=region_filter).values('country').annotate(
        total_revenue=models.Sum('total_revenue'),
        total_profit=models.Sum('total_profit')
    ).order_by('country')

    labels = [item['country'] for item in data]
    total_revenue = [float(item['total_revenue']) for item in data]
    total_profit = [float(item['total_profit']) for item in data]

    context = {
        'labels': labels,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'region': region_filter
    }
    return render(request, 'bar_chart.html', context)

def line_chart(request):
    country_filter = request.GET.get('country', '')

    data = Sale.objects.filter(country=country_filter).annotate(
        year=ExtractYear('order_date')
    ).values('year').annotate(
        total_profit=models.Sum('total_profit')
    ).order_by('year')

    labels = [item['year'] for item in data]
    total_profit = [float(item['total_profit']) for item in data]

    context = {
        'labels': labels,
        'total_profit': total_profit,
        'country': country_filter,
    }
    return render(request, 'line_chart.html', context)

def combo_chart(request):
    country =request.GET.get('country', '')
    year = request.GET.get('year', '')
    data = Sale.objects.filter(country=country, order_date__year=year).annotate(
        month=ExtractMonth('order_date')
    ).values('month').annotate(
        total_profit=models.Sum('total_profit'),
        units_sold=models.Sum('units_sold')
    ).order_by('month')


     # Create labels for all months ("January" to "December")
    labels = [month_name[month] for month in range(1, 13)]

    # Initialize total_profit list with zeros for all months
    total_profit = [0] * 12
    units_sold = [0] *12

    # Populate total_profit list with actual data for existing months
    for item in data:
        month_index = item['month'] - 1
        total_profit[month_index] = float(item['total_profit'])
        units_sold[month_index] =float(item['units_sold'])

    context = {
        'labels': labels,
        'total_profit': total_profit,
        'units_sold': units_sold,
        'country': country,
        'year': year,
    }
    return render(request, 'combo_chart.html', context)


def polar_chart(request):
    data = Sale.objects.values('item_type').annotate(total_items=models.Count('item_type'))
    labels = [item['item_type'] for item in data]
    total_items = [float(item['total_items']) for item in data]
    print(total_items)
    context = {
        'labels': json.dumps(labels),
        'total_items': json.dumps(total_items),
    }
    return render(request, 'polar_chart.html', context)

def radar_chart(request):
    data = Sale.objects.values('region', 'sales_channel').annotate(total_sales=models.Count('sales_channel'))
    sales_channels = list(set([item['sales_channel'] for item in data]))
    region_labels = list(set([item['region'] for item in data]))
    sales_data = {}

    for item in data:
        region = item['region']
        channel = item['sales_channel']
        total_sales = item['total_sales']

        if channel not in sales_data:
            sales_data[channel] = [0] * len(region_labels)

        sales_data[channel][region_labels.index(region)] = total_sales

    context = {
        'sales_channels': json.dumps(sales_channels),
        'region_labels': json.dumps(region_labels),
        'sales_data': json.dumps(list(sales_data.values())),
    }
    return render(request, 'radar_chart.html', context)
