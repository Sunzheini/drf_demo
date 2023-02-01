from django.shortcuts import render
from django.views import generic as views
from rest_framework import generics as rest_views
from rest_framework import serializers
from rest_framework import views as rest_based_views
from rest_framework.response import Response
from rest_framework import viewsets

from drf_demo.api.models import Employee, Department


# 8
class ShortEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name')


# 8
class DepartmentSerializer(serializers.ModelSerializer):
    employee_set = ShortEmployeeSerializer(many=True)   # many=True ako ne e single object

    class Meta:
        model = Department
        fields = '__all__'


# 6
class ShortDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# 2. serialization: object to text format
class EmployeeSerializer(serializers.ModelSerializer):
    # 6 expands the department, not only to show id, but all selected info
    department = ShortDepartmentSerializer()

    # 2. ModelSerializer works like Modelform
    class Meta:
        model = Employee
        fields = '__all__'

    # 11. overwrite create to be able to create using
    # `raw data` form in localhost:8000/api/employees/?department_id=2
    def create(self, validated_data):
        department_name = validated_data.pop('department').get('name')
        try:
            department = Department.objects.filter(name=department_name).get()
        except Department.DoesNotExist:
            department = Department.objects.create(
                name=department_name,
            )
        return Employee.objects.create(
            **validated_data,
            department=department,
        )


# 5. Custom serializer
# class DemoSerializer(serializers.Serializer):
#     key = serializers.CharField()
#     value = serializers.IntegerField()


# 1. server-side rendering, i.e. the result is rendered HTML
class EmployeesListView(views.ListView):
    model = Employee
    template_name = ''


# 7
class DepartmentsListApiView(rest_views.ListCreateAPIView):
    queryset = Department.objects.all()
    #serializer_class = ShortDepartmentSerializer   # short
    serializer_class = DepartmentSerializer    # long with Employees: 8
    # + also register in urls


# 3. JSON serialization, i.e. parse models into JSON
# class EmployeesListApiView(rest_views.ListAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# 4. like above + form
class EmployeesListApiView(rest_views.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # 10. get by id: overwrite the `get_queryset` method
    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        queryset = self.queryset
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset.all()
        # now works with http://localhost:8000/api/employees/?department_id=2


# 9a.
class NameSerializer(serializers.Serializer):
    name = serializers.CharField()


# 9b. customise how we display data
class DemoSerializer(serializers.Serializer):
    employees = ShortEmployeeSerializer(many=True)
    employees_count = serializers.IntegerField()
    departments = ShortDepartmentSerializer(many=True)
    first_department = serializers.CharField()
    department_names = NameSerializer(many=True)


# 9c. like django views + register in urls
class DemoApiView(rest_based_views.APIView):
    def get(self, request):
        employees = Employee.objects.all()
        departments = Department.objects.all()
        body = {
            'employees': employees,
            'employees_count': employees.count(),               # count: new method!
            'departments': departments,
            'first_department': departments.first(),            # new!
            'department_names': departments,
        }
        serializer = DemoSerializer(body)
        return Response(serializer.data)     # `Response comes from DRF`


# 12. All operations in 1, must be registered in urls as router...
# read https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
