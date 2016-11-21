# -*- coding: utf-8 -*-
from django.forms import modelform_factory, modelformset_factory, ModelForm, Textarea, TextInput, EmailInput, Select, ModelChoiceField, \
DateInput, FileInput, CheckboxInput, SelectMultiple, CheckboxSelectMultiple, HiddenInput

from demografia.models import Persona, Vivienda, Miembrohogar, Hogar, Salud, Pais, Discapacidad, Vocero
import datetime, re
from django import forms
from dal import autocomplete

from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, EnclosedInput, LinkedSelect, AutosizedTextarea, NumberInput, SuitSplitDateTimeWidget


#####################################################################################################################################
############################################## Formulario persoalizado de las personas ##############################################
class PersonaForm(ModelForm):
	class Meta:
		model = Persona
		fields = (
			'foto',
			'letracedulaidentidad',
			'cedulaidentidad',
 		 	'rif',
 		 	'pasaporte',
 		 	'nombre',
 		 	'otrosnombres',
 		 	'apellido',
 		 	'otrosapellidos',
 		 	'fechanacimiento',
 		 	'sexo',
 		 	'telefono',
 		 	'celular',
 		 	'email',
 		 	'twitter',
 			'paisnacimiento',
 			'etnia',
 			'padre',
 			'madre',
 			'conyuge',
 			'authuser',
 			'cne'
		)
		widgets = {
            'foto': FileInput(),
            'letracedulaidentidad': Select(attrs={'class':'btn btn-default btn-sm input-sm'}),
            'cedulaidentidad': TextInput(attrs={'class':'form-control input-sm'}),
            'rif': TextInput(attrs={'class':'form-control input-sm'}),
            'pasaporte': TextInput(attrs={'class':'form-control input-sm'}),
            'nombre': TextInput(attrs={'class':'form-control input-sm'}),
            'otrosnombres': TextInput(attrs={'class':'form-control input-sm'}),
            'apellido': TextInput(attrs={'class':'form-control input-sm'}),
            'otrosapellidos': TextInput(attrs={'class':'form-control input-sm'}),
            'fechanacimiento': SuitDateWidget(attrs={'class':'form-control input-sm','readonly':'True'}),
            'sexo': Select(attrs={'class':'form-control input-sm'}),
            'telefono': TextInput(attrs={'class':'form-control input-sm'}),
            'celular': TextInput(attrs={'class':'form-control input-sm'}),
            'email': EmailInput(attrs={'class':'form-control input-sm'}),
            'twitter': TextInput(attrs={'class':'form-control input-sm'}),
            'paisnacimiento': autocomplete.ModelSelect2(url='demografia:paisAutoComplete', attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
            'etnia': autocomplete.ModelSelect2(url='demografia:etniaAutoComplete', attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
            'padre': autocomplete.ModelSelect2(url='demografia:hombreAutoComplete', attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
            'madre': autocomplete.ModelSelect2(url='demografia:mujerAutoComplete', attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
            'conyuge': autocomplete.ModelSelect2(url='demografia:personaAutoComplete', forward=('sexo',), attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
            'cne': TextInput(attrs={'class':'form-control input-sm','readonly':'True'}),
        }

	def clean(self):
		diccionario_limpio = super(PersonaForm, self).clean()
		fechaNacimiento = diccionario_limpio.get('fechanacimiento')
		cedulaIdentidad = str(diccionario_limpio.get('cedulaidentidad'))
		rif = diccionario_limpio.get('rif')

		#Validamos que la fecha de nacimiento no sea mayor a la fecha actual
		fecha_actual = datetime.date.today()
		if fecha_actual < fechaNacimiento:
			self.add_error('fechanacimiento', "La fecha de nacimiento no debe ser mayor al dia de hoy")

     	#Si la persona tiene nueve(9) años o mas, validamos la cédula tenga la forma 99999999
		edad = fecha_actual.year - fechaNacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fechaNacimiento.month, fechaNacimiento.day))
		patronMayorEdad = re.compile('^\d{5,8}$')
		if edad >= 9 and patronMayorEdad.match(cedulaIdentidad) is None:
			self.add_error('cedulaidentidad', "La cédula de identidad de las personas mayores o iguales a nueve (9) años de edad, debe comenzar con V ó E, seguido de ocho (8) digitos correspondientes al número de la cédula")

		#Si la persona tiene menos de nueve(9), validamos la cédula tenga la forma -99999999
		patronMenorEdad = re.compile('^\-\d{5,9}$')
		if edad < 9 and patronMenorEdad.match(cedulaIdentidad) is None:
			self.add_error('cedulaidentidad', "La cédula de identidad de los menores de nueve (9) años de edad, debe comenzar con guion seguido de seguido de ocho (8) digitos correspondientes al número de la cédula de la madre o representante legal, seguido de un digito que indica el número de hijo.")

		##Si la persona tiene nueve(9) años o mas, validamos que el R.I.F. tenga la forma G|J|V|E-99999999-9
		patronMayorEdad = re.compile('^[GgJjVvEe]\-\d{5,8}\-\d{1}$')
		if  edad >= 9 and patronMayorEdad.match(rif) is None:
			self.add_error('rif', "El R.I.F. debe comenzar por G, J, V ó E, seguido de un guión y el número de R.I.F. El ultimo numero, separdo por un guión.")

		##Si la persona tiene menos de nueve(9), validamos que el R.I.F. sea igual al número de cédula de identidad
		if  edad < 9 and patronMenorEdad.match(rif) is None:
			self.add_error('rif', "El R.I.F. de los menores de nueve (9) años de edad, debe ser igual a cedula")

    # Validamos que el teléfono cumpla con el formato
	def clean_telefono(self):
	 	diccionario_limpio = self.cleaned_data
	 	telefono = diccionario_limpio.get('telefono')
	 	patron = re.compile('^\+58\s\(\d{3}\)\s\d{3}\-\d{2}\-\d{2}$')
	 	if telefono:
	 		if patron.match(telefono) is None:
	 			raise forms.ValidationError("El número de teléfono local debe cumplir con la forma +58 (999) 999-99-99")
	 	return telefono

    # Validamos que el celular cumpla con el formato
	def clean_celular(self):
	 	diccionario_limpio = self.cleaned_data
	 	celular = diccionario_limpio.get('celular')
	 	patron = re.compile('^\+58\s\(\d{3}\)\s\d{3}\-\d{2}\-\d{2}$')
	 	if celular:
	 		if patron.match(celular) is None:
	 			raise forms.ValidationError("El número de teléfono celular debe cumplir con la forma +58 (999) 999-99-99")
	 	return celular

#####################################################################################################################################
######################################### Formulario customizado de la salud de las personas ########################################
class SaludPersonaForm(ModelForm):
	class Meta:
		model = Salud
		fields = (
			'persona',
			'conapdis',
			'cuidador',
 		 	'discapacidad',
			'mtlp',
 		 	'alcoholismo',
 		 	'tabaquismo',
 		 	'drogas',
 		 	'patologia',
 		 	'tipoapoyo',
		)
		widgets = {
			'persona': HiddenInput(),
            'conapdis': TextInput(attrs={'class':'form-control input-sm'}),
            'cuidador': autocomplete.ModelSelect2(url='demografia:personaAutoComplete', forward=['sexo'], attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
 		 	'discapacidad': CheckboxSelectMultiple(),
            'mtlp': CheckboxInput(attrs={'class':'form-control input-sm'}),
 		 	'alcoholismo': CheckboxInput(attrs={'class':'form-control input-sm'}),
 		 	'tabaquismo': CheckboxInput(attrs={'class':'form-control input-sm'}),
 		 	'drogas': CheckboxInput(attrs={'class':'form-control input-sm'}),
 		 	'patologia': CheckboxSelectMultiple(),
 		 	'tipoapoyo': CheckboxSelectMultiple()
        }
#####################################################################################################################################
####################################### Formulario persoalizado de los miembros de la familia #######################################
class MiembrohogarForm(ModelForm):
	class Meta:
		model = Miembrohogar
		fields = (
			'hogar',
 		 	'parentesco',
 		 	'persona'
		)
		widgets = {
            'hogar': Select(attrs={'class':'form-control input-sm'}),
            'parentesco': Select(attrs={'class':'form-control input-sm'}),
            'persona': autocomplete.ModelSelect2(url='demografia:personaAutoComplete', attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
        }

#####################################################################################################################################
############################################## Formulario persoalizado de los hogares ###############################################
class HogarForm(ModelForm):
	class Meta:
		model = Hogar
		fields = (
			'nombrehogar',
 		 	'tipopropiedadvivienda',
 		 	'vivienda'
		)
		widgets = {
            'nombrehogar': TextInput(attrs={'class':'form-control input-sm'}),
            'tipopropiedadvivienda': Select(attrs={'class':'form-control input-sm'}),
 		 	'vivienda': Select(attrs={'class':'form-control input-sm'}),
        }

#####################################################################################################################################
############################################## Formulario persoalizado de los voceros ###############################################
class VoceroForm(ModelForm):
	class Meta:
		model = Vocero
		fields = (
			'zona',
 		 	'persona'
		)
		widgets = {
            'zona': TextInput(attrs={'class':'form-control input-sm'}),
            'persona': autocomplete.ModelSelect2(url='demografia:personaAutoComplete', forward=['sexopersona'], attrs={'data-placeholder': '----------', 'data-minimum-input-length': 3, 'class':'form-control input-sm'}),
        }

#####################################################################################################################################
####################################### Formulario persoalizado de la vivienda #######################################
class ViviendaForm(ModelForm):
	class Meta:
		model = Vivienda
		fields = (
			'tipovivienda',
            'nombrevivienda',
            'piso',
            'apartamento',
            'tipovia',
            'nombrevia',
            'tipolocalidad',
            'nombrelocalidad',
            'metroscuadrados',
            'numerohabitaciones',
            'numerobanos',
            'condicionfisica',
            'zona',
		)
		widgets = {
			'tipovivienda': Select(attrs={'class':'form-control input-sm'}),
            'nombrevivienda': TextInput(attrs={'class':'form-control input-sm'}),
            'piso': TextInput(attrs={'class':'form-control input-sm'}),
            'apartamento': TextInput(attrs={'class':'form-control input-sm'}),
            'tipovia': Select(attrs={'class':'form-control input-sm'}),
            'nombrevia': TextInput(attrs={'class':'form-control input-sm'}),
            'tipolocalidad': Select(attrs={'class':'form-control input-sm'}),
            'nombrelocalidad': TextInput(attrs={'class':'form-control input-sm'}),
            'metroscuadrados': NumberInput(attrs={'class':'form-control input-sm'}),
            'numerohabitaciones': NumberInput(attrs={'class':'form-control input-sm'}),
            'numerobanos': NumberInput(attrs={'class':'form-control input-sm'}),
            'condicionfisica': Select(attrs={'class':'form-control input-sm'}),
            'zona': HiddenInput(),
            'nombrehogar': TextInput(attrs={'class':'form-control input-sm'}),
        }