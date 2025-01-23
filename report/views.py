# report/views.py

from django.shortcuts import render, redirect
from datetime import datetime
from report.services.db_queries import get_scraped_cell_summaries
from .forms import ReportForm

def report(request):
    year = datetime.now().year  # Replace with the desired year value
    month = datetime.now().month  # Replace with the desired month value
    results = get_scraped_cell_summaries().filter(scraped_dt__year=year, scraped_dt__month=month)
    return render(request, 'report/report.html', {'results': results})


def submit_report(request): 
    if request.method == 'POST': 
        form = ReportForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('report') 
        else: form = ReportForm() 
        return render(request, 'report/submit_report.html', {'form': form})