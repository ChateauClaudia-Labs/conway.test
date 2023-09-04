import os as _os

from conway_acceptance.test_logic.acceptance_test_context                          import AcceptanceTestContext
from conway_acceptance.util.scenarios_config                                       import ScenariosConfig

from conway_test.framework.scenario_foundry.operator_scenario_manifest import OperatorScenarioManifest
from conway_test.framework.test_database.operator_test_database        import Operator_TestDatabase
from conway_test.util.chassis_test_statics                             import Chassis_TestStatics


class Chassis_TestContext(AcceptanceTestContext):

    def __init__(self, test_case_name, notes, 
                 seeding_round                  = 0):
        '''
        This class is a Python context manager intended to be invoked by each test method of any of the test classes in
        the a Conway's application test module.

        @param test_case_name A string, representing the "name" of the test case using this context. It should match
                exactly what appears in the Conway application's ScenariosIds.yaml file. Such file is typically located
                via an environment variable setting such as $'CHASSIS_SCENARIOS_REPO for Conway framework's test cases,
                or a Conway-application-specific environment variable (for example, $VULNERABILITY_MANAGEMENT_SCENARIOS_REPO/ScenariosIds.yaml 
                for a hypotethical Conway application called "VulnerabilityManagement").

        @param notes A AcceptanceTestNotes object, that should be the data structure in which the test case can record
                observations in the course of its execution under this context. When the context exits these notes
                will be saved to the sceneario folder, under the subfolder given by the static variable
                TestStatics.RUN_NOTES

        @param seeding_round An int, designating the round fo seeding for which we seek the path.
                By default it is 0, meaning that the test datbase should be seeded from conteint in a folder called "SEED@T0". 
                For some test cases that is the only seeding event in the lifecycle of the test, but other test cases require 
                multiple phases where at each phase we need to simulate that the user has changed or added additional
                content to the database. In that case, the test harness pattern calls for multiple seeding events each of
                which will enrich the database at different times from data in different folders. For example,
                a folder "SEED@T0" would be used for an initial seeding at the start of the test,
                then "SEED@T1" for content that must be used to enrich the database in a subsequent phase 1, then
                "SEED@T2" for a subsequent phase 2, etc. Each seeding event should use a different AcceptanceTestContext
                object

        '''
        scenarios_repo                                  = self._scenarios_repo()
        scenario_id                                     = ScenariosConfig(scenarios_repo).get_scenario_id(test_case_name)
        manifest                                        = OperatorScenarioManifest(scenarios_repo, scenario_id)

        super().__init__(scenario_id, manifest, notes, seeding_round)

    def _scenarios_repo(self):
        '''
        '''
        scenarios_repo                                  = _os.environ.get(Chassis_TestStatics.CHASSIS_SCENARIOS_REPO)
        if scenarios_repo == None:
            raise ValueError("Environment variable '" + Chassis_TestStatics.CHASSIS_SCENARIOS_REPO + "' is not set." 
                              + "\nIt should point to the location where you deployed the 'conway_scenarios' repo" )
        
        return scenarios_repo

    def initialize_database(self):
        '''
        Constructs an instance of a TestDatabase concrete class and sets it as the value of self.test_database

        @param spec A ScenarioSpec object used to create the TestDatabase object created by this method.
        '''
        self.test_database                              = Operator_TestDatabase(self.manifest)

    def __enter__(self):
        '''
        Creates and returns a TestDatabase object. Intention is that this context manager is used by a specific
        test case method to surround the business logic it runs, and that business logic should be run against
        the TestDatabase returned by this method.
        '''
        super().__enter__()

        return self
    
