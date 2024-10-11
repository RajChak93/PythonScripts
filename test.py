files_run_dict = {}
native_app_files_to_be_run = ["snowflake_na_local_state_artifacts_deploy.sql", "na_snowhouse_local_validation.sql",
                              "snowhouse_local_app_package_deploy.sql"]

for expected_file in native_app_files_to_be_run:
    assert expected_file in files_run_dict and files_run_dict[
        files_run_dict] == 'True', f"{expected_file} not run or failed"

share_object_files_to_be_run = ["snowhouse_local.snowhouse_import.stream_task.metering_history_task.sql",
                                "snowhouse_local.snowhouse_import.stream_task.warehouse_metering_history_task.sql",
                                "snowhouse_local.snowhouse_import.account_usage.views.metering_history.sql",
                                "snowhouse_local.snowhouse_import.core.schema_setup.sql",
                                "snowhouse_local.snowhouse_import.core.functions.budget.sql",
                                "snowhouse_local.snowhouse_import.installer.schema_setup.sql"]

for expected_file in share_object_files_to_be_run:
    assert expected_file in files_run_dict and files_run_dict[
        files_run_dict] == 'True', f"{expected_file} not run or failed"
