# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>${ _('Login') }</h1>

<fieldset>
  <legend>${ _('Login') }</legend>

  <p>${ _('Please login to continue') }</p>

% if c.message:
  <p><span class="error-message">${ c.message }</span></p>
% endif

  ${ h.rails.form_tag.form(h.rails.url_for(), method='post') }

  <table>
    <tr>
      <td>${ _('E-mail') }:</td>
      <td>${ h.rails.form_tag.text_field('email') }</td>
    </tr>

    <tr>
      <td>${ _('Password') }:</td>
      <td>${ h.rails.form_tag.password_field('password') }</td>
    </tr>

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.rails.end_form() }

</fieldset>
