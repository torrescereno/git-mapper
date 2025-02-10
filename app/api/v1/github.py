from fastapi import APIRouter, Depends

from app.schemas.github import GitHubFilesResponse
from app.services.github_service import GitHubService, get_github_service

router = APIRouter()


@router.get(
    "/files",
    summary="Obtiene el contenido de un repositorio de GitHub",
    description="Descarga de forma asíncrona los archivos relevantes de un repositorio, excluyendo los que no son necesarios para el análisis.",
    response_model=GitHubFilesResponse,
)
async def download_repo_async(
    owner: str, repo: str, github_service: GitHubService = Depends(get_github_service)
):
    """
    Endpoint asíncrono que descarga todos los archivos importantes de un repositorio de GitHub.
    """
    result = await github_service.download_repo_files(owner, repo)
    return {"files": result}
