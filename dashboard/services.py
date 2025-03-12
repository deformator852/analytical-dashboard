from django.db.models import Count, Sum, F
from django.db.models.functions import ExtractMonth, ExtractYear
from dashboard.models import Customers, OrderDetails, Orders


def get_customers_count():
    data = Customers.objects.count()
    return data


def get_current_year_sales_revenue():
    data = (
        OrderDetails.objects.select_related("order")
        .filter(order__order_date__year=1997)
        .annotate(year=ExtractYear("order__order_date"))
        .annotate(month=ExtractMonth("order__order_date"))
        .values("year", "month")
        .annotate(month_total_price=Sum(F("unit_price") * F("quantity")))
        .order_by("year", "month")
    )
    return data


def get_number_of_sales_and_total_revenue():
    data = OrderDetails.objects.aggregate(
        number_of_sales=Count("*"),
        total_revenue=Sum(F("unit_price") * F("quantity")),
    )
    return data["number_of_sales"], data["total_revenue"]


def get_sales_by_region():
    data = (
        Orders.objects.select_related("customer")
        .values("customer__country")
        .exclude(customer__country__isnull=True)
        .annotate(
            total_sales=Sum(F("orderdetails__unit_price") * F("orderdetails__quantity"))
        )
        .order_by("-total_sales")
    )
    return data
