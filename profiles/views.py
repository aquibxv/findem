from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request, 'profiles/search.html')

def profile(request):
    return render(request, 'profiles/profile.html')
