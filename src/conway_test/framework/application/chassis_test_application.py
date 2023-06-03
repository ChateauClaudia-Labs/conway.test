
from conway.application.application                                import Application

from vulnerability_management.observability.vm_logger                           import VM_Logger

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

        logger                                          = VM_Logger(activation_level=VM_Logger.LEVEL_INFO)
          
        super().__init__(logger)

