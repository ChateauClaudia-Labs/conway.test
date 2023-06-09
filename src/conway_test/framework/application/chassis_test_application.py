
from conway.application.application                                import Application

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

        logger                                          = Test_Logger(activation_level=Logger.LEVEL_INFO)
          
        super().__init__(logger)

