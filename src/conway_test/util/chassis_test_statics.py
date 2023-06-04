
class Chassis_TestStatics():

    def __init__(self):
        '''
        Class of "enums", i.e., static string-value variables used throughout the conway_test module
        as a way to use consistent strings when they reference a named domain structural element.
        '''

    CHASSIS_SCENARIOS_REPO                          = "CHASSIS_SCENARIOS_REPO"  
    '''
    Denotes an environment variable that points to the root folder under which all the test scenarios reside
    for the :class:`conway_test`, i.e., the root folder for the ``conway_scenarios`` repo.

    This is a root directory that then breaks into sub-folders by ``scenario_id``, each of which is a test database for
    the scenario denoted by that ``scenario_id``.
    ''' 

    # When testing the repo administrator, we need to simulate root folders for the local and remote collection
    # of repos
    #
    BUNDLED_REPOS_LOCAL_FOLDER                      = "bundled_repos_local"
    BUNDLED_REPOS_REMOTE_FOLDER                     = "bundled_repos_remote"


