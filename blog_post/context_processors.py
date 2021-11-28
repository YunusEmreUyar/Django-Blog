from .models import Category

def context_variable(request):
    categories = Category.objects.all()
    return {'categories':categories,}
