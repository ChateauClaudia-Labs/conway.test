import os                                                           as _os

from conway.application.application                                 import Application

from conway.observability.logger                                    import Logger

class Test_Logger(Logger):
    '''
    This is a mock logger, needed in order to run the tests of the :class:`conway_test`.

    Specifically, it is needed by the :class:`Chassis_Test_Application`. Please refer to its
    documentation as to why these mock classes are needed in order to run the tests.
    '''


class Chassis_Test_Application(Application):

    '''
    This is a mock application, which is needed in order to run the tests of the :class:`conway_test`.

    This is needed because the :class:`conway` requires that any business logic be run under
    the context of a global :class:`Application` object, which is normally the case for real applications, or 
    for tests of real applications.

    But for testing the :class:`conway` itself without a real application, the tests cases in 
    :class:`conway_test` wouldn't run unless there is (mock) Application as a global context.

    Hence this class, which is initialized in ``conway_test.__init__.py``
    '''
    def __init__(self):

        APP_NAME                        = "ChassisTestApp"
        logger                          = Test_Logger(activation_level=Logger.LEVEL_INFO)

        # __file__ is something like 
        #
        #   'C:\Alex\Code\conway\conway.test\src\conway_test\framework\application\chassis_test_application.py'
        #
        #
        # So to get the project folder ("conway") we need to go 6 directories up
        #
        directory                       = _os.path.dirname(__file__)

        for idx in range(6):
            directory                   = _os.path.dirname(directory)
        project_directory               = directory   
        config_path                     = project_directory + "/config"     
          
        super().__init__(app_name=APP_NAME, config_path=config_path, logger=logger)

