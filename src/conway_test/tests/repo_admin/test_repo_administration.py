import sys                                                                          as _sys

from conway_acceptance.test_logic.acceptance_test_case                              import AcceptanceTestCase
from conway_acceptance.test_logic.acceptance_test_notes                             import AcceptanceTestNotes

from conway_ops.repo_admin.repo_administration                                      import RepoAdministration, GitUsage
from conway_ops.scaffolding.scaffold_spec                                           import ScaffoldSpec
from conway_ops.scaffolding.scaffolding_statics                                     import ScaffoldingStatics

from conway_test.framework.test_logic.chassis_test_context                          import Chassis_TestContext
from conway_test.framework.test_logic.chassis_excels_to_compare                     import Chassis_ExcelsToCompare

class TestRepoAdministration(AcceptanceTestCase):


    def test_create_project(self):
        '''
        Checks that the :class:`RepoAdministration` correctly creates a set of GIT repos for a standard
        project based on the :class:`conway`, without scaffolding code.

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

    def test_scaffold_101(self):
        '''
        Checks that the :class:`RepoAdministration` correctly creates a set of GIT repos for a standard
        project based on the :class:`conway`, using scaffolding templates with id 101.

        '''
        MY_NAME                                         = "repo_admin.scaffold_101"

        TEST_PROJECT                                    = "cash"

        SS                                              = ScaffoldingStatics
        params_dict                                     = {SS.APP_CODE_PARAM:                   TEST_PROJECT, 
                                                            SS.APP_NAME_PARAM:                  "CashManagement", 
                                                            SS.APP_NAME_UPPER_PARAM:            "CASH_MANAGEMENT",
                                                            SS.APP_ABBREVIATION_UPPER_PARAM:    "CM",
                                                            SS.APP_ABBREVIATION_LOWER_PARAM:    "cm",
                                                            SS.APP_MODULE_PARAM:                "cash_management",
                                                            
                                                            SS.AUTHOR_PARAM:                    "test_scaffold_101",
                                                            SS.AUTHOR_EMAIL_PARAM:              "NA",
                                                            SS.PROJECT_DESCRIPTION_PARAM:       "Sample application used to test scaffolding funtionality of Conway",
                                                            }
        variables_dict                                  = {SS.PARAMS:               params_dict}
        scaffold_spec                                   = ScaffoldSpec(f"{ScaffoldSpec.standard_templates_location()}/101", 
                                                                       variables_dict)

        notes                                           = AcceptanceTestNotes("database_structure", self.run_timestamp)

        excels_to_compare                               = Chassis_ExcelsToCompare()
        excels_to_compare.addXL_RepoStats(TEST_PROJECT)

        git_usage                                       = GitUsage.git_local_only # no_git_usage

        with Chassis_TestContext(MY_NAME, notes=notes) as ctx:

            local_repos_root                            = ctx.test_database.local_repos_hub.hub_root()
            remote_repos_root                           = ctx.test_database.remote_repos_hub.hub_root()

            # Enrich the variables used in template generation with ctx-dependent information
            params_dict[SS.PROJECT_ROOT_PARAM]          = f"{local_repos_root}"

            admin                                       = RepoAdministration(local_root         = local_repos_root, 
                                                                             remote_root        = remote_repos_root, 
                                                                             repo_bundle        = None)
            repo_bundle                                 = admin.create_project(project_name     = TEST_PROJECT,
                                                                               work_branch_name = "bar-dev",
                                                                               scaffold_spec    = scaffold_spec,
                                                                               git_usage        = git_usage) 

            admin.repo_bundle                           = repo_bundle

            admin.create_repo_report(publications_folder=ctx.manifest.path_to_actuals(), git_usage = git_usage, mask_nondeterministic_data=True)

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
        elif what_to_do == "scaffold_101":
            T.test_scaffold_101()

    main(_sys.argv)