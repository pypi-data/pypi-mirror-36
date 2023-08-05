django-tables2-column-shifter
------------------------------


.. image:: https://badge.fury.io/py/django-tables2-column-shifter.svg
    :target: https://badge.fury.io/py/django-tables2-column-shifter
    :alt: Latest PyPI version


.. image:: https://travis-ci.org/djk2/django-tables2-column-shifter.svg?branch=master
    :target: https://travis-ci.org/djk2/django-tables2-column-shifter
    :alt: Travis CI


.. image:: https://requires.io/github/djk2/django-tables2-column-shifter/requirements.svg?branch=master
    :target: https://requires.io/github/djk2/django-tables2-column-shifter/requirements/?branch=master
    :alt: Requirements Status


About the app:
Simple extension for django-tables2 to dynamically show or hide columns using jQuery.
Application uses web storage to store information whih columns are visible or not.
Using JQuery, Bootstrap3 or Bootstrap4 and Django >=1.9.

- Tested by tox with:

    * Python :2.7, 3.6, 3.7
    * Django : 1.9, 1.10, 1.11, 2.0, 2.1
    * django-tables2 : 1.5, 1.6, ..., 1.21, 2.0, master

- Supported:

    * Django >= 1.9
    * django-tables2 >= 1.5.0 (earlier version probably will be work but wasn't tested)
    * **bootstrap2** / **bootstrap3** / **bootstrap4** / **bootstrap4.1.3**
    * **JQuery**

- Supported locale:

    * EN        - (English)
    * PL        - (Polish)
    * EL        - (Greek / Hellenic Republic)
    * PT-BR     - (Portuguese - Brazilian)


More information about django-tables in here: https://django-tables2.readthedocs.io/


Screens:
----------

.. image:: https://raw.githubusercontent.com/djk2/django-tables2-column-shifter/master/doc/static/scr1.png
    :alt: screen 1

.. image:: https://raw.githubusercontent.com/djk2/django-tables2-column-shifter/master/doc/static/scr2.png
    :alt: screen 2


How to Install:
---------------
1. Install django-tables2-column-shifter using::


        pip install django-tables2-column-shifter

    or

        pip install git+https://github.com/djk2/django-tables2-column-shifter

    or

        pip install django-tables2-column-shifter.zip

    or

        pip install django-tables2-column-shifter.tar.gz


2. Add ``django_tables2_column_shifter`` to your ``INSTALLED_APPS`` setting (after django_tables2) like this ::

    INSTALLED_APPS = [
        ...,
        'django_tables2',
        'django_tables2_column_shifter',
        ...,
    ]

3. Add path to js script: ``django_tables2_column_shifter.min.js`` in your base django template.
   Script must be add after jquery.js aand bootstrap.js and before </body> tag.


  base.html::

    {% load static %}

    <body>
        ...
        ...
        <script src="{% static "jquery.min.js" %}"></script> {# require #}
        <script src="{% static "bootstrap/js/bootstrap.min.js" %}"></script>

        <script
            type="text/javascript"
            src="{% static "django_tables2_column_shifter/js/django_tables2_column_shifter.min.js" %}">
        </script>
    </body>


Usage:
------
To use app, you must inherit your table class from ``django_tables2_column_shifter.tables.ColumnShiftTable``

  models.py - create normal model::

    from django.db import models

    class MyModel(models.Model):
        first_name = models.CharField("First name", max_length=50)
        last_name = models.CharField("Last name", max_length=50)

  tables.py - change inherit to ColumnShiftTable::

    from django_tables2_column_shifter.tables import ColumnShiftTable
    from app.models import MyModel

    # By default you probably inherit from django_table2.Table
    # Change inherit to ColumnShiftTable
    class MyModelTable(ColumnShiftTable):
        class Meta:
            model = MyModel

  views.py - In your view, nothing changes::

    from .tables import MyModelTable
    from .models import MyModel

    def simple_list(request):
        queryset = MyModel.objects.all()
        table = MyModelTable(queryset)
        return render(request, 'template.html', {'table': table})

  template.html - use default render_table tag to display table object (using bootstrap3 / bootstrap4)::

    {% extends "base.html" %}
    {% load django_tables2 %}
    {% render_table table %}
    
To retrieve the invisible columns you can use the ``$.django_tables2_column_shifter_hidden()`` API. You can either pass the 0-based index of the table in the page (i.e use ``$.django_tables2_column_shifter_hidden(1)`` to get the hidden columns for the 2nd table in the page) or just use it without parameters to retrieve the hidden columns for the first table. This API returns an array with the invisible column names.

These columns can then be used when you want to export only the visible columns, ie  when the user clicks on the export button it would append an ``&excluded_columns=col1,col2`` to the export button's ``href`` which would then be used by the django-tables2 ``TableExporter``   (http://django-tables2.readthedocs.io/en/latest/pages/export.html#excluding-columns) to exclude these cols, i.e something like

    exporter = TableExport('csv', table, exclude_columns=self.request.GET.get('excluded_columns').split(',))


Bootstrap2 (support for old projects):
--------------------------------------
If you use Bootstrap v2 in your project then your Table class should inherit from `ColumnShiftTableBootstrap2`
imported from `django_tables2_column_shifter.tables`.


Warnings:
----------

- **Warning** : - If you use {% render_table %} tag with queryset (not table class instance),
  django-tables2-column-shifter will not be work. Queryset does not have ``template`` attribute::

    {% load django_tables2 %}
    {% render_table queryset %} {# not work #}


- **Warning** : - If you use a different template than ``django_tables2_column_shifter/table.html``
  to render your table, probably django-tables2-column-shifter will not be work.
  Your custom template should inherit from ``django_tables2_column_shifter/table.html``


Customizing:
-------------
1. If you use more then one instance of the same Table class, you should use a different prefix for each instance::

    tab1 = MyModelTable(queryset, prefix='tab1')
    tab2 = MyModelTable(queryset, prefix='tab2')
    tab3 = MyModelTable(queryset, prefix='tab3')

2. To disable shifter mechanism - set ``False`` to ``shift_table_column`` in your table class (default value is True)::

    class MyModelTable(ColumnShiftTable):
       shift_table_column = False
       ...


3. By default, all columns from sequence are visible, if you want limit visible columns,
   override method ``get_column_default_show(self)`` like that::

    class MyModelTable(ColumnShiftTable):
        def get_column_default_show(self):
            self.column_default_show = ['column1', 'column2']
            return super(MyModelTable, self).get_column_default_show()


Run demo:
---------
1. Download or clone project from `https://github.com/djk2/django-tables2-column-shifter`::

    git clone https://github.com/djk2/django-tables2-column-shifter.git

2. Go to testproject directory::

    cd django-tables2-column-shifter/testproject

3. Install requirements::

    pip install -r requirements.txt

4. Run django developing server::

    python manage.py runserver


Links:
--------
- `Django documentation <https://docs.djangoproject.com/en/dev/>`_
- `django-tables2 documentation <https://django-tables2.readthedocs.io/en/latest/>`_
