with open('resources/targets_without_istam.txt', 'rt') as logfile:
    for line in logfile:
        deployment = line.strip()
        print(
            f'METASTORE_TYPE=PROD VAULT_TYPE=PROD SCRIPT_PATH=jun5_deployment/v5.sql DEPLOYMENT={deployment} SECRETS_PROVIDER=VAULT java -jar snowhouse-accountUsageViewGenerator-jar-with-dependencies.jar')

