=============
keystoneauth1
=============

.. _keystoneauth1_3.11.0:

3.11.0
======

.. _keystoneauth1_3.11.0_New Features:

New Features
------------

.. releasenotes/notes/filter-versions-service-type-763af68092344b7a.yaml @ b'83be7453fa0cd36b504b9ec268bd09525376b944'

- Added ability to filter the results of ``get_all_version_data`` by
  service-type.

.. releasenotes/notes/filter-versions-service-type-763af68092344b7a.yaml @ b'83be7453fa0cd36b504b9ec268bd09525376b944'

- Added ``get_all_version_data`` to ``adapter.Adapter`` that uses the
  adapter's ``service_type`` to filter the version data fetched.


.. _keystoneauth1_3.11.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/ironic-microversions-a69bf92ab21f0cf5.yaml @ b'c40eb2951d5cf24589ea357a11aa252978636020'

- Fixed support for detecting microversion ranges on older Ironic
  installations.


.. _keystoneauth1_3.10.0:

3.10.0
======

.. _keystoneauth1_3.10.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bug-1733052-1b4af3b3fe1b05bb.yaml @ b'323f4e4bc4710d42e493eb56e40ba139a84d67b3'

- [`bug 1733052 <https://bugs.launchpad.net/keystoneauth/+bug/1733052>`_] Now the version discovery mechanism only fetches the version info from server side if the versioned url has been overrode. So that the request url's path won't be changed completely.

