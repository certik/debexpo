# -*- coding: utf-8 -*-
<%inherit file="list.mako"/>

<%def name="main()">

<h1>${ _('Packages in section %s' % c.section) }</h1>

${self.list()}

</%def>
