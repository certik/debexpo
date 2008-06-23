# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="main()">

<h1>${ _('My account') }</h1>

<fieldset>
  <legend>${ _('Change details') }</legend>

  ${ h.form(h.url_for()) }
  ${ h.hidden_field('form', 'details') }

  <table>
    <tr>
      <td>${ _('Name') }:</td>
      <td>${ h.text_field('name', value=c.user.name) }</td>
    </tr>

    <tr>
      <td>${ _('E-mail') }:</td>
      <td>${ h.text_field('email', value=c.user.email) }</td>
    </tr>

    <tr>
      <td>${ h.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change GPG key') }</legend>

  ${ h.form(h.url_for(), multipart=True) }
  ${ h.hidden_field('form', 'gpg') }

  <table>

% if c.currentgpg:

    <tr>
      <td>${ _('Current GPG key') }:</td>
      <td>${ c.currentgpg }</td>
    </tr>

    <tr>
      <td>${ _('Delete current key') }:</td>
      <td>${ h.check_box('delete_gpg') }</td>
    </tr>

% else:

    ${ h.hidden_field('delete_gpg', 0) }

% endif

    <tr>
      <td>${ _('GPG key') }:</td>
      <td>${ h.file_field('gpg') }</td>
    </tr>

    <tr>
      <td>${ h.submit(_('Submit')) }</td>
    </tr>

   </table>

  ${ h.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change password') }</legend>

  ${ h.form(h.url_for()) }
  ${ h.hidden_field('form', 'password') }

  <table>
    <tr>
      <td>${ _('Current password') }:</td>
      <td>${ h.password_field('password_current') }</td>
    </tr>
 
    <tr>
      <td>${ _('New password') }:</td>
      <td>${ h.password_field('password_new') }</td>
    </tr>
    
    <tr>
      <td>${ _('Confirm new password') }:</td>
      <td>${ h.password_field('password_confirm') }</td>
    </tr>
    
    <tr>
      <td>${ h.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change other details') }</legend>

  ${ h.form(h.url_for()) }
  ${ h.hidden_field('form', 'other_details') }

  <table>
    <tr>
      <td>${ _('Country') }:</td>
      <td>${ h.select('country', c.countries) }</td>
    </tr>

    <tr>
      <td>${ _('IRC nickname') }:</td>
      <td>${ h.text_field('ircnick', value=c.user.ircnick) }</td>
    </tr>

    <tr>
      <td>${ _('Jabber address') }:</td>
      <td>${ h.text_field('jabber', value=c.user.jabber) }</td>
    </tr>

% if c.config['debexpo.debian_specific'] == 'true':

    % if c.debian_developer:

        <tr>
          <td>${ _('Debian status') }:</td>
          <td>${ _('Debian Developer') }</td>
        </tr>
	${ h.hidden_field('status') }

    % else:

        <tr>
          <td><a href="http://wiki.debian.org/Maintainers">${ _('Debian Maintainer') }</a>:</td>
          <td>${ h.check_box('status', checked=c.debian_maintainer) }</td>
        </tr>

    % endif

% else:

    ${ h.hidden_field('status') }

% endif

    <tr>
      <td>${ h.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.end_form() }

</fieldset>

</%def>
