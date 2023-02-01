from django.urls import path

from drf_demo.api.views import EmployeesListApiView, DepartmentsListApiView, DemoApiView

urlpatterns = (
    path('employees/', EmployeesListApiView.as_view(), name='api list employees'),
    path('departments/', DepartmentsListApiView.as_view(), name='api list departments'),

    # terminal: curl localhost:8000/api/employees/
    #           curl localhost:8000/api/departments/

    # browser: http://localhost:8000/api/employees/
    #          http://localhost:8000/api/departments/

    path('demo/', DemoApiView.as_view(), name='demo view'),
)

# http://localhost:8000/api/employees/?department_id=2

