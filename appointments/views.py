from django.shortcuts import render
app_name = 'appointments'


def test_view(request):
    return render(request, 'appointments/index.html')
