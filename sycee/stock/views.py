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