import requests
import json
import argparse
import os

def fetch_package_tags(git_token, package_name):
    """
    https://api.github.com/orgs/NeuroDesk/packages/container/romeo_3.2.4/versions
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {git_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f"https://api.github.com/orgs/NeuroDesk/packages/container/{package_name}/versions"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch package tags: {response.status_code} {response.text}")
    tags = response.json()
    package_tag_list = []
    for tag in tags:
        # print(f"Tag {package_name}: {tag['metadata']['container']['tags']}")
        if len(tag['metadata']['container']['tags']) > 1:
            for i in range(len(tag['metadata']['container']['tags'])):
                if tag['metadata']['container']['tags'][i] == "latest":
                    continue
                else:
                    package_tag_list.append(package_name + "_" + tag['metadata']['container']['tags'][i])
        elif len(tag['metadata']['container']['tags']) == 1:
            package_tag_list.append(package_name + "_" + tag['metadata']['container']['tags'][0])
        else:
            continue
    return package_tag_list
    

def fetch_packages(git_token):
    """
    Fetch the list of packages from Github
    """
    page = 1
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {git_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        "package_type": "container",
        "per_page": 100,
        "page": page,
        "visibility": "public"
    }
    # print(f"Fetching packages from Github with token {params}")
    url = "https://api.github.com/orgs/NeuroDesk/packages"

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch packages: {response.status_code} {response.text}")
    packages = response.json()
    print(f"Fetched {len(packages)} packages from Github")

    while 'next' in response.links:
        page += 1
        params = {
            "package_type": "container",
            "per_page": 100,
            "page": page,
            "visibility": "public"
        }
        print(f"Fetching next page of packages from Github", response.links['next']['url'], params, page)
        response=requests.get(url,headers=headers, params=params)
        # print(f"Fetched {len(response.json())} packages from Github", response.json())
        packages.extend(response.json())

    # Split the package name and version
    app_list = []
    for package in packages:
        package_name = "%2F".join(package['name'].split("/"))
        package_tags = fetch_package_tags(git_token, package_name)
        app_list.extend(package_tags)
    print(f"Found {len(app_list)} packages")
    return app_list

def update_readme(packages):
    with open("./packages.txt", "w") as file:
        for i in range(len(packages)):
            # print(packages[i])
            new_content = packages[i] + "\n"
            file.write(new_content)
            file.truncate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="Upload container to Zenodo",
    )
    
    # parser.add_argument("--container_filepath", type=str, required=True, help="Container file to upload to Zenodo")
    # parser.add_argument("--container_name", type=str, required=True, help="Container name")
    parser.add_argument("--token", type=str, required=True, help="Zenodo token")
    
    args = parser.parse_args()

    doi_url = fetch_packages(args.token)
    # print(doi_url)
    update_readme(doi_url)