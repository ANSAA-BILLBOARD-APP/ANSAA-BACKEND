from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .utils import generate_csv_report

class ReportDownloadView(APIView):
    def get(self, request, format=None):
        time_filter = request.query_params.get('time_filter')
        vacancy = request.query_params.get('vacancy')
        
        if not time_filter or not vacancy:
            return Response({'error': 'time_filter and vacancy are required parameters.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            csv_content = generate_csv_report(time_filter, vacancy)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        return response
