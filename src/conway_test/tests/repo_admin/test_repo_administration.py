import sys                                                                          as _sys
import pandas                                                                       as _pd
from pathlib                                                                        import Path

from conway_acceptance.test_logic.acceptance_test_case                             import AcceptanceTestCase
from conway_acceptance.test_logic.acceptance_test_notes                            import AcceptanceTestNotes

from conway_ops.repo_admin.repo_administration                         import RepoAdministration
from conway_ops.repo_admin.repo_statics                                import RepoStatics

from conway_test.framework.test_logic.chassis_test_context             import Chassis_TestContext
from conway_test.framework.test_logic.chassis_excels_to_compare        import Chassis_ExcelsToCompare

class TestRepoAdministration(AcceptanceTestCase):


    def test_create_project(self):
        '''
        Checks that the :class:`RepoAdministration` correctly scaffolds a set of GIT repos for a standard
        project based on the :class:`conway`.

        '''
        MY_NAME                                         = "repo_admin.create_project"

        TEST_PROJECT                                    = "foo_app"

        notes                                           = AcceptanceTestNotes("database_structure", self.run_timestamp)

        excels_to_compare                               = Chassis_ExcelsToCompare()
        excels_to_compare.addXL_RepoStats(TEST_PROJECT)

        with Chassis_TestContext(MY_NAME, notes=notes) as ctx:

            local_repos_root                            = ctx.test_database.local_repos_hub.hub_root()
            remote_repos_root                           = ctx.test_database.remote_repos_hub.hub_root()

            admin                                       = RepoAdministration(local_root     = local_repos_root, 
                                                                             remote_root    = remote_repos_root, 
                                                                             repo_bundle    = None)
            repo_bundle                                 = admin.create_project(project_name     = TEST_PROJECT,
                                                                               work_branch_name = "bar-dev") 

            admin.repo_bundle                           = repo_bundle

            admin.create_repo_report(publications_folder=ctx.manifest.path_to_actuals(), mask_nondeterministic_data=True)

            self.assert_database_structure(ctx, excels_to_compare)       

    def test_create_branch(self):
        '''
        Checks that the :class:`RepoAdministration` correctly creates a feature branch for all pertinent repos.

        '''
        MY_NAME                                         = "repo_admin.create_branch"

        TEST_PROJECT                                    = "foo_app"

        notes                                           = AcceptanceTestNotes("database_structure", self.run_timestamp)

        excels_to_compare                               = Chassis_ExcelsToCompare()
        excels_to_compare.addXL_RepoStats(TEST_PROJECT)

        with Chassis_TestContext(MY_NAME, notes=notes) as ctx:

            local_repos_root                            = ctx.test_database.local_repos_hub.hub_root()
            remote_repos_root                           = ctx.test_database.remote_repos_hub.hub_root()

            admin                                       = RepoAdministration(local_root     = local_repos_root, 
                                                                             remote_root    = remote_repos_root, 
                                                                             repo_bundle    = None)
            repo_bundle                                 = admin.create_branch(branch_name = "feature 1234") 

            admin.repo_bundle                           = repo_bundle

            admin.create_repo_report(publications_folder=ctx.manifest.path_to_actuals(), mask_nondeterministic_data=True)

            self.assert_database_structure(ctx, excels_to_compare)  

    def _get_files(self, root_folder):
        '''
        Overwrites parent to ignore files inside a ".git" folder, since GIT appears to use a non-deterministic
        way to hash objects

        @param root_folder A string representing the root of a folder structure
        '''
        all_files_l                                     = super()._get_files(root_folder)

        files_l                                         = [f for f in all_files_l if not ".git" in f.split("/")]

        return files_l

if __name__ == "__main__":
    # In the debugger, executes only if we have a configuration that takes arguments, and the string
    # corresponding to the test method of interest should be configured in that configuration
    def main(args):
        T                                               = TestRepoAdministration()
        T.setUp()
        what_to_do                                      = args[1]
        if what_to_do == "create_project":
            T.test_create_project()
        elif what_to_do == "create_branch":
            T.test_create_branch()

    main(_sys.argv)