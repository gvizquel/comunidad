from django.contrib.auth.decorators import permission_required
from django.conf.urls import url
from . import views
from demografia.views import ViviendaList, HogarList, PersonaList, PaisAutocomplete, PaisAutocomplete2, PersonaAutocomplete, PersonaHombreAutocomplete, PersonaMujerAutocomplete, EtniaAutocomplete

app_name = 'demografia'

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^comunidad/$', permission_required('demografia.ctrl_comunidad')(views.comunidad), name='comunidad'),
    url(r'^comunidad/zona/$', permission_required('demografia.ctrl_comunidad')(ViviendaList.as_view()), name='zona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(HogarList.as_view()), name='vivienda'),
    url(r'^comunidad/zona/agregarVivienda/(?P<idZona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.vivienda), name='agregarVivienda'),
    url(r'^comunidad/zona/editarVivienda/(?P<idVivienda>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.vivienda), name='editarVivienda'),
    url(r'^comunidad/zona/eliminarVivienda/(?P<idVivienda>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.eliminarVivienda), name='eliminarVivienda'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/editarHogar/(?P<idHogar>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.editarHogar), name='editarHogar'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/eliminarHogar/(?P<idHogar>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.eliminarHogar), name='eliminarHogar'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(PersonaList.as_view()), name='hogar'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/persona/$',  permission_required('demografia.ctrl_comunidad')(views.persona), {'accion':0}, name='agregarPersona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/mostrarPersona/(?P<idPersona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.persona), {'accion':1}, name='mostrarPersona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/editarPersona/(?P<idPersona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.persona), {'accion':2}, name='editarPersona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/eliminarPersona/(?P<idPersona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.persona), {'accion':3}, name='eliminarPersona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/mostrarSaludPersona/(?P<idPersona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.saludPersona), {'accione':4}, name='mostrarSaludPersona'),
    url(r'^comunidad/zona/vivienda/(?P<idVivienda>[^/]+)/hogar/(?P<idHogar>[^/]+)/editarSaludPersona/(?P<idPersona>[^/]+)/$',  permission_required('demografia.ctrl_comunidad')(views.saludPersona), {'accione':5}, name='editarSaludPersona'),
    url(r'^resumenCenso/$', views.resumenCenso, name='resumenCenso'),

    url(r'^comunidad/mapa/$', views.mapa, name='mapa'),
    url(r'^ubicacion/$', views.ubicacion, name='ubicacion'),
    url(r'^datosHogar/$', views.persona, name='hogar'),
    url(r'^personaAutoComplete/$', permission_required('demografia.ctrl_comunidad')(PersonaAutocomplete.as_view()), name='personaAutoComplete',),
    url(r'^personaHombreAutoComplete/$', permission_required('demografia.ctrl_comunidad')(PersonaHombreAutocomplete.as_view()), name='hombreAutoComplete',),
    url(r'^personaMujerAutoComplete/$', permission_required('demografia.ctrl_comunidad')(PersonaMujerAutocomplete.as_view()), name='mujerAutoComplete',),
    url(r'^paisAutoComplete/$', permission_required('demografia.ctrl_comunidad')(PaisAutocomplete.as_view()), name='paisAutoComplete',),
    url(r'^paisAutoComplete2/$', permission_required('demografia.ctrl_comunidad')(PaisAutocomplete2.as_view()), name='paisAutoComplete2',),
    url(r'^etniaAutoComplete/$', permission_required('demografia.ctrl_comunidad')(EtniaAutocomplete.as_view()), name='etniaAutoComplete',),
]