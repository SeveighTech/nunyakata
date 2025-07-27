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
    """Get the GitHub project ID"""
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


def find_issue_by_title(title_pattern):
    """Find an issue by its title (supports partial matching)"""
    url = f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100"
    res = requests.get(url, headers=headers)
    issues = res.json()

    for issue in issues:
        if (
            "pull_request" not in issue
            and title_pattern.lower() in issue["title"].lower()
        ):
            return issue
    return None


def update_issue(issue_number, title=None, body=None, labels=None, state=None):
    """Update an existing GitHub issue"""
    payload = {}
    if title:
        payload["title"] = title
    if body:
        payload["body"] = body
    if labels:
        payload["labels"] = labels
    if state:
        payload["state"] = state

    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    res = requests.patch(url, headers=headers, json=payload)
    return res.json()


def create_issue_body(integration):
    """Create the standardized issue body"""
    api_status = "✅ Available" if integration["api_available"] else "❌ Not Available"
    doc_url = integration.get("api_documentation_url", "")
    labels_str = ", ".join(integration.get("labels", []))

    return f"""## Integration Request: {integration['name']}

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


def update_integration_issue(integration_name, updates):
    """
    Update an integration issue based on changes to the YAML

    Args:
        integration_name: Name of the integration (e.g., "Kowri")
        updates: Dict of updates made to the integration
    """
    # Find the issue
    issue_title = f"Integration: {integration_name}"
    issue = find_issue_by_title(integration_name)

    if not issue:
        print(f"❌ No issue found for {integration_name}")
        return None

    print(f"🔍 Found issue #{issue['number']}: {issue['title']}")

    # Load current integration data
    with open("integrations.yaml") as f:
        integrations = yaml.safe_load(f)

    # Find the integration
    integration = None
    for integ in integrations:
        if integ["name"] == integration_name:
            integration = integ
            break

    if not integration:
        print(f"❌ Integration {integration_name} not found in YAML")
        return None

    # Generate new issue body
    new_body = create_issue_body(integration)

    # Update labels
    issue_labels = integration.get("labels", []).copy()
    issue_labels.append("integration")
    if integration["api_available"]:
        issue_labels.append("api-available")
        if "no-api" in issue_labels:
            issue_labels.remove("no-api")
    else:
        issue_labels.append("no-api")
        if "api-available" in issue_labels:
            issue_labels.remove("api-available")

    if integration.get("status") == "completed":
        issue_labels.append("completed")

    # Update the issue
    updated_issue = update_issue(
        issue["number"], title=issue_title, body=new_body, labels=issue_labels
    )

    print(f"✅ Updated issue #{issue['number']}")

    # Add comment about the update
    comment_body = """## 🔄 Integration Updated

The following changes were made to this integration:

"""
    for key, value in updates.items():
        comment_body += f"- **{key.replace('_', ' ').title()}:** {value}\n"

    comment_body += f"\n_Updated on {requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC').json()['datetime'][:10]}_"

    # Post comment
    comment_url = (
        f"https://api.github.com/repos/{repo}/issues/{issue['number']}/comments"
    )
    requests.post(comment_url, headers=headers, json={"body": comment_body})

    return updated_issue


def bulk_update_from_yaml():
    """Update all issues based on current YAML state"""
    with open("integrations.yaml") as f:
        integrations = yaml.safe_load(f)

    updated_count = 0
    for integration in integrations:
        issue = find_issue_by_title(integration["name"])
        if issue:
            # Update issue with current YAML data
            new_body = create_issue_body(integration)
            issue_labels = integration.get("labels", []).copy()
            issue_labels.append("integration")
            if integration["api_available"]:
                issue_labels.append("api-available")
            else:
                issue_labels.append("no-api")

            if integration.get("status") == "completed":
                issue_labels.append("completed")

            update_issue(issue["number"], body=new_body, labels=issue_labels)
            updated_count += 1
            print(f"✅ Updated {integration['name']}")

    print(f"\n🎉 Updated {updated_count} issues from YAML")


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print(
            """
Usage:
    python update_issues.py <command> [args]

Commands:
    update <integration_name> <key=value> [key=value] ...
        Update a specific integration and its issue
        Example: python update_issues.py update "Kowri" api_documentation_url="https://docs.kowri.com"
    
    bulk-update
        Update all issues from current YAML state
        Example: python update_issues.py bulk-update
    
    find <integration_name>
        Find an issue by integration name
        Example: python update_issues.py find "Kowri"
        """
        )
        return

    command = sys.argv[1]

    if command == "update" and len(sys.argv) >= 4:
        integration_name = sys.argv[2]
        updates = {}

        # Parse key=value pairs
        for arg in sys.argv[3:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                # Convert string booleans
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                updates[key] = value

        # Update YAML first
        with open("integrations.yaml") as f:
            integrations = yaml.safe_load(f)

        for integration in integrations:
            if integration["name"] == integration_name:
                for key, value in updates.items():
                    integration[key] = value
                break

        # Write back to YAML
        with open("integrations.yaml", "w") as f:
            yaml.safe_dump(integrations, f, default_flow_style=False, sort_keys=False)

        print(f"📝 Updated {integration_name} in YAML")

        # Update GitHub issue
        update_integration_issue(integration_name, updates)

    elif command == "bulk-update":
        bulk_update_from_yaml()

    elif command == "find" and len(sys.argv) >= 3:
        integration_name = sys.argv[2]
        issue = find_issue_by_title(integration_name)
        if issue:
            print(f"🔍 Found: #{issue['number']} - {issue['title']}")
            print(f"   URL: {issue['html_url']}")
            print(f"   State: {issue['state']}")
        else:
            print(f"❌ No issue found for {integration_name}")


if __name__ == "__main__":
    main()
