def get_project_name_from_git_url(url: str) -> str:
    return url.rstrip('/').rsplit('/', maxsplit=1)[-1].removesuffix('.git')
