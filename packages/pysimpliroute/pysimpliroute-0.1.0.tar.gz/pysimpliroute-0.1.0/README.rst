PySimpliRoute
=======

Wrapper for the SimpliRoute service API

Installation
------------

::

    pip3 install pysimpliroute

Usage
-----

::

    from pysimpliroute import simpliroute as sr
    client = sr.Client(token='token_from_perfil')
    params = {
            "order": 1,
            "title": "Dansanti Test1",
            "address": "Parcela 19, culiprán, Melipilla, Chile",
            "latitude": "-33.774290",
            "longitude": "-71.250123",
            "contact_name": "Daniel",
            "contact_phone": "+123413123212",
            "contact_email": "apu@example.com",
            "reference": "invoice_id",
            "notes": "Leave at front door",
            "planned_date": "2018-08-19",
            "window_start": "19:00",
          }
    client.send_visit(params)
