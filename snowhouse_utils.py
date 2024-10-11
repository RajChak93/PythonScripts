def read_deployments_list():
    """
    Read deployment list from snowhouse_metadata.config.deployment_target_pairs
    select distinct(deployment_name) from snowhouse_metadata.config.deployment_target_pairs;
    :return: list of values
    """
    ret_list = []
    with open('resources/deployment_names.txt', 'rt') as logfile:
        for line in logfile:
            deployment = line.strip().replace('-', '_')
            ret_list.append(deployment)
    return ret_list


def read_line_by_line(filename):
    """
    Read a file line-by-line and return as list
    :return: list of values
    """
    ret_list = []
    with open(filename, 'rt') as logfile:
        for line in logfile:
            ret_list.append(line.strip())
    return ret_list


def success_in_n_trials(n):
    if (n <= 0):
        raise Exception('false')
    prob = 0.1
    # 1 trial : 0.1
    # 2 trials : 0.9 * 0.1
    # 3 trials : 0.9 * 0.9 * 0.1
    for i in range(1, n):
        prob = 0.9 * prob
    return prob


def print_n_trials(n):
    for i in range(1, n + 1):
        val = success_in_n_trials(i) * 100
        print(f'Getting lottery picked up is {val} percent')


def read_org_data_schema_for_snowhouse_proc_task(deployment_config, args):
    """
    If the file being run is snowhouse_proc_task, then validate the connection host config
    and write the value of org_data_schema in args (which is used by deployment script).
    :param deployment_config: connection config for connecting to snowhouse (either preprod8 or prod1)
    :param args: arguments passed to deploy.py
    :return: throws Assertion Error in case of any invalid configs, else sets the org_data_schema in args
    """
    connection_host = deployment_config["host"].lower()
    is_preprod8_connection = connection_host.find("snowhouse.preprod8.us-west-2.aws.snowflakecomputing.com") != -1
    is_prod1_connection = connection_host.find("snowhouse.snowflakecomputing.com") != -1
    assert is_prod1_connection or is_preprod8_connection, f'snowhouse_proc_task deployment can only be for prod1 snowhouse or preprod8 snowhouse'
    args.org_data_schema = 'prod' if is_prod1_connection else 'preprod'
    return


def validate_org_usage_deployment_params(deployment_config, args):
    """
    If the file being run is snowhouse_proc_task, then validate the org_data_schema and connection host config
    :param deployment_config: connection config for connecting to snowhouse (either preprod8 or prod1)
    :param args: arguments passed to deploy.py
    :return: throws Assertion Error in case of any invalid configs
    """
    connection_host = deployment_config["host"].lower()
    is_preprod8_connection = connection_host.find("snowhouse.preprod8.us-west-2.aws.snowflakecomputing.com") != -1
    is_prod1_connection = connection_host.find("snowhouse.snowflakecomputing.com") != -1
    org_data_schema = args.org_data_schema.lower()
    # While running snowhouse_proc_task, only "preprod" or "prod" are valid values for org_data_schema
    assert org_data_schema in ['preprod',
                               'prod'], f'org_data_schema {org_data_schema} invalid, must be preprod or prod for snowhouse_proc_task'
    # if org_data_schema is preprod then host connection must be preprod8 snowhouse, similarly for prod
    assert (is_prod1_connection and org_data_schema == 'prod') or (
            is_preprod8_connection and org_data_schema == 'preprod'), f'Unmatched host and org_data_schema values'
    return


def generate_commands_org_usage():
    table_names = list(
        filter(lambda name: name.startswith('--') is False, read_line_by_line('resources/org_usage_tables.txt')))
    for table_name in table_names:
        print(f"select '{table_name}' as tbl,count(*) as cnt from (select distinct(deployment_id) from {table_name})")
        print('union')


def generate_commands_org_usage2():
    table_names = list(
        filter(lambda name: name.startswith('--') is False, read_line_by_line('resources/org_usage_tables.txt')))
    for table_name in table_names:
        print(f"select deployment_id from {table_name}")
        print('inner join')


def generate_unionall_command_for_viewdef():
    """
    Return a command like
    select name, viewdef ilike '%cachedPlanId%', viewdef, dpo from
    (
    SELECT dpo:"name" as name,dpo:"viewDefinition" as viewdef, dpo
    FROM snowhouse_import.prod1.SNOWHOUSE_VIEW_TYPE_ETL
    where name ilike 'job_raw_v'
    union all
    SELECT dpo:"name" as name,dpo:"viewDefinition" as viewdef, dpo
    FROM snowhouse_import.au.SNOWHOUSE_VIEW_TYPE_ETL
    where name ilike 'job_raw_v'
    ...
    );
    unioned over all deployments
    :return: final SQL command to run
    """
    deployment_names = read_deployments_list()
    deployment_commands = []
    for deployment_name in deployment_names:
        command = f'SELECT \'{deployment_name}\' as deployment_name, dpo:"name" as name,dpo:"viewDefinition" as viewdef, dpo  FROM snowhouse_import.{deployment_name}.SNOWHOUSE_VIEW_TYPE_ETL where name ilike \'job_raw_v\''
        deployment_commands.append(command)
    separator = ' union all \n'
    unionall_command = separator.join(deployment_commands)
    return f'select deployment_name, name, viewdef ilike \'%cachedPlanId%\', viewdef, dpo from(\n{unionall_command}\n);'


def generate_masking_commands(cmd_list):
    """
    Given commands
    """
    deployment_names = read_deployments_list()
    for deployment_name in deployment_names:
        for command in cmd_list:
            replaced = command.replace('&deployment', deployment_name)
            print(replaced)


def generate_unionall_command_for_replication_databases():
    """
    Return a command like
    select 'SFCOGSOPS.'||alias||'.SNOWFLAKE_SYSTEM_SHARE_STATUS_AU'
    from snowhouse_import.au.account_etl_v
    where name ilike 'snowhouse_local'
    unioned over all deployments
    :return: final SQL command to run
    """
    deployment_names = read_deployments_list()
    deployment_commands = []
    for deployment_name in deployment_names:
        bg_db = f'SNOWFLAKE_SYSTEM_SHARE_STATUS_{deployment_name}'
        command = f'''
        select \'create database if not exists {bg_db} as replica of SFCOGSOPS.\'||alias||\'.{bg_db};\' 
        from snowhouse_import.{deployment_name}.account_etl_v
        where name ilike \'snowhouse_local\'
        '''
        deployment_commands.append(command)
    separator = ' union all \n'
    unionall_command = separator.join(deployment_commands)
    return unionall_command


def generate_whitelist_cmd():
    whitelisted_files = ['.*snowhouse_local.snowhouse_import.cortex.*',
                         '.*snowhouse_local.snowhouse_import.cognitive_services.*',
                         '.*snowhouse_local.snowhouse_import.ml.*',
                         '.*snowhouse_local.snowhouse_import.db_roles.ml_user.sql',
                         '.*snowhouse_local.snowhouse_import.db_roles.document_intelligence_creator.sql',
                         '.*snowhouse_local.snowhouse_import.db_roles.cognitive_services_user.sql']
    comma_sep_files = ",".join(whitelisted_files)
    whitelist_cmd = f"alter system set SNOWFLAKE_SHARE_TASKDEF_FILENAME_ALLOW_REGEX_LIST='{comma_sep_files}'"
    expected_val = "alter system set SNOWFLAKE_SHARE_TASKDEF_FILENAME_ALLOW_REGEX_LIST='.*snowhouse_local.snowhouse_import.cortex.*,.*snowhouse_local.snowhouse_import.cognitive_services.*,.*snowhouse_local.snowhouse_import.ml.*,.*snowhouse_local.snowhouse_import.db_roles.ml_user.sql,.*snowhouse_local.snowhouse_import.db_roles.document_intelligence_creator.sql,.*snowhouse_local.snowhouse_import.db_roles.cognitive_services_user.sql'"
    assert (whitelist_cmd == expected_val)

