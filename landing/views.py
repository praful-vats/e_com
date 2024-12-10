from django.shortcuts import render

def landing_page(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'landing/landing_page.html', context)
