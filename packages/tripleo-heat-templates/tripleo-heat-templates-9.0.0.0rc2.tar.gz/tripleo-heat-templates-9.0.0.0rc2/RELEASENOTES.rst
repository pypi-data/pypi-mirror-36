======================
tripleo-heat-templates
======================

.. _tripleo-heat-templates_9.0.0.0rc2:

9.0.0.0rc2
==========

.. _tripleo-heat-templates_9.0.0.0rc2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/stackrc-baremetal-version-309809c01105095f.yaml @ 128347fbd724a77e4a603d2e18b59fc58604ec89

- The baremetal API version is no longer hardcoded in ``stackrc``. This
  allows easy access to new features in *ironicclient* as they are
  introduced. If you need to use a fixed API version, set the
  ``OS_BAREMETAL_API_VERSION`` environment variable.

