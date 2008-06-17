# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="list()">

<table>
  <tr>
    <th>${ _('Package') }</th>
    <th>${ _('Description') }</th>
    <th>${ _('Version') }</th>
    <th>${ _('Uploader') }</th>
    <th>${ _('Needs a sponsor') }</th>
  </tr>

% for package in c.packages:
  <tr>
    <td class="lines"><a href="${ h.url_for('package', package=package['name']) }">${ package['name'] }</a></td>
    <td class="lines">${ package['description'] }</td>
    <td class="lines">${ package['version'] }</td>
    <td class="lines">${ package['uploader'] }</td>
    <td class="lines">${ package['needs_sponsor'] }</td>
  </tr>
% endfor

</table>

</%def>
