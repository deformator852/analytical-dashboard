from rest_framework import serializers


class CurrentYearSalesRevenueSeriazlier(serializers.Serializer): ...


class DashBoardSerializer(serializers.Serializer):
    number_of_sales = serializers.IntegerField()
    total_revenue = serializers.FloatField()
    total_customers = serializers.IntegerField()
    current_year_sales_revenue = serializers.ListField()
    sales_by_region = serializers.ListField()
