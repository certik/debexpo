# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="main()">

<h1>${ _('Sign up for a maintainer account') }</h1>

<fieldset>
  <legend>${ _('Account details') }</legend>

  ${ h.rails.form(h.rails.url_for(), method='post') }

  <table>
    <tr>
      <td>${ _('Full name') }:</td>
      <td>${ h.rails.text_field('name') }</td>
    </tr>
    
    <tr>
      <td>${ _('E-mail') }:</td>
      <td>${ h.rails.text_field('email') }</td>
    </tr>
    
    <tr>
      <td>${ _('Password') }:</td>
      <td>${ h.rails.password_field('password') }</td>
    </tr>
    
    <tr>
      <td>${ _('Confirm password') }:</td>
      <td>${ h.rails.password_field('password_confirm') }</td>
    </tr>

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.rails.end_form() }

</fieldset>

</%def>
