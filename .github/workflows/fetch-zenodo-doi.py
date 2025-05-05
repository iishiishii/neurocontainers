import requests

ACCESS_TOKEN = "zlW6jLclQls3Zkqwch9JXIkOluBhbbddMcdHeq88IktVJgu4Q3sxdmoS2bVK"
params = {
    "access_token": ACCESS_TOKEN,
    "status": "published",
    "page": 1,
    "size": 100,
}
response = requests.get('https://sandbox.zenodo.org/api/deposit/depositions',
                        params=params)
print(len(response.json()))

with open("./doi.txt", "w") as file:
    for i in range(len(response.json())):
        # print(packages[i])
        new_content = response.json()[i]['title'] + "\n"
        file.write(new_content)
        file.truncate()