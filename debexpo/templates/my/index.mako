# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>${ _('My account') }</h1>

<fieldset>
  <legend>${ _('Change details') }</legend>

  ${ h.rails.form(h.url_for()) }
  ${ h.rails.hidden_field('form', 'details') }

  <table>
    <tr>
      <td>${ _('Name') }:</td>
      <td>${ h.rails.text_field('name', value=c.user.name) }</td>
    </tr>

    <tr>
      <td>${ _('E-mail') }:</td>
      <td>${ h.rails.text_field('email', value=c.user.email) }</td>
    </tr>

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.rails.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change GPG key') }</legend>

  ${ h.rails.form(h.url_for(), multipart=True) }
  ${ h.rails.hidden_field('form', 'gpg') }

  <table>

% if c.currentgpg:

    <tr>
      <td>${ _('Current GPG key') }:</td>
      <td>${ c.currentgpg }</td>
    </tr>

    <tr>
      <td>${ _('Delete current key') }:</td>
      <td>${ h.rails.check_box('delete_gpg') }</td>
    </tr>

% else:

    ${ h.rails.hidden_field('delete_gpg', 0) }

% endif

    <tr>
      <td>${ _('GPG key') }:</td>
      <td>${ h.rails.file_field('gpg') }</td>
    </tr>

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>

   </table>

  ${ h.rails.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change password') }</legend>

  ${ h.rails.form(h.url_for()) }
  ${ h.rails.hidden_field('form', 'password') }

  <table>
    <tr>
      <td>${ _('Current password') }:</td>
      <td>${ h.rails.password_field('password_current') }</td>
    </tr>

    <tr>
      <td>${ _('New password') }:</td>
      <td>${ h.rails.password_field('password_new') }</td>
    </tr>

    <tr>
      <td>${ _('Confirm new password') }:</td>
      <td>${ h.rails.password_field('password_confirm') }</td>
    </tr>

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.rails.end_form() }

</fieldset>

<fieldset>
  <legend>${ _('Change other details') }</legend>

  ${ h.rails.form(h.url_for()) }
  ${ h.rails.hidden_field('form', 'other_details') }

  <table>
    <tr>
      <td>${ _('Country') }:</td>
      <td>${ h.rails.select('country', h.rails.options_for_select(c.countries, c.current_country)) }</td>
    </tr>

    <tr>
      <td>${ _('IRC nickname') }:</td>
      <td>${ h.rails.text_field('ircnick', value=c.user.ircnick) }</td>
    </tr>

    <tr>
      <td>${ _('Jabber address') }:</td>
      <td>${ h.rails.text_field('jabber', value=c.user.jabber) }</td>
    </tr>

% if c.config['debexpo.debian_specific'] == 'true':

    % if c.debian_developer:

        <tr>
          <td>${ _('Debian status') }:</td>
          <td>${ _('Debian Developer') }</td>
        </tr>
	${ h.rails.hidden_field('status') }

    % else:

        <tr>
          <td><a href="http://wiki.debian.org/Maintainers">${ _('Debian Maintainer') }</a>:</td>
          <td>${ h.rails.check_box('status', checked=c.debian_maintainer) }</td>
        </tr>

    % endif

% else:

    ${ h.rails.hidden_field('status') }

% endif

    <tr>
      <td>${ h.rails.submit(_('Submit')) }</td>
    </tr>
  </table>

  ${ h.rails.end_form() }

</fieldset>
