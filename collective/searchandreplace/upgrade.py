PROFILE_ID = 'profile-collective.searchandreplace:default'


def dummy_upgrade_step(context):
    return


def run_actions_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'actions')


def run_rolemap_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')
