from .models import Category

def menuLinks(request):
    links = Category.objects.all()
    return dict(links = links)