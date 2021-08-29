# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get(
    'smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler

    scheduler = Scheduler(
        db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# db.define_table('unidad',
#                 Field('tipo', 'string',
#                       requires=[IS_NOT_EMPTY(error_message=T('No puede ser vacío')),
#                                 IS_NOT_IN_DB(db, 'unidad.tipo', error_message=T('Ese valor ya existe'))])
#                 )

db.define_table('pieza',
                Field('codigo', 'string', label=T('Código')),
                Field('nombre', 'string'),
                Field('descripcion', 'text', label=T('Descripción')),
                Field('cantidad', 'integer'),
                Field('unidad', 'integer'),
                Field('precio_entrada', 'double'),
                Field('precio_salida', 'double'),
                Field('fecha_entrada', 'date')
                )

db.define_table('proveedor',
                Field('nombre', 'string', requires=[IS_NOT_EMPTY(error_message=T('No puede ser vacío'))],
                      label="Nombre"),
                Field('descripcion', 'text', label="Descripción"),
                Field('direccion', 'string', label="Dirección"),
                Field('telefono', 'string', label="Teléfono")
                )

db.define_table('pieza_proveedor',
                Field('id_pieza', 'reference pieza'),
                Field('id_proveedor', 'reference proveedor'),
                )

# Ventas

db.define_table('pieza_venta',
                Field('codigo', 'string'),
                Field('nombre', 'string'),
                Field('descripcion', 'text'),
                Field('cantidad', 'integer', label="Cantidad vendida"),
                Field('unidad', 'string'),
                Field('precio_entrada', 'double'),
                Field('precio_salida', 'double'),
                Field('fecha_entrada', 'date')
                )

db.define_table('proveedor_venta',
                Field('nombre', 'string'),
                Field('descripcion', 'text'),
                Field('direccion', 'string'),
                Field('telefono', 'string'),
                Field('id_pieza_venta', 'reference pieza_venta')
                )

db.define_table('venta',
                Field('fecha_salida', 'date'),
                Field('precio_total', 'double', label="Monto total"),
                Field('id_pieza_venta', 'reference pieza_venta')
                )

# Entradas

db.define_table('pieza_entrada',
                Field('codigo', 'string'),
                Field('nombre', 'string'),
                Field('descripcion', 'text'),
                Field('cantidad', 'integer'),
                Field('unidad', 'string'),
                Field('precio_entrada', 'double'),
                Field('precio_salida', 'double'),
                Field('fecha_entrada', 'date')
                )

db.define_table('proveedor_entrada',
                Field('nombre', 'string'),
                Field('descripcion', 'text'),
                Field('direccion', 'string'),
                Field('telefono', 'string'),
                Field('id_pieza_entrada', 'reference pieza_entrada')
                )

# ----------------------------------------------------------------------

db.pieza.id.readable = False
db.proveedor.id.readable = False

db.pieza.fecha_entrada.represent = lambda fecha_entrada, row: __format_fecha(fecha_entrada)
db.pieza_venta.fecha_entrada.represent = lambda fecha_entrada, row: __format_fecha(fecha_entrada)
db.venta.fecha_salida.represent = lambda fecha_salida, row: __format_fecha(fecha_salida)


# db.unidad.id.readable = False
# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


def __format_fecha(fecha):
    if fecha.month < 10:
        month = "0" + str(fecha.month)
    else:
        month = str(fecha.month)

    if fecha.day < 10:
        day = "0" + str(fecha.day)
    else:
        day = str(fecha.day)

    return day + "/" + month + "/" + str(fecha.year)