import toml

project_config = toml.load("pyproject.toml")

print(project_config.get("project").get("dependencies"))
