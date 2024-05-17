from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVData
import csv
import io
from django.core.paginator import Paginator

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)  # Skip the header
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                _, created = CSVData.objects.update_or_create(
                    email=column[0],
                    name=column[1],
                    credit_score=column[2],
                    credit_lines=column[3],
                    masked_phone_number=column[4]
                )
            return redirect('upload_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})
def display_data(request):
    data_list = CSVData.objects.all()
    paginator = Paginator(data_list, 100)  # Show 100 records per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'display_data.html', {'page_obj': page_obj})
def calculate_pricing(request):
    data_list = CSVData.objects.all()
    base_price = 10
    price_per_credit_line = 1
    price_per_credit_score_point = 0.05

    pricing_data = []
    for data in data_list:
        subscription_price = (base_price + 
                              (price_per_credit_line * data.credit_lines) + 
                              (price_per_credit_score_point * data.credit_score))
        pricing_data.append({
            'email': data.email,
            'name': data.name,
            'subscription_price': subscription_price
        })

    paginator = Paginator(pricing_data, 100)  # Show 100 records per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pricing_data.html', {'page_obj': page_obj})

