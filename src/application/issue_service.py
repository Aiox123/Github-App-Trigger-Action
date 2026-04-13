from src.domain.github_app import GitHubAppDomain
from src.infrastructure.github_api_client import GitHubApiClient

class IssueService:
    def __init__(self):
        self.app_domain = GitHubAppDomain()
        self.api_client = GitHubApiClient()

    def create_issue(self, repo, title, body):
        jwt = self.app_domain.generate_jwt()
        token = self.api_client.get_installation_token(
            jwt,
            self.app_domain.installation_id
        )
        status = self.api_client.trigger_create_issue(token, repo, title, body)
        return status