# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>${ _('What is mentors.debian.net?') }</h1>
   <p>
      ${ _('''Only approved members of the Debian project - so-called <i>Debian
      Developers</i> - are granted the permission to upload software packages
      into the Debian distribution. Still a large number of packages is
      maintained by non-official developers. How do they get their work into
      Debian when they are not allowed to upload their own packages directly?
      By means of a process called <i>sponsorship</i>. Don't worry - it does
      not deal with money. Sponsorship means that a Debian developer uploads
      the package on behalf of the actual maintainer. The Debian developer
      will also check the package for technical correctness and help the
      maintainer to improve the package if necessary. Therefore the sponsor is
      sometimes also called a <i>mentor</i>.''') }
   </p>

   <h1>${ _('I want to have my package uploaded to Debian') }</h1>
   <p>
      ${ _('''Thank you for your contribution to Debian. This service is
      dedicated to get your package into Debian quickly and without much fuss.
      Please go to our <a href="%s#maintainer">introductory
      page for maintainers</a> and learn how to use mentors.debian.net.'''
      % h.rails.url_for('intro')) }
   </p>

   <h1>${ _('I am a Debian developer and want to offer sponsorship') }</h1>
   <p>
      ${ _('''Do you remember how hard it was to get your packages into Debian
      before you were accepted as a Debian developer? Sponsorees depend on your
      help to get their packages into good shape and upload them to Debian. 
      Please go to our <a href="%s#sponsor">introductory page
      for sponsors</a> to learn how you can help best.'''
      % h.rails.url_for('intro')) }
   </p>
   
<h1>${ _('Recently uploaded packages') }</h1>

<%include file="../packages/list.mako" />
