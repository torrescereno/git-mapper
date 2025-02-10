from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GIT MAPPER API"
    debug: bool
    github_token: str

    EXCLUDED_DIRS: set = {
        "node_modules",
        ".git",
        "docs",
        "tests",
        "test",
        "vendor",
        "build",
        "dist",
        "LICENSES",
    }
    EXCLUDED_FILE_EXTENSIONS: set = {
        ".md",
        ".txt",
        ".json",
        ".yml",
        ".yaml",
        ".xml",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".svg",
        ".webp",
        ".csv",
        ".xlsx",
        ".xls",
    }
    EXCLUDED_FILE_NAMES: set = {
        "README",
        "README.md",
        ".gitignore",
    }

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
