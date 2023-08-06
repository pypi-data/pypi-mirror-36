def get_cluster_id(turbot_host, turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, api_version):
    """ Gets the cluster id
    # TODO: put this in cluster.py
    """
    import requests
    import json
    import urllib.parse
    api_method = "GET"
    api_url = "/api/%s/cluster" % (api_version)

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)
    urn = responseObj['urn']

    return urn


def get_cluster_options(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version):
    """ Gets the current turbot vpc configuration for an account
    TODO: refactor this
    :return: Returns the current turbot VPC configuration
    """
    import requests
    import json
    import urllib.parse
    api_method = "GET"
    api_url = "/api/%s/cluster" % (api_version)
    vpc_list = []

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)
    for obj in responseObj['items']:
        vpc_list.append(obj['subnets'])

    return vpc_list


def get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version):
    """ Gets the current turbot account names

    :return: Returns a dict of turbot account names as turbot_id:AWSaccount
    """
    import requests
    import json
    import urllib.parse
    # Set to the required API request type and location
    accounts = {}
    api_method = "GET"
    api_url = "/api/%s/accounts" % (api_version)

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)

    if responseObj['items']:
        # A user may not have permission to list all accounts
        for obj in responseObj['items']:
            accounts[obj['id']] = obj['awsAccountId']

    return accounts


def get_aws_account_ids(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, api_version):
    import requests
    import json
    import urllib.parse
    """ Gets the current turbot account names

    :return: Returns a list of turbot account names as accounts
    """
    # Set to the required API request type and location
    accounts = []
    api_method = "GET"
    api_url = "/api/%s/accounts" % (api_version)

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)

    for obj in responseObj['items']:
        accounts.append(obj['awsAccountId'].zfill(12))

    return accounts


def get_account_titles(turbot_api_access_key, turbot_api_secret_key,turbot_host_certificate_verification, turbot_host, api_version):
    import requests
    import json
    import urllib.parse
    accounts = {}
    api_method = "GET"
    api_url = "/api/%s/accounts" % (api_version)

    response = requests.request(
        api_method,
        urllib.parse.urljoin(turbot_host, api_url),
        auth=(turbot_api_access_key, turbot_api_secret_key),
        verify=turbot_host_certificate_verification,
        headers={
            'content-type': "application/json",
            'cache-control': "no-cache"
        }
    )

    # Convert the response JSON into a Python object
    responseObj = json.loads(response.text)

    for obj in responseObj['items']:
        accounts[obj['id']] = obj['title']

    return accounts


def validate_account(turbot_api_access_key, turbot_api_secret_key, turbot_host_certificate_verification, turbot_host, account):
    """ Simply validates that we have a valid account id being passed in """

    from turbotutils.cluster import get_turbot_account_ids

    ids = get_turbot_account_ids(turbot_api_access_key, turbot_api_secret_key,
                                                     turbot_host_certificate_verification, turbot_host)
    idList = []
    for key in ids.items():
        idList.append(key[0])
    while True:
        if account not in idList:
            print('Sorry, account %s is not in this turbot cluster' % account)
            account=input('Please enter the account ID you are adding the user to: ')
            continue
        else:
            # We do have a valid account
            return(account)
