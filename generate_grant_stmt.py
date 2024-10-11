with open('resources/grants_to_finance.txt', 'rt') as grantfile:
    for line in grantfile:
        if not line.startswith('PRIVILEGE'):  # ignore the first line
            privilege, granted_on, granted_to, grantee_name = line.split()
            print(
                f'grant {privilege} on {granted_on} finance.metering_usage.WA_METRICS_SNOWSERVICES_COMPUTE_USAGE_RAW_V to {granted_to} {grantee_name};')

print('----------------------PREPROD8---------------------------------------------------------------------------------')
with open('resources/grants_preprod8.txt', 'rt') as grantfile:
    for line in grantfile:
        if not line.startswith('created_on'):  # ignore the first line
            _, privilege, granted_on, _, granted_to, grantee_name, _, _ = line.split()
            print(
                f'grant {privilege} on {granted_on} finance.metering_usage.WA_METRICS_SNOWSERVICES_COMPUTE_USAGE_RAW_V to {granted_to} {grantee_name};')
