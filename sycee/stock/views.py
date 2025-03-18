from django.shortcuts import render

# Create your views here.

from .models import DailyStock

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_records = DailyStock.objects.all().count()
    num_records = 0

    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()


    context = {
        'num_records': num_records,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import requests

from datetime import datetime
from django.db import transaction

def process_data_and_save_to_db(data):
    symbol = data["Meta Data"]["2. Symbol"]
    time_series = data["Time Series (Daily)"]
    
    records = []
    
    for date_str, daily_data in time_series.items():
        try:
            # Generate unique ID: symbol + date (e.g., "IBM-2025-03-14")
            record_id = f"{symbol}-{date_str}"
            
            # Convert date string to Date object
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Create DailyStock instance
            records.append(DailyStock(
                id=record_id,
                symbol=symbol,
                date=date,
                open=daily_data["1. open"],
                high=daily_data["2. high"],
                low=daily_data["3. low"],
                close=daily_data["4. close"],
                volume=int(daily_data["5. volume"])  # Convert to integer
            ))
            
        except (KeyError, ValueError, TypeError) as e:
            # Handle missing fields or conversion errors
            print(f"Error processing {date_str}: {e}")
            continue

    # Bulk create records in a transaction
    with transaction.atomic():
        DailyStock.objects.bulk_create(
            records,
            update_conflicts=True,
            update_fields=['open', 'high', 'low', 'close', 'volume'],
            unique_fields=['id']
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_stock_data(request):
    # Alpha Vantage API URL
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
    
    try:
        # Fetch data from external API
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Check if response contains valid data
        if "Time Series (Daily)" not in data:
            return Response({"status": "error", "message": "Invalid data received"}, status=400)
            
        process_data_and_save_to_db(data)
        
        return Response({"status": "success", "message": "Data fetched successfully"})
        
    except requests.exceptions.RequestException as e:
        return Response({"status": "error", "message": str(e)}, status=500)