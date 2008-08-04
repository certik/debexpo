# -*- coding: utf-8 -*-
<%inherit file="list.mako"/>

<h1>${ _('Packages maintained by %s') % c.maintainer }</h1>

${self.list()}
