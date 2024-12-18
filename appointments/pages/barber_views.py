import os
import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView, View
from ..forms.barber_forms import ServiceForm
from ..models import BarberService, Scheduling, CustomUser
from ..utils.validations import OnlyStaffMixin, OnlySuperuserMixin
from ..utils.api import get_results_api
from ..serializers import ServiceSerializer


class ServicesCreationView(LoginRequiredMixin, OnlyStaffMixin, View):
    """
    ServicesCreationView handles the creation of barber services.

    This view is accessible only to users with the 'employee', 'manager', or
    'superuser' user type.
    It allows authorized users to create new barber services through a form.

    Methods
    -------
    get(request)
        Renders the service creation form if the user has permission.

    post(request)
        Processes the form submission for creating a new barber service.
    """

    def get(self, request):
        """
        Handles GET requests to render the service creation form.

        Checks if the authenticated user is an employee, manager, or superuser.
        If not, it redirects to the home page.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        Returns
        -------
        HttpResponse
            - Renders the service creation template with the service form
              if the user has permission.
            - Redirects to the home page if the user does not have permission.
        """

        service_form = ServiceForm()

        context = {
            'service_form': service_form
        }

        return render(self.request, 'appointments/services.html', context)

    def post(self, request):
        """
        Handles POST requests to process the creation of a new barber service.

        Receives the form data, validates it, and saves a new service.
        If the service is successfully created, it redirects to the services
        list.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        Returns
        -------
        HttpResponse
            Redirects to the services list page if the service is created
            successfully, or re-renders the service creation page with error
            messages if the form is invalid.
        """
        service_form = ServiceForm(request.POST, request.FILES)

        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.save()
            return redirect('appointments:services_list')

        context = {'service_form': service_form}
        return render(self.request, 'appointments/services.html', context)


class ServicesListView(LoginRequiredMixin, ListView):
    """
    ServicesListView displays a list of barber services.

    This view is accessible only to authenticated users. It fetches the list
    of services from an external API and renders them in a template.


    Attributes
    ----------
    model : BarberService
        The model used to retrieve the barber services.

    template_name : str
        The template used to render the services list page.

    Methods
    -------
    get(request)
        Fetches the list of services from an external API and renders the
        services list page.
    """

    model = BarberService
    template_name = 'appointments/services_list.html'

    def get(self, request):
        """
        Handles GET requests to fetch and display the list of barber services.

        Retrieves the services from an external API and renders them in the
        services list template.

        Parameters
        ----------
        request : HttpRequest
            The request object containing metadata about the request.

        Returns
        -------
        HttpResponse
            Renders the services list template with the fetched services.
        """
        api_url = str(os.getenv('SERVICES_API_URL'))

        response = get_results_api(self.request, api_url)

        context = {
            'obj': response,
        }
        return render(self.request, self.template_name, context)


class DashboardView(LoginRequiredMixin, OnlyStaffMixin, APIView):
    template_name = 'appointments/dashboard.html'

    def get_total_users(self):
        return CustomUser.objects.count()

    def get_total_employees(self):
        employee = CustomUser.objects.filter(user_type='employee').count()
        owners = CustomUser.objects.filter(user_type='superuser').count()
        return employee + owners

    def get_total_appointments(self):
        return Scheduling.objects.count()

    def get_total_services(self):
        api_url = os.getenv('SERVICES_API_URL')

        response = get_results_api(self.request, api_url)
        total_services = len(response)
        return total_services

    def get_appointments(self):
        api_url = os.getenv('SCHEDULES_API_URL')

        response = get_results_api(self.request, api_url)
        return response

    def get(self, request, *args, **kwargs):
        total_users = self.get_total_users()
        total_employees = self.get_total_employees()
        total_appointments = self.get_total_appointments()
        total_services = self.get_total_services()
        appointments = self.get_appointments()

        context = {
            'total_users': total_users,
            'total_employees': total_employees,
            'total_appointments': total_appointments,
            'total_services': total_services,
            'appointments': appointments,
            'status_choices': Scheduling.STATUS_CHOICES
        }

        return render(request, self.template_name, context)


class GetEmployeesView(LoginRequiredMixin, OnlySuperuserMixin, APIView):
    template_name = 'appointments/view_employees.html'

    def get_employees(self):
        employees = CustomUser.objects.filter(
            user_type='employee')
        return employees

    def get_superusers(self):
        superusers = CustomUser.objects.filter(
            user_type='superuser')
        return superusers

    def get(self, request, *args, **kwargs):
        context = {
            'employees': self.get_employees(),
            'superusers': self.get_superusers(),
        }
        return render(request, self.template_name, context)


class UpdateStatusView(SuccessMessageMixin, OnlyStaffMixin, UpdateView):
    model = Scheduling
    fields = ['status']
    template_name = 'appointments/status_update.html'
    success_message = 'Status atualizado com sucesso!'
    success_url = reverse_lazy('appointments:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Scheduling.STATUS_CHOICES
        return context


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ServiceViewSet provides CRUD operations for barber services.

    This viewset allows for the creation, retrieval, updating, and deletion of
    barber services.

    Attributes
    ----------
    queryset : QuerySet
        The queryset used to retrieve all barber services.

    serializer_class : Serializer
        The serializer class used to serialize and deserialize barber service
        data.
    """

    queryset = BarberService.objects.all()
    serializer_class = ServiceSerializer
