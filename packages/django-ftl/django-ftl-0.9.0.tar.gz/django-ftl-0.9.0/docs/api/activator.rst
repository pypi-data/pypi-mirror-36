=================================
 Activating/deactivating locales
=================================

.. currentmodule:: django_ftl


.. function:: activate(locale_code)

   Activate a locale given by a BCP47 locale code (e.g. "en-US"). All
   :class:`~django_ftl.bundles.Bundle` objects will be switched to look for
   translation files with that locale.

   This uses a thread local variable internally to store the current locale.

.. function:: deactivate()

   De-activate the currently activated locale. All Bundles will throw exceptions
   if you try to generate messages with them, until you activate another
   language.

.. function:: override(locale_code)

   A Python context manager that uses :func:`activate` to set a locale on
   entry, and then re-activates the previous locale on exit. It can also be
   used a function decorator.
