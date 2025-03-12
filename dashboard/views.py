from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard.serializers import DashBoardSerializer
from .services import *


class DashBoard(APIView):
    def get(self, request):
        info = {}
        customers_count = get_customers_count()
        current_year_sales_revenue = get_current_year_sales_revenue()
        number_or_sales, total_revenue = get_number_of_sales_and_total_revenue()
        sales_by_region = get_sales_by_region()
        info["number_of_sales"] = number_or_sales
        info["total_revenue"] = round(total_revenue, 2)
        info["total_customers"] = customers_count
        info["current_year_sales_revenue"] = list(current_year_sales_revenue)
        info["sales_by_region"] = sales_by_region
        serializer = DashBoardSerializer(data=info)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
