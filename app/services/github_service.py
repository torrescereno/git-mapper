from app.repositories.github_repository import GitHubRepository


class GitHubService:
    def __init__(self, repository: GitHubRepository = None):
        self.repository = repository or GitHubRepository()

    async def download_repo_files(self, owner: str, repo: str) -> list:
        """

        Lógica de negocio para obtener los archivos de un repositorio de GitHub.
        Aquí se pueden incluir validaciones o transformaciones adicionales.
        """
        return await self.repository.get_repo_files(owner, repo)


def get_github_service() -> GitHubService:
    return GitHubService()
