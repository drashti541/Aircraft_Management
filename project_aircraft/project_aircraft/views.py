from django.http import HttpResponse

def home_page(request):
    print("home")
    return HttpResponse("Home")
