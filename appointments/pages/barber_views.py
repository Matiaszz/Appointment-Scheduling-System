from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms.barber_forms import ServiceForm
from ..models import BarberService
from rest_framework import viewsets
from ..serializers import ServiceSerializer
from dotenv import load_dotenv
import requests
import os

load_dotenv('.../env/.env')


class ServicesCreationView(LoginRequiredMixin, View):
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
        if request.user.is_client():
            return redirect('appointments:index')

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
        api_url = str(os.getenv('API_URL'))

        response = requests.get(api_url)
        services = response.json()
        context = {
            'obj': services,
        }
        return render(self.request, self.template_name, context)


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
