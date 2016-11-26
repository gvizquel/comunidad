# -*- coding: utf-8

from .models import Condicionfisicavivienda, Comunidad, Hogar, Parentesco, Persona, Tipolocalidad, Tipovia, Tipovivienda, Vivienda, \
 Miembrohogar, Zona, Vocero, Pais, Patologia, Salud, Tipoapoyo, Tipodiscapacidad, Discapacidad

from .forms import PersonaForm, MiembrohogarForm, VoceroForm

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, EnclosedInput, LinkedSelect, AutosizedTextarea, NumberInput, SuitSplitDateTimeWidget




###############################################################################
### Administraion de la Zona del Consejo Comunal                            ###
###############################################################################

class VoceroInline(admin.TabularInline):
    form = VoceroForm
    model = Vocero
    extra = 1
    verbose_name_plural = 'Voceros de la zona'
    #ordering = ('parentesco',)

# class VoceroAdmin(VersionAdmin):
# 	search_fields = ('zona', 'persona')
# 	list_display = ('zona', 'persona')
# 	ordering = ('zona', 'persona')
# 	list_select_related = True
# 	#inlines = (VoceroInline,)
# 	fieldsets = [
#         (None, {
#             'fields': [
# 				'zona',
# 				'persona'
# 			]
#         }),
#     ]
# admin.site.register(Vocero, VoceroAdmin)

class ZonaAdmin(admin.ModelAdmin):
	search_fields = ('comunidad', 'nombrezona')
	list_display = ('comunidad', 'nombrezona')
	ordering = ('comunidad', 'nombrezona')
	list_select_related = True
	inlines = (VoceroInline,)
	fieldsets = [
        (None, {
            'fields': [
				'comunidad',
				'nombrezona',
				'descripcion'
			]
        }),
    ]
admin.site.register(Zona, ZonaAdmin)

class ZonaInline(admin.TabularInline):
    model = Zona
    extra = 1
    verbose_name_plural = "Zonas de la Comunidad"
    ordering = ('nombrezona',)

###############################################################################
### Administraion del Consejo Comunal                                       ###
###############################################################################
class comunidadAdmin(admin.ModelAdmin):
	search_fields = ('nombrecomunidad', 'parroquia')
	list_display = ('nombrecomunidad', 'parroquia')
	ordering = ('nombrecomunidad', 'parroquia')
	list_select_related = True
	inlines = (ZonaInline,)
	fieldsets = [
        (None, {
            'fields': [
				'idcomunidad',
				'nombrecomunidad',
				'tipovia',
				'nombrevia',
				'tipolocalidad',
				'nombrelocalidad',
				'tipolocal',
				'nombrelocal',
				'pisolocal',
				'numerolocal',
				'referencialocal',
				'parroquia',
				'poligonal',
				'centrocoordenadas',
				'coordenadas'
			]
        }),
    ]
admin.site.register(Comunidad, comunidadAdmin)

###############################################################################
### Administraion del Miembro de Hogar                                      ###
###############################################################################
# class MiembrohogarAdmin(VersionAdmin):
# 	form = MiembrohogarForm
# 	search_fields = ('hogar',)
# 	list_display = ('hogar', 'parentesco', 'persona')
# 	ordering = ('hogar', 'parentesco', 'persona')
# 	list_select_related = True
# 	fieldsets = [
#         (None, {
#             'fields': [
# 				'hogar',
# 				'parentesco',
# 				'persona',
# 			]
#         }),
#     ]
# admin.site.register(Miembrohogar, MiembrohogarAdmin)

class MiembrohogarInline(admin.TabularInline):
    form = MiembrohogarForm
    model = Miembrohogar
    extra = 1
    verbose_name_plural = 'Miembros del hogar'
    ordering = ('parentesco',)

###############################################################################
### Administraion del Modelo Hogar                                          ###
###############################################################################
class HogarAdmin(admin.ModelAdmin):
	search_fields = ('nombrehogar',)
	list_display = ('nombrehogar', 'vivienda')
	ordering = ('vivienda', 'nombrehogar')
	list_select_related = True
	inlines = (MiembrohogarInline,)
	fieldsets = [
        (None, {
            'fields': [
				'nombrehogar',
				'vivienda',
				'tipopropiedadvivienda'
			]
        }),
    ]
admin.site.register(Hogar, HogarAdmin)

admin.site.register(Parentesco)

###############################################################################
### Administraion del Modelo Persona                                        ###
###############################################################################
class PersonaAdmin(admin.ModelAdmin):
	form = PersonaForm
	search_fields = ('cedulaidentidadpersona',)
	list_display = ('__unicode__','fecharegistro')
	#ordering = ('nombrepersona', 'otrosnombrespersona', 'apellidopersona', 'otrosapellidospersona')
	list_select_related = True
admin.site.register(Persona, PersonaAdmin)


###############################################################################
### Administraion del Modelo Salud                                          ###
###############################################################################
class PruebaAdmin(admin.ModelAdmin):
	list_select_related = True
admin.site.register(Salud)

admin.site.register(Patologia)
admin.site.register(Tipoapoyo)
admin.site.register(Tipodiscapacidad)
admin.site.register(Discapacidad)

admin.site.register(Tipolocalidad)


###############################################################################
### Administraion del Modelo TipoVia                                        ###
###############################################################################
class TipoviaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Tipovia, TipoviaAdmin)


###############################################################################
### Administraion del Modelo TipoVivienda                                  ###
###############################################################################
class TipoviviendaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Tipovivienda, TipoviviendaAdmin)

###############################################################################
### Administraion del Modelo Vivienda                                       ###
###############################################################################
class ViviendaAdmin(admin.ModelAdmin):
	search_fields = ('nombrevivienda' ,'piso' ,'apartamento')
	list_display = ('nombrevivienda' ,'piso' ,'apartamento')
	list_select_related = True
	fieldsets = [
        (None, {
            'fields': [
				'tipovivienda',
				'nombrevivienda',
				'piso',
				'apartamento',
				'tipovia',
				'nombrevia',
				'tipolocalidad',
				'nombrelocalidad',
				'zona',
				'metroscuadrados',
				'numerohabitaciones',
				'numerobanos',
				'condicionfisica'
			]
        }),
    ]
admin.site.register(Vivienda, ViviendaAdmin)