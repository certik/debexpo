# -*- coding: utf-8 -*-
<%inherit file="list.mako"/>

<h1>${ _('Packages uploaded by %s') % c.username }</h1>

${self.list()}
