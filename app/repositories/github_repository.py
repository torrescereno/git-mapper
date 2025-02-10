import asyncio

import httpx

from app.core.config import settings


def should_exclude(path: str, item_type: str) -> bool:
    """
    Determina si un archivo o directorio debe ser excluido basado en su path y tipo.
    """

    for part in path.split("/"):
        if part in settings.EXCLUDED_DIRS:
            return True

    if item_type == "file":
        filename = path.split("/")[-1]
        if filename in settings.EXCLUDED_FILE_NAMES:
            return True
        for ext in settings.EXCLUDED_FILE_EXTENSIONS:
            if filename.lower().endswith(ext):
                return True

    return False


class GitHubRepository:
    def __init__(self):
        token = settings.github_token
        self.headers = {"Authorization": f"token {token}"} if token else {}
        self.base_url_template = "https://api.github.com/repos/{owner}/{repo}/contents"

    async def download_file(self, item: dict, client: httpx.AsyncClient) -> list:
        """
        Descarga el contenido de un archivo si no está excluido.
        """

        if should_exclude(item["path"], "file"):
            return []

        download_url = item.get("download_url")
        if download_url:
            response = await client.get(download_url, headers=self.headers)
            response.raise_for_status()
            content_str = response.text
            file_entry = {"file": item["path"], "content": content_str}
            return [file_entry]

        return []

    async def process_directory(
        self, base_url: str, api_path: str, client: httpx.AsyncClient
    ) -> list:
        """
        Procesa de forma recursiva un directorio del repositorio.
        Descarga archivos y se adentra en subdirectorios, respetando la exclusión.
        """

        directory_results = []
        current_url = f"{base_url}/{api_path}" if api_path else base_url

        while current_url:
            response = await client.get(current_url, headers=self.headers)
            response.raise_for_status()
            items = response.json()

            tasks = []
            for item in items:
                if "type" not in item or "path" not in item:
                    continue

                item_type = item["type"]
                item_path = item["path"]

                if should_exclude(item_path, item_type):
                    continue

                if item_type == "file":
                    tasks.append(self.download_file(item, client))
                elif item_type == "dir":
                    tasks.append(self.process_directory(base_url, item_path, client))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    directory_results.extend(result)

            link_header = response.headers.get("Link", "")
            current_url = None
            if 'rel="next"' in link_header:
                links = link_header.split(", ")
                for link in links:
                    if 'rel="next"' in link:
                        current_url = link[link.find("<") + 1 : link.find(">")]
                        break

        return directory_results

    async def get_repo_files(self, owner: str, repo: str) -> list:
        """
        Orquesta la descarga de archivos de un repositorio de GitHub.
        """

        base_url = self.base_url_template.format(owner=owner, repo=repo)
        async with httpx.AsyncClient() as client:
            results = await self.process_directory(base_url, "", client)
        return results
