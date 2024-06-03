import csv
from io import StringIO
from django.utils import timezone
from datetime import timedelta
from media_asset.models import Billboards

def filter_billboards(time_filter, vacancy):
    now = timezone.now()
    
    if time_filter == 'week':
        start_date = now - timedelta(days=now.weekday())
    elif time_filter == 'month':
        start_date = now.replace(day=1)
    elif time_filter == 'year':
        start_date = now.replace(month=1, day=1)
    else:
        start_date = None  # No time filter applied

    if start_date:
        billboards = Billboards.objects.filter(date__gte=start_date, vacancy=vacancy)
    else:
        billboards = Billboards.objects.filter(vacancy=vacancy)
        
    return billboards

def generate_csv_report(time_filter, vacancy):
    billboards = filter_billboards(time_filter, vacancy)
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Asset Name', 'Asset Type', 'Category', 'Zone', 'Sub Zone', 'Status', 'Vacancy', 'Dimension', 'Price', 'User', 'Date'])
    
    for billboard in billboards:
        writer.writerow([
            billboard.asset_name,
            billboard.get_asset_type_display(),
            billboard.get_category_display(),
            billboard.get_zone_display(),
            billboard.sub_zone,
            billboard.get_status_display(),
            billboard.get_vacancy_display(),
            billboard.dimension,
            billboard.price,
            billboard.user,
            billboard.date,
        ])
    
    return output.getvalue()
