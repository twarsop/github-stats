import os
import requests

token = os.environ["token"]
headers = {'Authorization': 'token ' + token}
base_url = "https://api.github.com"

def get_user_repos(username):
    url = f"{base_url}/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repositories_data = response.json()
        return repositories_data
    else:
        return None

if __name__ == "__main__":    
    username = "twarsop" # github username
    user_repos = get_user_repos(username)
    if user_repos:
        for repo in user_repos:
            print(repo["name"])
            url = f"{base_url}/repos/{username}/{repo['name']}/commits"
            print(url)
            commits = requests.get(url, headers=headers)
            for commit in commits:
                print(commit)
                print()
                break
            print()
            break
    else:
        print(f"Failed to retrieve repositories.")