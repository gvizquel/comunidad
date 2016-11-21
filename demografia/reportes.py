# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from demografia.models import Condicionfisicavivienda, Comunidad, Zona, Vivienda, Hogar, Persona, Miembrohogar, Vocero, Pais, Etnia
from datetime import date, timedelta
from django.template import RequestContext
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, cm, inch
from reportlab.lib.colors import yellow, red, black,white
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.lib.utils import ImageReader

class pintaCabeceraPie(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawImage("%s/img/imgCabecera12.png" % settings.STATIC_ROOT, 10*mm, 264.4*mm, width=114.7*mm, height=10*mm, mask='auto')
        self.drawImage("%s/img/imgCabecera22.png" % settings.STATIC_ROOT, 168.3*mm, 264.4*mm, width=37.6*mm, height=10*mm, mask='auto')
        self.drawImage("%s/img/imgCabecera32.png" % settings.STATIC_ROOT, 5*mm, 5*mm, width=4.44*cm, height=10.80*cm, mask='auto')
        # self.line(0,10*mm,215.9*mm,10*mm)
        # self.line(10*mm,0,10*mm,279.4*mm)
        self.setFont("Helvetica", 8)
        self.drawRightString(204*mm, 15*mm, "Página %d de %d" % (self._pageNumber, page_count))

class misReportes:
	def __init__(self, buffer, pagesize):
		self.buffer = buffer
		if pagesize == 'A4':
			self.pagesize = A4
		elif pagesize == 'Letter':
			self.pagesize = letter
		self.width, self.height = self.pagesize

	def print_users(self, usuario):
		buffer = self.buffer
		doc = SimpleDocTemplate(
			buffer,
			rightMargin = 10*mm,
			leftMargin = 10*mm,
			topMargin = 18*mm,
			bottomMargin = 20*mm,
			pagesize = self.pagesize)

		# Our container for 'Flowable' objects
		elements = []

		# *******************************************************************************************************************************
		# ***************************************************** Estilos del reporte *****************************************************
		# *******************************************************************************************************************************

		# A large collection of style sheets pre-made for us
		styles = getSampleStyleSheet()
		styles.add(
			ParagraphStyle(
				name='Cabecera1',
				alignment = 1,
				# allowOrphans = 0,
				allowWidows = 1,
				# backColor = None,
				# borderColor = None,
				# borderPadding = 0,
				# borderRadius = None,
				# borderWidth = 0,
				bulletAnchor = 'start',
				bulletFontName = 'Helvetica',
				bulletFontSize = 10,
				# bulletIndent = 0,
				# endDots = None,
				# firstLineIndent = 0,
				fontName = 'Helvetica',
				fontSize = 14,
				# justifyBreaks = 0,
				# justifyLastLine = 0,
				leading = 12,
				# leftIndent = 0,
				# rightIndent = 0,
				spaceAfter = 5*mm,
				# spaceBefore = 0,
				splitLongWords = 1,
				textColor = black,
				# textTransform = None,
				underlineProportion = False,
				# wordWrap = None
			)
		)

		styles.add(
			ParagraphStyle(
				name='centrado',
				alignment = 1,
				bulletAnchor = 'start',
				fontName = 'Helvetica',
				fontSize = 10,
				spaceBefore = 5*mm,
				textColor = black
			)
		)

		styles.add(
			ParagraphStyle(
				name='miNormal',
				alignment = 0,
				bulletAnchor = 'start',
				fontName = 'Helvetica',
				fontSize = 10,
				spaceAfter = 1*mm,
				textColor = black
			)
		)

		styles.add(
			ParagraphStyle(
				name='cabeceraTabla',
				alignment = 1,
				bulletAnchor = 'start',
				fontName = 'Helvetica',
				fontSize = 8,
				textColor = black
			)
		)

		# *******************************************************************************************************************************
		# ****************************************************** Datos del reporte ******************************************************
		# *******************************************************************************************************************************

		vocero = Vocero.objects.get(persona = User.objects.get(username = usuario).persona.pk)

	    # Ahora cargo todas las zonas del consejo comunal
		zona = Zona.objects.filter(comunidad = vocero.zona.comunidad.pk)

		voceros = Vocero.objects.filter(zona__in = zona).order_by('zonavocerozona', 'personavocerozona')

	    # Ahora cargo todas las viviendas de todas las zonas del consejo comunal
		vivienda = Vivienda.objects.filter(zona__in = zona)

	    # Ahora cargo todos los hogares o familias que habitan en las viviendas del conse comunal
		hogar = Hogar.objects.filter(vivienda__in = vivienda)

	    # Ahora cargo las personas hay en todos los hogares o familias que habitan en las viviendas del consejo comunal
		miembroHogar = Miembrohogar.objects.values_list('persona').filter(hogar__in = hogar)

		# *******************************************************************************************************************************
		# *********************************************** Construyendo los grupos etarios ***********************************************
		# *******************************************************************************************************************************
		# Grupo etario de 0 a 14 años de edad
		hoy = date.today()
		edadMin = 0
		edadMax = 14
		fechaMin1 = date(hoy.year - edadMax - 1, hoy.month, hoy.day) + timedelta(days = 1)
		fechaMax1 = date(hoy.year - edadMin, hoy.month, hoy.day)
		grupoEtario1 = Persona.objects.filter(idpersona__in = miembroHogar, fechanacimiento__gt = fechaMin1, fechanacimiento__lte = fechaMax1)

		# Grupo etario de 15 a 17 años de edad
		edadMin = 15
		edadMax = 17
		fechaMin2 = date(hoy.year - edadMax - 1, hoy.month, hoy.day) + timedelta(days = 1)
		fechaMax2 = date(hoy.year - edadMin, hoy.month, hoy.day)
		grupoEtario2 = Persona.objects.filter(idpersona__in = miembroHogar, fechanacimiento__gt = fechaMin2, fechanacimiento__lte = fechaMax2)

		# Grupo etario mayores de 18 años de edad
		edadMin = 18
		fechaMax3 = date(hoy.year - edadMin, hoy.month, hoy.day)
		grupoEtario3 = Persona.objects.filter(idpersona__in = miembroHogar, fechanacimiento__lte = fechaMax3)

		# *******************************************************************************************************************************
		# *********************************************** Contando los inscritos en el CNE **********************************************
		# *******************************************************************************************************************************
		inscritosCNE = Persona.objects.filter(idpersona__in = miembroHogar, cne__isnull=False)

		# *******************************************************************************************************************************
		# *************************************************** Construyendo el reporte ***************************************************
		# *******************************************************************************************************************************

		elements.append(Paragraph('<b>RESULTADOS DEL CENSO COMUNITARIO</b>', styles['Cabecera1']))
		elements.append(Paragraph('DEL CONSEJO COMUNAL: <u>' + str(vocero.zona.comunidad) + '</u>', styles['miNormal']))
		elements.append(Paragraph(str(vocero.zona.comunidad.tipolocalidad) + ': <u>' + str(vocero.zona.comunidad.nombrelocalidad) + '</u>, PARROQUIA: <u>' + str(vocero.zona.comunidad.parroquia) + '</u>', styles['miNormal']))
		elements.append(Paragraph('MUNICIPIO: <u>' + str(vocero.zona.comunidad.parroquia.idmunicipiocompleto) + '</u>, ESTADO: <u>' + str(vocero.zona.comunidad.parroquia.idmunicipiocompleto.idestado) + '</u>', styles['miNormal']))
		elements.append(Paragraph('<b>DATOS GENERALES DE LA COMUNIDAD</b>', styles['centrado']))
		elements.append(Paragraph('<b>Resumen del Censo:</b>', styles['Normal']))

		c1 = Paragraph('''<b>Nro. de Viviendas</b>''', styles["cabeceraTabla"])
		c2 = Paragraph('''<b>Nro. de Familias</b>''', styles["cabeceraTabla"])
		c3 = Paragraph('''<b>Nro. de Habitantes</b>''', styles["cabeceraTabla"])
		c4 = Paragraph('''<b>Menores de 0 a 14 años</b>''', styles["cabeceraTabla"])
		c5 = Paragraph('''<b>Menores de 15 a 17 años</b>''', styles["cabeceraTabla"])
		c6 = Paragraph('''<b>Mayores de 18 a 100 años</b>''', styles["cabeceraTabla"])
		c7 = Paragraph('''<b>Inscritos en el C.N.E.</b>''', styles["cabeceraTabla"])
		c8 = Paragraph('''<b>Nro. de Electores</b>''', styles["cabeceraTabla"])

		cabeceraTabla = (
			c1,
			c2,
			c3,
			c4,
			c5,
			c6,
			c7,
			c8
		)

		data=[
			[
				vivienda.count(),
				hogar.count(),
				miembroHogar.count(),
				grupoEtario1.count(),
				grupoEtario2.count(),
				grupoEtario3.count(),
				inscritosCNE.count(),
				'?'
			]
		]

		tabla = Table([cabeceraTabla] + data, colWidths=[(doc.width-20)/8]*8)
		tabla.setStyle(TableStyle(
		    [
		        ('GRID', (0, 0), (7, -1), 0.5, colors.black),
		        ('ALIGN',(0,0),(7,-1),'CENTER'),
		        ('VALIGN',(0,0),(7,-1),'MIDDLE'),
		        # ('LINEBELOW', (0, 0), (-1, 0), 2, colors.white),
		        ('BACKGROUND', (0, 0), (-1, 0), '#ebebeb')
		    ]
		))

		elements.append(tabla)

		doc.build(elements, canvasmaker=pintaCabeceraPie)

		# Get the value of the BytesIO buffer and write it to the response.
		pdf = buffer.getvalue()
		buffer.close()
		return pdf