from django.shortcuts import render

def index(request):
    url = "{{ MEDIA_URL }}bytesizebackground.png"
    context = {
        'hero_url': url,
    }
    return render(request, 'home/index.html', context)
