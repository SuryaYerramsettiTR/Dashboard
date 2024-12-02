from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import os
from concurrent.futures import ThreadPoolExecutor
import base64
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=["GET"])

GITHUB_TOKEN = ''
REPOSITORIES = [
  'tr/a200206_dete-app-ui-angular',
  'tr/a200206_dete-app-ui-authorities',
  'tr/a200206_dete-app-ui-advanced-config',
  'tr/a200206_dete-app-ui-modelscenarios',
  'tr/a200206_dete-lib-ui-common',
  'tr/a200206_dete-app-ui-ref-data',
  'tr/a200206_dete-app-ui-basic-config',
  'tr/a200206_dete-app-ui-oil-gas',
  'tr/a202750_ocmc-app-ui-cmc',
  'tr/a207963_ovat-app-ui',
  'tr/a202750_ocmc-app-ui-cmp',
  'tr/a200206_dete-app-ui-launcher',
  'tr/saffron_design_system'
]

TARGET_BRANCHES = ['develop', 'develop3', 'release/2025.1']

def fetch_data_from_github(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_github_data():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    data = []
    two_months_ago = datetime.now() - timedelta(days=60)

    def process_repo(repo):
        repo_data = {
            'repo': repo,
            'open_prs': [],
            'recently_closed_prs': [],
            'builds': [],
            'version_info': {}
        }

        # Fetch data concurrently
        with ThreadPoolExecutor() as executor:
            pr_future = executor.submit(fetch_data_from_github, f'https://api.github.com/repos/{repo}/pulls?state=all', headers)
            build_future = executor.submit(fetch_data_from_github, f'https://api.github.com/repos/{repo}/actions/runs', headers)
            commits_future = executor.submit(fetch_data_from_github, f'https://api.github.com/repos/{repo}/commits', headers)

            pr_data = pr_future.result()
            build_data = build_future.result()
            commits_data = commits_future.result()

        if not all([pr_data, build_data, commits_data]):
            print(f"Error fetching data for repo: {repo}")
            return repo_data

        # Filter builds for the specified branches
        filtered_builds = [
            build for build in build_data.get('workflow_runs', [])
            if build.get('head_branch') in TARGET_BRANCHES
        ]

        # Filter PRs
        open_prs = [
            pr for pr in pr_data if pr['state'] == 'open' and datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ') > two_months_ago
        ]
        closed_prs = [
            pr for pr in pr_data if pr['state'] == 'closed'
        ]
        closed_prs_sorted = sorted(closed_prs, key=lambda pr: pr['closed_at'], reverse=True)[:2]

        # Get assignee and reviewer names
        for pr in open_prs + closed_prs_sorted:
            assignee = pr.get('assignee')
            assignee_name = assignee.get('login') if assignee else None
            reviews_url = pr.get('url') + '/reviews'
            reviews_response = requests.get(reviews_url, headers=headers)
            if reviews_response.status_code == 200:
                reviews_data = reviews_response.json()
                reviewers = list(set([review['user']['login'] for review in reviews_data]))
            else:
                reviewers = []
            pr['assignee_name'] = assignee_name
            pr['reviewer_names'] = reviewers

        # Filter commits for the release branch
        release_commits = [
            commit for commit in commits_data
            if any(branch in commit.get('commit').get('message', '').lower() for branch in ['release'])
        ]

        # Merge release commits into builds
        for commit in release_commits:
            commit_id = commit.get('sha')
            branch_name = 'release'
            build_entry = {
                'type': 'Commit',
                'display_title': commit['commit']['message'],
                'timestamp': commit['commit']['author']['date'],
                'conclusion': 'success',
                'status': 'completed',
                'head_commit': {'author': {'name': commit['commit']['author']['name']}},
                'html_url': commit['html_url'],
                'head_sha': commit_id,
                'head_branch': branch_name
            }
            filtered_builds.append(build_entry)

        repo_data['open_prs'] = open_prs
        repo_data['recently_closed_prs'] = closed_prs_sorted
        repo_data['builds'] = filtered_builds

        # Fetch version information from common lib
        version_info = {}
        for branch in TARGET_BRANCHES:
            package_url = f'https://api.github.com/repos/{repo}/contents/package.json?ref={branch}'
            package_response = requests.get(package_url, headers=headers)
            if package_response.status_code == 200:
                package_data = package_response.json()
                if package_data and 'content' in package_data:
                    package_content = base64.b64decode(package_data['content']).decode('utf-8')
                    package_json = json.loads(package_content)
                    dependencies = package_json.get('dependencies', {})
                    version_info[branch] = {
                        "@a200206ui/det-common": dependencies.get("@a200206ui/det-common", "N/A"),
                        "@grapecity/wijmo": dependencies.get("@grapecity/wijmo", "N/A"),
                        "@saffron/core-components": dependencies.get("@saffron/core-components", "N/A")
                    }

        repo_data['version_info'] = version_info
        return repo_data

    # Use a ThreadPoolExecutor to process repositories concurrently
    with ThreadPoolExecutor() as executor:
        data = list(executor.map(process_repo, REPOSITORIES))

    return data

@app.route('/api/data')
def get_data():
    data = fetch_github_data()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
