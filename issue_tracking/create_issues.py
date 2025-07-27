import os
import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")  # e.g. "seveightech/nunyakata"
org = os.getenv("ORG")  # e.g. "SeveighTech"
project_number_str = os.getenv("PROJECT_NUMBER")
if project_number_str is None:
    raise ValueError("PROJECT_NUMBER environment variable is not set.")
project_number = int(project_number_str)
headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def get_project_id():
    query = """
    query ($org: String!, $number: Int!) {
      organization(login: $org) {
        projectV2(number: $number) {
          id
        }
      }
    }
    """
    variables = {"org": org, "number": project_number}
    res = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": variables},
    )
    return res.json()["data"]["organization"]["projectV2"]["id"]


def get_existing_issue_titles():
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"
        res = requests.get(url, headers=headers)
        batch = res.json()
        if not batch:
            break
        issues += batch
        page += 1
    return {issue["title"] for issue in issues if "pull_request" not in issue}


def create_issue(title, body, labels):
    payload = {"title": title, "body": body, "labels": labels}
    res = requests.post(
        f"https://api.github.com/repos/{repo}/issues", headers=headers, json=payload
    )
    return res.json()["node_id"]


def add_to_project(project_id, content_id):
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    variables = {"projectId": project_id, "contentId": content_id}
    requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": mutation, "variables": variables},
    )


def main():
    with open("integrations.yaml") as f:
        integrations = yaml.safe_load(f)

    project_id = get_project_id()
    existing_titles = get_existing_issue_titles()

    for integration in integrations:
        title = f"Integration: {integration['name']}"
        if title in existing_titles:
            print(f"Issue already exists: {title}")
            continue

        # Create issue body with integration details
        api_status = (
            "✅ Available" if integration["api_available"] else "❌ Not Available"
        )
        doc_url = integration.get("api_documentation_url", "")
        labels_str = ", ".join(integration.get("labels", []))

        body = f"""## Integration Request: {integration['name']}

**API Status:** {api_status}
**Labels:** {labels_str}
**Documentation URL:** {doc_url if doc_url else "Not provided"}

### Description
This issue tracks the integration of {integration['name']} into the nunyakata package.

### Tasks
- [ ] Research API documentation and endpoints
- [ ] Implement API client class
- [ ] Add authentication handling
- [ ] Write comprehensive tests
- [ ] Update documentation and examples
- [ ] Add to main package exports

### API Information
- **Available:** {'Yes' if integration['api_available'] else 'No'}
- **Documentation:** {doc_url if doc_url else 'Not available'}
- **Status:** {'Completed' if integration.get('status') == 'completed' else 'Pending'}

### Priority
{'High' if integration['api_available'] else 'Low'} - {'APIs available for integration' if integration['api_available'] else 'No public API available'}
"""

        # Use labels from the integration + add status labels
        issue_labels = integration.get("labels", []).copy()
        issue_labels.append("integration")
        if integration["api_available"]:
            issue_labels.append("api-available")
        else:
            issue_labels.append("no-api")

        if integration.get("status") == "completed":
            issue_labels.append("completed")

        node_id = create_issue(title, body, issue_labels)
        add_to_project(project_id, node_id)
        print(f"Created and linked issue: {title}")


if __name__ == "__main__":
    main()
