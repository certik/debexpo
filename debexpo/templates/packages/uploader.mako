# -*- coding: utf-8 -*-
<%inherit file="list.mako"/>

<%def name="main()">

<h1>${ _('Packages uploaded by %s' % c.username) }</h1>

${self.list()}

</%def>
