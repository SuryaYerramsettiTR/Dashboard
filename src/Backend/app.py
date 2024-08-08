from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=["GET"])

GITHUB_TOKEN = '********
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
    'tr/a202750_ocmc-app-ui-cmc'
]

TARGET_BRANCHES = ['develop', 'develop3', 'release/2024.5']

def fetch_github_data():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    data = []
    two_months_ago = datetime.now() - timedelta(days=60)

    for repo in REPOSITORIES:
        pr_url = f'https://api.github.com/repos/{repo}/pulls?state=all'
        build_status_url = f'https://api.github.com/repos/{repo}/actions/runs'

        pr_response = requests.get(pr_url, headers=headers)
        build_response = requests.get(build_status_url, headers=headers)

        if pr_response.status_code != 200 or build_response.status_code != 200:
            print(f"Error fetching data for repo: {repo}")
            continue  # Skip to the next repository if there's an error

        pr_data = pr_response.json()
        build_data = build_response.json()

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

        repo_data = {
            'repo': repo,
            'open_prs': open_prs,
            'recently_closed_prs': closed_prs_sorted,
            'builds': filtered_builds
        }
        data.append(repo_data)
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
