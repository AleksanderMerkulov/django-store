from django.shortcuts import render

# Create your views here.
def mainPage(request):
    return render(request, 'pages/main_page.html')
    pass