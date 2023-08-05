.. This file is a part of the AnyBlok / Attachmment / Jinja project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.


See the documentation of `jinja2 <http://jinja.pocoo.org/docs/>`_

Add on your blok (example of name of your ``yourblok``) the jinja file.

**yourblok/templates/mytemplate.jinja2**::

    <title>{% block title %}{% endblock %}</title>
    <ul>
    {% for user in users %}
        <li><a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>

Create the **wkhtml2pdf** options if it does not exist::

    page = self.registry.Attachment.WkHtml2Pdf.Page.insert(
        label="tray_labels", size="A4")

    wkhtml2pdf = self.registry.Attachment.WkHtml2Pdf.insert(
        label="tray_labels",
        page=page,
        margin_top=5,
        margin_bottom=4,
        margin_left=3,
        margin_right=3,
        dpi=90,
    )

Create the template::

    self.registry.Attachment.Template.Jinja.insert(
        name="users",
        template_path='yourblok#=#templates/mytemplate.jinja2',  # source
        jinja_paths='yourblok#=#templates/report',  # other templates sources
        wkhtml2pdf_configuration=wkhtml2pdf,
        contenttype='application/pdf',
        model='Model.Users',  # Fake Model for example
        filename='mypage.pdf')

Create the document::

    template = registry.Attachment.Template.query().filter_by(
        name="users").one()
    users = registry.Users.query().limit(10).all()
    document = registry.Attachment.Document.insert(
        template=template,
        data={'users': [{'url': u.url, 'username': u.name} for u in users]}
    )
    document.get_file()
    assert document.version = V000001


.. note:: 

    All change in the data directory will force the creation of a new version of the document::

        users = registry.Users.query().offset(10).limit(10).all()
        document.data={'users': [{'url': u.url, 'username': u.name} for u in users]}
        document.get_file()
        assert document.version = V000002
