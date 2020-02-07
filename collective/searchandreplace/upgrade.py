from collective.searchandreplace.interfaces import ISearchReplaceSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtilitiesFor
from zope.component import getUtility

import logging


PROFILE_ID = "profile-collective.searchandreplace:default"
logger = logging.getLogger("collective.searchandreplace")


def dummy_upgrade_step(context):
    return


def add_control_panel_and_upgrade_settings(context):
    # We have added an interface ISearchReplaceSettings and want a controlpanel
    # for it.  First we must remove the old maximum_text_characters setting,
    # because it did not belong to an interface yet.  If we keep the old
    # settings, the controlpanel gets confused, complaining that the record
    # does not exist.
    registry = getUtility(IRegistry)
    record_name = "collective.searchandreplace.maximum_text_characters"
    maximum_text_characters = registry.get(record_name)
    if maximum_text_characters is not None:
        del registry.records[record_name]
    # Run the registry step, registering our interface
    context.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")
    # Register our control panel.
    context.runImportStepFromProfile(PROFILE_ID, "controlpanel")
    # Restore the previous setting.
    if maximum_text_characters is not None:
        # Use the new interface to set the value.
        settings = registry.forInterface(ISearchReplaceSettings)
        settings.maximum_text_characters = maximum_text_characters


def remove_behavior(context):
    # In version 6 we introduced a dexterity behavion, but in version 7 this is
    # no longer needed.  So we remove it from existing types, otherwise you get
    # warnings and errors in the logs when accessing a type.  It seems to cause
    # no harm.
    try:
        from plone.dexterity.interfaces import IDexterityFTI
    except ImportError:
        logger.info("No dexterity available, " "so there is no behavior to remove.")
        return
    behavior_name = "collective.searchandreplace.interfaces.ISearchReplaceable"
    for name, fti in getUtilitiesFor(IDexterityFTI):
        behaviors = list(fti.behaviors)
        if behavior_name not in behaviors:
            continue
        behaviors.remove(behavior_name)
        fti._updateProperty("behaviors", tuple(behaviors))
        logger.info("Removed behavior %s from type %s.", behavior_name, name)
