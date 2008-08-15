# -*- coding: utf-8 -*-
<%inherit file="base.mako"/>To: ${ c.to }
Subject: Accepted ${ c.changes['Source'] } ${ c.changes['Version'] } (${ c.changes['Architecture'] })

${ c.changes_contents }

Accepted:
% for file in c.changes['Files']:
${ file['name'] }
  to ${ c.dest }/${ file['name'] }
% endfor
