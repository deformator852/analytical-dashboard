from django.db.models import F, Count, OuterRef, Subquery, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from dashboard.models import Customers, OrderDetails
from dashboard.serializers import DashBoardSerializer


class DashBoard(APIView):
    def get(self, request):
        info = {}
        customers_count = Customers.objects.count()
        current_year_sales_revenue = (
            OrderDetails.objects.select_related("order")
            .filter(order__order_date__year=1997)
            .annotate(year=ExtractYear("order__order_date"))
            .annotate(month=ExtractMonth("order__order_date"))
            .values("year", "month")
            .annotate(month_total_price=Sum(F("unit_price") * F("quantity")))
            .order_by("year", "month")
        )

        data = OrderDetails.objects.aggregate(
            number_of_sales=Count("*"),
            total_revenue=Sum(F("unit_price") * F("quantity")),
        )
        info["number_of_sales"] = data["number_of_sales"]
        info["total_revenue"] = round(data["total_revenue"], 2)
        info["total_customers"] = customers_count
        info["current_year_sales_revenue"] = list(current_year_sales_revenue)
        serializer = DashBoardSerializer(data=info)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
