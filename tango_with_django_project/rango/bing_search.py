import json
import urllib


def read_bing_key():
    bing_api_key = None
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key file not found')
    return bing_api_key


def run_query(search_terms):
    bing_api_key = read_bing_key()

    if not bing_api_key:
        raise KeyError('BING Key Not Found')

    root_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    service = 'Web'
    results_per_page = 10
    offset = 0
    query = "'{0}'".format(search_terms)
    query = urllib.parse.quote(query)
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        service,
        results_per_page,
        offset,
        query)
    username = ''
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)
    results = []
    try:
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(search_url).read()
        response = response.decode('utf-8')
        json_response = json.load(response)
        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': result['Url'],
                            'summary': result['Description']})
    except:
        print("Error when querying the BING API")

    return results


def main():
    print("Enter a query ")
    query = input()
    results = run_query(query)
    for result in results:
        print(result['title'])
        print('-' * len(result['title']))
        print(result['summary'])
        print(result['link'])
        print()


if __name__ == '__main__':
    main()
