import requests
import argparse

def fetch_zenodo_dois(zenodo_token):
    """
    Fetch the list of DOIs from Zenodo
    """
    page = 1
    params = {
        "access_token": zenodo_token,
        "status": "published",
        "page": 1,
        "size": 100,
    }
    url = "https://sandbox.zenodo.org/api/deposit/depositions"
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch DOIs: {response.status_code} {response.text}")
    dois = response.json()

    while 'next' in response.links:
        page += 1
        params = {
            "access_token": zenodo_token,
            "status": "published",
            "page": page,
            "size": 100,
        }
        # print(f"Fetching next page of packages from Github", response.links['next']['url'], params, page)
        response=requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch DOIs: {response.status_code} {response.text}")
        # print(f"Fetched {len(response.json())} packages from Github", response.json())
        dois.extend(response.json())

    doi_list = []
    for doi in dois:
        doi_list.append(doi['title'])
    return doi_list

def update_readme(packages):
    with open("./dois.txt", "w") as file:
        for i in range(len(packages)):
            new_content = packages[i] + "\n"
            file.write(new_content)
            file.truncate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Get Published DOIs from Zenodo",
    )
    parser.add_argument("--zenodo_token", type=str, required=True, help="Zenodo token")
    args = parser.parse_args()

    print(fetch_zenodo_dois(args.zenodo_token))
    # update_readme(fetch_zenodo_dois(args.zenodo_token))