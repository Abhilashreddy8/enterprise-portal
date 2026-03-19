from django.urls import path
from .views import dashboard
from .views import report_list, report_detail
urlpatterns = [

path("", dashboard, name="dashboard"),

path("api/reports/", report_list),

path("api/reports/<int:pk>/", report_detail),

]