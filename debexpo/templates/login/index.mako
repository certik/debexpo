# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="main()">

<h1>${ _('Login') }</h1>

<fieldset>
  <legend>${ _('Login') }</legend>

  <p>${ _('Please login to continue') }</p>

% if c.message:
  <p><span class="error-message">${ c.message }</span></p>
% endif

  ${ h.form(h.url_for(), method='post') }

  <table>
    <tr>
      <td>${ _('E-mail') }:</td>
      <td>${ h.text_field('email') }</td>
    </tr>
    
    <tr>
      <td>${ _('Password') }:</td>
      <td>${ h.password_field('password') }</td>
    </tr>
    
    <tr>
      <td>${ h.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.end_form() }

</fieldset>

</%def>
