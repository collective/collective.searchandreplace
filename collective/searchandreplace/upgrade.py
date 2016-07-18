from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger('collective.searchandreplace')
PROFILE_ID = 'profile-collective.searchandreplace:default'


def dummy_upgrade_step(context):
    return


def run_actions_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'actions')


def run_rolemap_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')


def run_registry_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def reindex_object_provides(context, portal_type=None):
    """Reindex the object_provides index.

    This is needed when more or less portal_types provide our interface.

    portal_type can be:

    - None (default): reindex the index for the whole site.

    - a string or a list of strings: get the brains of these
    portal_types, and reindex the index only for those objects.
    """
    catalog = getToolByName(context, 'portal_catalog')
    index = 'object_provides'
    if portal_type is None:
        logger.info('Reindexing %s in whole site.', index)
        catalog.manage_reindexIndex(ids=[index])
        return
    brains = catalog.unrestrictedSearchResults(portal_type=portal_type)
    logger.info('Reindexing %s for %d items of these portal_types: %r.',
                index, len(brains), portal_type)
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=[index])
