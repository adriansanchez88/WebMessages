from django.shortcuts import render
from django.views.generic.base import TemplateView

# CBV que muestra la página de inicio utilizando el template home.html y heredando de la vista genérica TemplateView
class IndexView(TemplateView):
    # Se define el nombre que va a tener el template que va a mostrar la vista
    template_name = "core/index.html"

    # Se redefine el método get para que renderice el template y lo muestre,
    # como tercer argumento al render() se define un diccionario de contexto ({'clave':'valor'}) 
    # para asi en el template llamar a la 'clave' del diccionario y nos muestre su 'valor'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'título':'Mi Página Web Genérica', 
            'subtítulo':'Index'
            })

class AboutView(TemplateView):
    # Se define el nombre que va a tener el template que va a mostrar la vista
    template_name = "core/about.html"

    # Se redefine el método get para que renderice el template y lo muestre,
    # como tercer argumento al render() se define un diccionario de contexto ({'clave':'valor'}) 
    # para asi en el template llamar a la 'clave' del diccionario y nos muestre su 'valor'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'título':'Mi Página Web Genérica', 
            'subtítulo':'About'
            })
