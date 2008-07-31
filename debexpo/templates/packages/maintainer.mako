# -*- coding: utf-8 -*-
<%inherit file="list.mako"/>

<%def name="main()">

<h1>${ _('Packages maintained by %s') % c.maintainer }</h1>

${self.list()}

</%def>
