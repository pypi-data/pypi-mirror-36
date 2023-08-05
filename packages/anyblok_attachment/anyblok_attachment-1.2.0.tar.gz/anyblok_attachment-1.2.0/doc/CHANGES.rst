.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

CHANGELOG
=========

1.2.0 (2018-09-14)
------------------

* Allow to get another field to represent the file
* PR #4: Added a column name on the template to identify them easyly (@GohuHQ)
* PR #3: Fixed option name for wkhtmltopdf (@GohuHQ)

1.1.1 (2018-06-05)
------------------

* Fix the mixins come from **anyblok_mixins**

1.1.0 (2018-05-16)
------------------

* [ADD] add Mixin ``Mixin.LatestDocument`` and ``Mixin.VersionedDocument``
  to help the developer to get **latest_document** or **versioned_document**

1.0.2 (2018-02-24)
------------------

* [REF] Anyblok 0.17.0 changed setter to add application and application 
  groups, So I had to adapt the existing to use new setter

1.0.1 (2018-01-11)
------------------

* [FIX] ``Mixin.WkHtml2Pdf`` check also if the configuration changed for 
  **Template.check_if_file_must_be_generated**

1.0.0 (2018-01-10)
------------------

* [ADD] **attachment** blok: stock versionned file
* [ADD] **report** blok: create versionned file from template
* [ADD] **report-format** blok: template type
* [ADD] **wkhtml2pdf** blok: convert html to pdf in the template
