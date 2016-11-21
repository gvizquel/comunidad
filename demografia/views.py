# -*- coding: utf-8 -*-
from io import BytesIO
from demografia.models import Condicionfisicavivienda, Comunidad, Hogar, Persona, Vivienda, Miembrohogar, Zona, Vocero, Pais, Salud, Etnia, Discapacidad, Tipodiscapacidad

from django.db.models import Value
import urllib
import datetime
from django.utils.html import strip_tags
from django.db.models.functions import Concat
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import PersonaForm, MiembrohogarForm, HogarForm, ViviendaForm, SaludPersonaForm
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from dal import autocomplete
from io import BytesIO
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import mm, cm, inch
# from reportlab.lib.colors import yellow, red, black,white
# from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.platypus import Table
# from reportlab.lib.enums import TA_CENTER
from demografia.reportes import misReportes


#@login_required
def index(request):
    return render(request, 'index.html.twig')

class PaisAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Pais.objects.none()

        if self.q:
            qs = Pais.objects.filter(nombrepais__istartswith=self.q).order_by('nombrepais')

        return qs

class PaisAutocomplete2(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Pais.objects.none()

        if self.q:
            qs = Pais.objects.filter(nombrepais__istartswith=self.q).order_by('nombrepais')

        return qs

class PersonaMujerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Persona.objects.none()

        if self.q:
            qs = Persona.objects.filter(sexo = 'F', cedulaidentidad = self.q)


        return qs

class PersonaHombreAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Persona.objects.none()

        if self.q:
            qs = Persona.objects.filter(sexo = 'M', cedulaidentidad = self.q)

        return qs

class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Persona.objects.none()

        sexo = self.forwarded.get('sexo', None)
        # miembrohogar = 0 #self.forwarded.get('miembrohogar', None)

        # if miembrohogar == 1:
        #     qs2 = Miembrohogar.objects.all().values_list('personamiembrohogar', flat=True)
        #     qs = qs.exclude(idpersona__in = qs2)


        if self.q:
            if sexo == 'M':
                qs = Persona.objects.filter(sexo = 'F', cedulaidentidad = self.q)
            elif sexo == 'F':
                qs = Persona.objects.filter(sexo = 'M', cedulaidentidad = self.q)
            else:
                qs = Persona.objects.filter(cedulaidentidad = self.q)

        return qs

class EstadoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Esado.objects.none()

        qs = Estado.objects.all()

        if self.q:
            qs = qs.filter(nombreestado__icontains = self.q).order_by('nombreestado')

        return qs

class EtniaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Pais.objects.none()

        qs = Etnia.objects.all()

        if self.q:
            qs = qs.filter(nombreetnia__istartswith=self.q)

        return qs


######################################################################################################################
## Clases para el modelo persona: lista personas, edita personas y agrega personas (misma clase) y elimina personas ##
######################################################################################################################
class PersonaList(FormMixin, ListView):
    model = Miembrohogar
    form_class = MiembrohogarForm
    context_object_name = 'listaPersona'
    template_name = 'demografia/listaPersona.html.twig'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect('')
        else:
            return self.get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonaList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):

        # Cargo todos los miembros que pertencen a la familia que estoy pasando como parametro garantizando que sea un hogar/familia
        # que el usuario auntenticado pueda modificar. Asi evito que algun vivo modifque el url para modificar otro hogar/familia.
        return Miembrohogar.objects.filter(hogar = Hogar.objects.get(vivienda__in = Vivienda.objects.filter(zona = User.objects.get(username = self.request.user).persona.vocero.zona.pk), pk = self.kwargs['idHogar']).pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PersonaList, self).get_context_data(**kwargs)

        # Ahora cargo todos los hogares o familias que habitan en la vivienda
        context['hogar'] = Hogar.objects.get(pk = self.kwargs['idHogar'])

        context['form'] = self.get_form()

        return context

@login_required
def persona(request, idPersona=None, idHogar=None, idVivienda=None, accion=None):
    fecha_actual = datetime.date.today()
    hoy =str(int(fecha_actual.day) - 1) + "/" + str(fecha_actual.month) + "/" + str(fecha_actual.year)
    if accion == 0:
        active = 'Añadir persona'
        form = PersonaForm()
        persona = ''
        cne = ''
    elif accion == 1:
        active = 'Mostrar persona'
        persona = Persona.objects.get(pk = idPersona)
        form = PersonaForm(instance = persona)
        cne = ''
    elif accion == 2:
        active = 'Editar persona'
        persona = Persona.objects.get(pk = idPersona)
        try:
            #url = urllib.urlopen("http://www.cne.gov.ve/web/registro_electoral/ceRE.php?nacionalidad=" + persona.letracedulaidentidad + "&cedula=" + str(persona.cedulaidentidad))
            #cne = strip_tags(url.read().decode('utf-8')).replace("\t", "").replace("\n", "").replace("\r", "")
            cne = None
        except ValueError:
            cne = None
        if cne:
            posParroquia = cne.find(u'Parroquia') + 10
            posCentro = cne.find(u'Centro')
            cne = cne[posParroquia:posCentro]
        else:
            cne = None
        form = PersonaForm(instance = persona, initial={'cne': cne})
    elif accion == 3:
        active = 'Eliminar persona'
        persona = Miembrohogar.objects.get(persona = idPersona)

    if request.method == 'POST':
        if accion == 0:
            form = PersonaForm(request.POST, request.FILES)
        elif accion == 2:
            form = PersonaForm(request.POST, request.FILES, instance = persona)
        elif accion == 3:
            persona.delete()
            return HttpResponseRedirect(reverse('demografia:hogar', args=(idVivienda, idHogar)))

        if form.is_valid():
            if accion == 0 or accion == 2:
                form.save()
                return HttpResponseRedirect(reverse('demografia:hogar', args=(idVivienda, idHogar)))
        else:
            return render(request, 'demografia/persona.html.twig', {'form':form, 'vivienda':idVivienda, 'hogar':idHogar, 'persona':persona, 'active':active, 'hoy': hoy })

    elif accion == 3:
        return render(request, 'demografia/eliminarPersona.html.twig', {'vivienda':idVivienda, 'hogar':idHogar, 'persona':persona, 'active':active, 'hoy': hoy })
    else:
        return render(request, 'demografia/persona.html.twig', {'form':form, 'vivienda':idVivienda, 'hogar':idHogar, 'persona':persona, 'active':active, 'cne': cne })


@login_required
def saludPersona(request, idPersona=None, idHogar=None, idVivienda=None, accione=None):
    persona = Persona.objects.get(pk = idPersona)
    tipoDiscapacidad = Tipodiscapacidad.objects.filter().order_by('nombretipodiscapacidad')
    if accione == 4:
        active = 'Mostrar persona'
    elif accione == 5:
        active = 'Editar persona'

    try:
        saludPersona = Salud.objects.get(pk = idPersona)
    except:
        saludPersona = None


    if saludPersona:
        form = SaludPersonaForm(instance = saludPersona)
        listaPatologia = saludPersona.patologia.all()
        listaDiscapacidad = saludPersona.discapacidad.all()
        listaTipoApoyo = saludPersona.tipoapoyo.all()
    else:
        form = SaludPersonaForm(initial={'persona': idPersona})
        listaPatologia = None
        listaDiscapacidad = None
        listaTipoApoyo = None

    if request.method == 'POST':
        if saludPersona:
            form = SaludPersonaForm(request.POST, request.FILES, instance = saludPersona)
        else:
            form = SaludPersonaForm(request.POST, request.FILES, initial={'persona': idPersona})

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hogar', args=(idVivienda, idHogar)))

    return render(request, 'demografia/saludPersona.html.twig', {'form':form, 'vivienda':idVivienda, 'hogar':idHogar, 'active':active, 'persona': persona, 'tipoDiscapacidad':tipoDiscapacidad, 'listaPatologia':listaPatologia, 'listaDiscapacidad':listaDiscapacidad, 'listaTipoApoyo':listaTipoApoyo })


@login_required
def eliminarPersona(request, idPersona=None, idHogar=None, idVivienda=None):
    persona = Miembrohogar.objects.get(persona = idPersona)
    if request.method == 'POST':
        persona.delete()
        return HttpResponseRedirect(reverse('hogar', args=(idVivienda, idHogar)))
    return render(request, 'demografia/eliminarPersona.html.twig', { 'persona': persona, 'vivienda': idVivienda, 'hogar': idHogar })


######################################################################################################################
## Clases para el modelo hogar: lista y agrega, edita, elimina hogares y agrega miembros a los hogares              ##
######################################################################################################################
class HogarList(FormMixin, ListView):
    model = Hogar
    form_class = HogarForm
    context_object_name = 'listaHogar'
    template_name = 'demografia/listaHogar.html.twig'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form.save()
            return HttpResponseRedirect('')
        else:
            return self.get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HogarList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Hogar.objects.filter(vivienda = Vivienda.objects.get(zona = User.objects.get(username = self.request.user).persona.vocero.zona.pk, pk = self.kwargs['idVivienda']).pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HogarList, self).get_context_data(**kwargs)

        # Busco la vivienda que paso en el parametro
        context['vivienda'] = Vivienda.objects.get(pk = self.kwargs['idVivienda'])

        # Ahora cargo todos los hogares o familias que habitan en la vivienda
        context['hogar'] = Hogar.objects.filter(vivienda = context['vivienda'].pk)

        # Cargar la zona de la vivienda
        context['cantidadMiembroHogar'] = Miembrohogar.objects.filter(hogar__in = context['hogar']).count()

        return context

@login_required
def editarHogar(request, idHogar=None, idVivienda=None):
    hogar = Hogar.objects.get(pk = idHogar)
    form = HogarForm(instance = hogar)
   # form.fields['vivienda'].queryset = Vivienda.objects.filter(vivienda>64)

    if request.method == 'POST':
        form = HogarForm(request.POST, instance = hogar)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vivienda', args=(idVivienda,)))
    return render(request, 'demografia/editarHogar.html.twig', {'form':form, 'vivienda':idVivienda, 'hogar':idHogar })

@login_required
def eliminarHogar(request, idHogar=None, idVivienda=None):
    hogar = Hogar.objects.get(pk = idHogar)
    if request.method == 'POST':
        hogar.delete()
        return HttpResponseRedirect(reverse('vivienda', args=(idVivienda,)))
    return render(request, 'demografia/eliminarHogar.html.twig', { 'vivienda': idVivienda, 'hogar': hogar })

@login_required
def agregarMiembroHogar(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = PersonaFormSet(request.POST, request.FILES)
        # check whether it's valid:
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('')
    else:
        return render(request, 'demografia/persona.html.twig', {'formset': formset, 'persona': persona })


######################################################################################################################
## Clases para el modelo vivienda: lista, grega, edita y elimina viviendas                                          ##
######################################################################################################################

class ViviendaList(ListView):
    context_object_name = 'listaVivienda'
    template_name = 'demografia/zona.html.twig'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ViviendaList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Ahora cargo todas las viviendas de todas las zonas del consejo comunal
        return Vivienda.objects.filter(zona = Zona.objects.get(pk = User.objects.get(username = self.request.user).persona.vocero.zona.pk))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ViviendaList, self).get_context_data(**kwargs)

        # Ahora cargo todas las zonas del consejo comunal
        context['zona'] = Zona.objects.get(pk = User.objects.get(username = self.request.user).persona.vocero.zona.pk)

        # Ahora cargo todas las zonas del consejo comunal
        context['comunidad'] = context['zona'].comunidad

        # Busco las viviendas que paso en el parametro
        context['vivienda'] = Vivienda.objects.filter(zona = context['zona'])

        # Ahora cargo todos los hogares o familias que habitan en las viviendas del conse comunal
        context['hogar'] = Hogar.objects.filter(vivienda__in = context['vivienda'])

        # Ahora cuento cuantas personas hay en todos los hogares o familias que habitan en las viviendas del conse comunal
        context['cantidadMiembroHogar'] = Miembrohogar.objects.filter(hogar__in = context['hogar']).count()

        return context

@login_required
def vivienda(request, idVivienda=None, idZona=None):
    if idVivienda == None:
        form = ViviendaForm()
        active = 'Añadir vivienda'
    else:
        vivienda = Vivienda.objects.get(pk = idVivienda)
        form = ViviendaForm(instance = vivienda)
        idZona = vivienda.zona.pk
        active = 'Editar vivienda'

    if request.method == 'POST':
        if idVivienda == None:
            form = ViviendaForm(request.POST)
        else:
            form = ViviendaForm(request.POST, instance = vivienda)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('zona'))

    return render(request, 'demografia/editarVivienda.html.twig', {'form':form, 'idZona':idZona, 'vivienda':idVivienda, 'active':active })

@login_required
def eliminarVivienda(request, idVivienda=None):
    vivienda = Vivienda.objects.get(pk = idVivienda)
    if request.method == 'POST':
        vivienda.delete()
        return HttpResponseRedirect(reverse('zona'))
    return render(request, 'demografia/eliminarVivienda.html.twig', { 'vivienda': vivienda })


#Esta vista utiliza la API de googlemaps para pintar un punto con la ubicación del CC
@login_required
def ubicacion(request):

    # Determino el consejo comunal al que pertenece la zona del vocero que acaba de logearse.
    comunidad = Comunidad.objects.get(pk = User.objects.get(username = request.user.username).persona.vocero.zona.comunidad.pk)

    return render(request, 'demografia/ubicacion.html.twig', { 'comunidad':comunidad })

@login_required
def mapa(request):

    # Determino el consejo comunal al que pertenece la zona del vocero que acaba de logearse.
    comunidad = Comunidad.objects.get(pk = User.objects.get(username = request.user.username).persona.vocero.zona.comunidad.pk)

    poligono = comunidad.poligonal.split()
    return render(request, 'demografia/mapa.html.twig', { 'comunidad':comunidad, 'poligono':poligono })

@login_required
def comunidad(request):
    vocero = Vocero.objects.get(persona = User.objects.get(username = request.user.username).persona.pk)

    # Ahora cargo todas las zonas del consejo comunal
    comunidad = vocero.zona.comunidad

    # Ahora cargo todas las zonas del consejo comunal
    zona = Zona.objects.filter(comunidad = vocero.zona.comunidad.pk)

    voceros = Vocero.objects.filter(zona__in = zona).order_by('zona', 'persona')

    # Ahora cargo todas las viviendas de todas las zonas de la comunidad
    vivienda = Vivienda.objects.filter(zona__in = zona)

    # Ahora cargo todos los hogares o familias que habitan en las viviendas de la zona
    hogar = Hogar.objects.filter(vivienda__in = vivienda)

    # Ahora cuento cuantas personas hay en todos los hogares o familias que habitan en las viviendas del conse comunal
    cantidadMiembroHogar = Miembrohogar.objects.filter(hogar__in = hogar).count()

    return render(request, 'demografia/comunidad.html.twig', { 'comunidad':comunidad, 'zona':zona, 'vocero':vocero, 'voceros':voceros, 'cantidadVivienda':vivienda.count(), 'cantidadHogar':hogar.count(), 'cantidadMiembroHogar':cantidadMiembroHogar })

def resumenCenso(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RESULTADOS_DEL_CENSO_COMUNITARIO_I.pdf"'
    usuario = request.user.username
    buffer = BytesIO()

    report = misReportes(buffer, 'Letter')
    pdf = report.print_users(usuario)

    response.write(pdf)
    return response