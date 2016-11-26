# -*- coding: utf-8
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Condicionfisicavivienda(models.Model):
    idcondicionfisicavivienda = models.IntegerField(db_column='idCondicionFisicaVivienda', primary_key=True)
    nombrecondicionfisicavivienda = models.CharField(db_column='nombreCondicionFisicaVivienda', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombrecondicionfisicavivienda

    class Meta:
        db_table = 'condicionFisicaVivienda'
        verbose_name = "Condicion Físicasica de la Vivienda"
        verbose_name_plural = "Condiciones Físicas de la Vivienda"


class Comunidad(models.Model):
    idcomunidad = models.IntegerField("R.I.F. Consejo Comunal", db_column='idComunidad', primary_key=True)
    nombrecomunidad = models.CharField("Nombre Consejo Comunal",db_column='nombreComunidad', max_length=255, blank=True, null=True)
    poligonal = models.TextField("Coordenadas poligonal", db_column='poligonal', blank=True, null=True)
    tipovia = models.ForeignKey('Tipovia', on_delete=models.PROTECT, db_column='idTipoVia', verbose_name="Tipo de v\xeda", blank=True, null=True)
    nombrevia = models.CharField("Nombre de la vía", db_column='nombreVia', max_length=255, blank=True, null=True)
    tipolocalidad = models.ForeignKey('Tipolocalidad', on_delete=models.PROTECT, db_column='idTipoLocalidad', verbose_name="Tipo de localidad", blank=True, null=True)
    nombrelocalidad = models.CharField("Nombre de la localidad", db_column='nombreLocalidad', max_length=255, blank=True, null=True)
    tipolocal = models.ForeignKey('Tipovivienda', on_delete=models.PROTECT, db_column='idTipoLocal', verbose_name="Tipo de local", blank=True, null=True)
    nombrelocal = models.CharField("Nombre del local", db_column='nombreLocal', max_length=255, blank=True, null=True)
    pisolocal = models.CharField("Piso del local", db_column='pisoLocal', max_length=255, blank=True, null=True)
    numerolocal = models.CharField("Número/nombre del local", db_column='numeroLocal', max_length=255, blank=True, null=True)
    referencialocal = models.CharField("Referencia", db_column='referenciaLocal', max_length=255, blank=True, null=True)
    parroquia = models.ForeignKey('Parroquia', on_delete=models.PROTECT, db_column='idParroquia', verbose_name="Parroquia", blank=True, null=True)
    coordenadas = models.CharField("Coordenadas ubicación", db_column='coordenadas', max_length=255, blank=True, null=True)
    centrocoordenadas = models.CharField("Centro de coordenadas", db_column='centroCoordenadas', max_length=255, blank=True, null=True)
    tipocomunidad = models.ForeignKey('Tipocomunidad', on_delete=models.PROTECT, db_column='idTipoComunidad', verbose_name="Tipo de Comunidad", blank=True, null=True)


    def save(self, force_insert=False, force_update=False):
        self.nombrecomunidad = self.nombrecomunidad.upper()
        self.nombrevia = self.nombrevia.upper()
        self.nombrelocalida = self.nombrelocalida.upper()
        self.nombrelocal = self.nombrelocal.upper()
        self.pisolocal = self.pisolocal.upper()
        self.numerolocal = self.numerolocal.upper()
        self.referencialocal = self.referencialocal.upper()
        super(Comunidad, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.nombrecomunidad

    class Meta:
        default_permissions = (
            ('view_comunidad', 'Can view Comunidad'),
        )
        db_table = 'comunidad'
        verbose_name = "Comunidad"
        verbose_name_plural = "Comunidades"


class Discapacidad(models.Model):
    iddiscapacidad = models.AutoField(db_column='idDiscapacidad', primary_key=True)  # Field name made lowercase.
    tipodiscapacidad = models.ForeignKey('Tipodiscapacidad', on_delete=models.PROTECT, db_column='idTipoDiscapacidad', blank=True, null=True)  # Field name made lowercase.
    nombrediscapacidad = models.CharField(db_column='nombreDiscapacidad', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __unicode__(self):
        return self.nombrediscapacidad

    class Meta:
        db_table = 'discapacidad'
        verbose_name = "Discapacidad"
        verbose_name_plural = "Discapacidades"
        ordering = ['tipodiscapacidad','nombrediscapacidad']


class Estado(models.Model):
    idestado = models.CharField(db_column='idEstado', primary_key=True, max_length=255)
    nombreestado = models.CharField(db_column='nombreEstado', max_length=255)

    def __unicode__(self):
        return self.nombreestado

    class Meta:
        managed = False
        db_table = 'estado'


class Etnia(models.Model):
    idetnia = models.AutoField(db_column='idEtnia', primary_key=True)
    nombreetnia = models.CharField("Etnia", db_column='nombreEtnia', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombreetnia

    class Meta:
        managed = False
        db_table = 'etnia'


class Gradoinstruccion(models.Model):
    idgradoinstruccion = models.AutoField(db_column='idGradoInstruccion', primary_key=True)
    nombregradoinstruccion = models.CharField(db_column='nombreGradoInstruccion', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombregradoinstruccion

    class Meta:
        db_table = 'gradoInstruccion'


class Hogar(models.Model):
    idhogar = models.AutoField(db_column='idHogar', primary_key=True)
    nombrehogar = models.CharField(db_column='nombreHogar', verbose_name="Nombre familia", max_length=255, blank=True, null=True)
    vivienda = models.ForeignKey('Vivienda', on_delete=models.PROTECT, db_column='idVivienda', verbose_name="Vivienda", blank=True, null=True)
    tipopropiedadvivienda = models.ForeignKey('Tipopropiedadvivienda',  on_delete=models.PROTECT, db_column='idTipoPropiedadVivienda', verbose_name="Tipo de Propiedad", blank=True, null=True)

    def save(self, force_insert=False, force_update=False):
        self.nombrehogar = self.nombrehogar

    def save(self, force_insert=False, force_update=False):
        self.nombrehogar = self.nombrehogar.upper()
        super(Hogar, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.nombrehogar

    class Meta:
        db_table = 'hogar'
        verbose_name = "Hogar"
        verbose_name_plural = "Hogares"


class Miembrohogar(models.Model):
    idmiembrohogar = models.AutoField(db_column='idMiembroHogar', primary_key=True)
    hogar = models.ForeignKey(Hogar,  on_delete=models.PROTECT, db_column='idHogar', blank=True, null=True)
    parentesco = models.ForeignKey('Parentesco',  on_delete=models.PROTECT, db_column='idParentesco', verbose_name='Parentesco', blank=True, null=True)
    persona = models.OneToOneField('Persona', on_delete=models.PROTECT, db_column='idPersona', verbose_name='Persona')

    def __unicode__(self):
        return '%s %s' % (self.hogar, self.persona)

    class Meta:
        db_table = 'miembroHogar'
        verbose_name = "Miembro de hogar"
        verbose_name_plural = "Miembros de hogar"


class Municipio(models.Model):
    idmunicipiocompleto = models.CharField(db_column='idMunicipioCompleto', primary_key=True, max_length=255)
    idestado = models.ForeignKey(Estado,  on_delete=models.PROTECT, db_column='idEstado')
    idmunicipio = models.CharField(db_column='idMunicipio', max_length=255)
    nombremunicipio = models.CharField(db_column='nombreMunicipio', max_length=255)

    def __unicode__(self):
        return self.nombremunicipio

    class Meta:
        managed = False
        db_table = 'municipio'


class Pais(models.Model):
    idpais = models.AutoField(db_column='idPais', primary_key=True, max_length=3)
    codisopais = models.CharField(db_column='codISOPais', max_length=3, blank=True, null=True)
    nombrepais = models.CharField(db_column='nombrePais', max_length=255, blank=True, null=True)
    nombrepaisiso = models.CharField(db_column='nombreISOPais', max_length=255, blank=True, null=True)
    codisopaisalfa2 = models.CharField(db_column='codISOPaisAlfa2', max_length=2, blank=True, null=True)
    codisopaisalfa3 = models.CharField(db_column='codISOPaisAlfa3', max_length=3, blank=True, null=True)

    def __unicode__(self):
        return self.nombrepais

    class Meta:
        db_table = 'pais'


class Parentesco(models.Model):
    idparentesco = models.AutoField(db_column='idParentesco', primary_key=True)
    nombreparentesco = models.CharField(db_column='nombreParentesco', max_length=255, blank=True, null=True)
    ordenparentesco = models.IntegerField(db_column='ordenParentesco', blank=True, null=True)

    def __unicode__(self):
        return self.nombreparentesco

    class Meta:
        db_table = 'parentesco'
        ordering = ['ordenparentesco']


class Parroquia(models.Model):
    idparroquiacompleto = models.CharField(db_column='idParroquiaCompleto', primary_key=True, max_length=255)
    idmunicipiocompleto = models.ForeignKey(Municipio,  on_delete=models.PROTECT, db_column='idMunicipioCompleto')
    idestadoprroquia = models.CharField(db_column='idEstadoPrroquia', max_length=255)
    idmunicipioparroquia = models.CharField(db_column='idMunicipioParroquia', max_length=255)
    idparroquia = models.CharField(db_column='idParroquia', max_length=255)
    nombreparroquia = models.CharField(db_column='nombreParroquia', max_length=255)

    def __unicode__(self):
        return self.nombreparroquia

    class Meta:
        managed = False
        db_table = 'parroquia'


class Patologia(models.Model):
    idpatologia = models.AutoField(db_column='idPatologia', primary_key=True)
    nombrepatologia = models.CharField("Nombre",db_column='nombrePatologia', max_length=255, blank=True, null=True)
    descripcionpatologia = models.CharField("Descripción",db_column='descripcionPatologia', max_length=255, blank=True, null=True)


    def save(self, force_insert=False, force_update=False):
        self.nombrepatologia = self.nombrepatologia.upper()
        super(Patologia, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.nombrepatologia

    class Meta:
        db_table = 'patologia'
        verbose_name = "Patología"
        verbose_name_plural = "Patologías"
        ordering = ['nombrepatologia']


class Persona(models.Model):
    SEXO_CHOICES = (
        ('F', 'FEMENINO'),
        ('M', 'MASCULINO'),
    )
    LETRACEDULA_CHOICES = (
        ('V', 'V'),
        ('E', 'E'),
    )
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)
    rif = models.CharField("R.I.F.",db_column='rif', max_length=255, blank=True, null=True)
    letracedulaidentidad = models.CharField(db_column='letraCedulaIdentidad', max_length=1, choices=LETRACEDULA_CHOICES, default=LETRACEDULA_CHOICES[0][0], blank=False, null=False)
    cedulaidentidad = models.IntegerField("Cédula de Identidad",db_column='cedulaIdentidad', unique=True, blank=False, null=False)
    nombre = models.CharField("Primer Nombre", db_column='nombre', max_length=255, blank=False, null=False)
    otrosnombres = models.CharField("Otros Nombres", db_column='otrosNombres', max_length=255, blank=True, null=True)
    apellido = models.CharField("Primer Apellido", db_column='apellido', max_length=255, blank=False, null=False)
    otrosapellidos = models.CharField("Otros Apellidos", db_column='otrosApellidos', max_length=255, blank=True, null=True)
    telefono = models.CharField("Teléfono Local", db_column='telefono', max_length=255, blank=True, null=True)
    celular = models.CharField("Teléfono Celular", db_column='celular', max_length=255, blank=True, null=True)
    email = models.EmailField("Correo Electrónico", db_column='email', max_length=255, blank=True, null= True)
    twitter = models.CharField("Twitter",db_column='twitter', max_length=255, blank=True, null=True)
    fechanacimiento = models.DateField("Fecha de Nacimiento", db_column='fechaNacimiento', blank=True, null=True)
    padre = models.ForeignKey('self',  on_delete=models.SET_NULL, verbose_name="Padre", db_column='padre', related_name='idPadre', blank=True, null=True)
    madre = models.ForeignKey('self',  on_delete=models.SET_NULL, verbose_name="Madre", db_column='madre', related_name='idMadre', blank=True, null=True)
    conyuge = models.ForeignKey('self',  on_delete=models.SET_NULL, verbose_name="Conyuge", db_column='conyuge', related_name='idConyuge', blank=True, null=True)
    sexo = models.CharField("Sexo", db_column='sexo', max_length=255, choices=SEXO_CHOICES, blank=False, null=False)
    paisnacimiento = models.ForeignKey(Pais,  on_delete=models.PROTECT, db_column='paisNacimiento', verbose_name="País de Nacimiento", blank=True, null=True)
    fecharegistro = models.DateField("Fecha de Registro", db_column='fechaRegistro', default=datetime.now().strftime("%Y-%m-%d"))
    authuser = models.OneToOneField(User, db_column='authuser', on_delete=models.PROTECT, unique=True, blank=True, null=True)
    pasaporte = models.CharField("Pasaporte", db_column='pasaporte', max_length=255, blank=True, null=True)
    etnia = models.ForeignKey(Etnia,  on_delete=models.PROTECT, db_column='etnia', verbose_name="Etnia", blank=True, null=True)
    foto = models.ImageField(upload_to = 'foto', db_column='foto', verbose_name="Foto", blank=True, null=True)
    cne = models.CharField("CNE", db_column='cne', max_length=255, blank=True, null=True)

    def save(self, force_insert=False, force_update=False):
        self.rif = self.rif.upper()
        self.nombre = self.nombre.upper()
        self.otrosnombres = self.otrosnombres.upper()
        self.apellido = self.apellido.upper()
        self.otrosapellidos = self.otrosapellidos.upper()
        self.pasaporte = self.pasaporte.upper()
        super(Persona, self).save(force_insert, force_update)

    def __unicode__(self):
        return '%s %s %s %s' % (self.nombre, self.otrosnombres, self.apellido, self.otrosapellidos)

    class Meta:
        db_table = 'persona'
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        #ordering = ['nombrepersona','otrosnombrespersona','apellidopersona','otrosapellidospersona']


class Tipoapoyo(models.Model):
    idtipoapoyo = models.AutoField(db_column='idTipoApoyo', primary_key=True)
    nombretipoapoyo = models.CharField(db_column='nombreTipoApoyo', max_length=255, blank=True, null=True)
    descripciontipoapoyo = models.CharField(db_column='descripcionTipoApoyo', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombretipoapoyo

    class Meta:
        db_table = 'tipoApoyo'
        verbose_name = "Tipo de Apoyo"
        verbose_name_plural = "Tipos de Apoyo"
        ordering = ['nombretipoapoyo']


class Salud(models.Model):
    persona = models.OneToOneField('Persona', on_delete=models.PROTECT, db_column='idPersona', verbose_name='Persona', primary_key=True)
    conapdis = models.CharField("Certicado CONAPDIS",db_column='conapdis', max_length=255, blank=True, null=True, default=None)
    mtlp = models.BooleanField("MTLP",db_column='mtlp', default=False)
    alcoholismo = models.BooleanField("Alcoholismo",db_column='alcoholismo', default=False)
    tabaquismo = models.BooleanField("Tabaquismo",db_column='tabaquismo', default=False)
    drogas = models.BooleanField("Otras drogas",db_column='drogas', default=False)
    patologia = models.ManyToManyField(Patologia, db_column='idPatologia', verbose_name="Patologías", blank=True)
    tipoapoyo = models.ManyToManyField(Tipoapoyo, db_column='idTipoApoyo', verbose_name="Tipo de apoyo", blank=True)
    discapacidad = models.ManyToManyField(Discapacidad, db_column='idDiscapacidad', verbose_name="Discapacidad(es)", blank=True)
    cuidador = models.ForeignKey('Persona',  on_delete=models.SET_NULL, db_column='cuidador', related_name ='+', verbose_name='Guía / Cuidadador', blank=True, null=True)

    def __unicode__(self):
        return '%s %s %s %s' % (self.persona.nombre, self.persona.otrosnombres, self.persona.apellido, self.persona.otrosapellidos)

    class Meta:
        db_table = 'salud'
        verbose_name = "Perfil de Salud"
        verbose_name_plural = "Perfiles de Salud"


class Tipocomunidad(models.Model):
    idtipocomunidad = models.AutoField(db_column='idTipoComunidad', primary_key=True)  # Field name made lowercase.
    nombretipocomunidad = models.CharField(db_column='nombreTipoComunidad', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __unicode__(self):
        return self.nombretipocomunidad

    class Meta:
        db_table = 'tipoComunidad'
        verbose_name = "Tipo de Comunidad"
        verbose_name_plural = "Tipos de Comunidad"
        ordering = ['nombretipocomunidad']


class Tipodiscapacidad(models.Model):
    idtipodiscapacidad = models.AutoField(db_column='idTipoDiscapacidad', primary_key=True)  # Field name made lowercase.
    nombretipodiscapacidad = models.CharField(db_column='nombreTipoDiscapacidad', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __unicode__(self):
        return self.nombretipodiscapacidad

    class Meta:
        db_table = 'tipoDiscapacidad'
        verbose_name = "Tipo de Discapacidad"
        verbose_name_plural = "Tipos de Discapacidad"
        ordering = ['nombretipodiscapacidad']


class Tipolocalidad(models.Model):
    idtipolocalidad = models.IntegerField(db_column='idTipoLocalidad', primary_key=True)
    nombretipolocalidad = models.CharField(db_column='nombreTipoLocalidad', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombretipolocalidad

    class Meta:
        db_table = 'tipoLocalidad'
        verbose_name = "Tipo de Localidad"
        verbose_name_plural = "Tipos de Localidad"


class Tipovia(models.Model):
    idtipovia = models.IntegerField(db_column='idTipoVia', primary_key=True)
    nombretipovia = models.CharField(db_column='nombreTipoVia', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombretipovia

    class Meta:
        db_table = 'tipoVia'
        verbose_name = "Tipo de Vía"
        verbose_name_plural = "Tipos de Vía"


class Tipopropiedadvivienda(models.Model):
    idtipopropiedadvivienda = models.AutoField(db_column='idTipoPropiedadVivienda', primary_key=True)
    nombretipopropiedadvivienda = models.CharField(db_column='nombreTipoPropiedadVivienda', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombretipopropiedadvivienda

    class Meta:
        db_table = 'tipoPropiedadVivienda'
        ordering = ['nombretipopropiedadvivienda']


class Tipovivienda(models.Model):
    idtipovivienda = models.IntegerField(db_column='idTipoVivienda', primary_key=True)
    nombretipovivienda = models.CharField(db_column='nombreTipoVivienda', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombretipovivienda

    class Meta:
        db_table = 'tipoVivienda'
        verbose_name = "Tipo de Vivienda"
        verbose_name_plural = "Tipos de Viviendas"


class Vivienda(models.Model):
    idvivienda = models.AutoField(db_column='idVivienda', primary_key=True)
    nombrevivienda = models.CharField("Nombre de la vivienda", db_column='nombreVivienda', max_length=255, blank=False, null=False)
    piso = models.CharField("Piso de la ", db_column='piso', max_length=255, blank=True, null=True)
    apartamento = models.CharField("Apartamento", db_column='apartamento', max_length=255, blank=True, null=True)
    nombrevia = models.CharField("Nombre de la vía", db_column='nombreVia', max_length=255, blank=True, null=True)
    nombrelocalidad = models.CharField("Nombre localidad", db_column='nombreLocalidad', max_length=255, blank=True, null=True)
    metroscuadrados = models.FloatField("Metros cuadrados", db_column='metrosCuadrados', blank=True, null=True)
    numerohabitaciones = models.IntegerField("Cant. de habitaciones", db_column='numeroHabitaciones', blank=True, null=True)
    numerobanos = models.IntegerField("Cant. de baños", db_column='numeroBanos', blank=True, null=True)
    condicionfisica = models.ForeignKey(Condicionfisicavivienda,  on_delete=models.PROTECT, db_column='condicionFisica', verbose_name="Condición Física", blank=True, null=True)
    zona = models.ForeignKey('Zona',  on_delete=models.PROTECT, db_column='idZona', verbose_name="Comunidad", blank=False, null=False, db_index=True)
    tipolocalidad = models.ForeignKey(Tipolocalidad,  on_delete=models.PROTECT, db_column='idTipoLocalidad', verbose_name="Tipo de localidad", blank=False, null=False)
    tipovia = models.ForeignKey(Tipovia,  on_delete=models.PROTECT, db_column='idTipoVia', verbose_name="Tipo de vía", blank=False, null=False)
    tipovivienda = models.ForeignKey(Tipovivienda,  on_delete=models.PROTECT, db_column='idTipoVivienda', verbose_name="Tipo de vivienda", blank=False, null=False)

    def __unicode__(self):
        return '%s PISO %s APTO. %s' % (self.nombrevivienda, self.piso, self.apartamento)

    class Meta:
        db_table = 'vivienda'
        verbose_name = "Vivienda"
        verbose_name_plural = "Viviendas"
        ordering = ['nombrevivienda','piso','apartamento']


class Vocero(models.Model):
    idvocero = models.AutoField(db_column='idVocero', primary_key=True)
    zona = models.ForeignKey('Zona', on_delete=models.PROTECT, db_column='idZona', blank=True, null=True, db_index=True)
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, db_column='idPersona', unique=True, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'vocero'


class Zona(models.Model):
    idzona = models.AutoField(db_column='idZona', primary_key=True)
    comunidad = models.ForeignKey(Comunidad,  on_delete=models.PROTECT, db_column='idComunidad', verbose_name="Comunidad", blank=True, null=True, db_index=True)
    nombrezona = models.CharField("Nombre de la zona", db_column='nombreZona', max_length=255, blank=True, null=True)
    descripcion = models.TextField("Descripción de la zona", db_column='descripcion', blank=True, null=True)

    def __unicode__(self):
        return '%s. ZONA: %s' % (self.comunidad, self.nombrezona)

    class Meta:
        db_table = 'zona'
        verbose_name = "Zona de la Comunidad"
        verbose_name_plural = "Zonas de la Comunidad"
        ordering = ['comunidad','nombrezona']