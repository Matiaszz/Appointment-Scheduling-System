from django.shortcuts import render
app_name = 'project'


def test_view(request):
    return render(request, 'base.html')
