# Configuration VS Code

Enables:

* Format on save via [Black](https://black.readthedocs.io/)
* Sort imports using [isort](https://pycqa.github.io/isort/)
* Highlight linting issues with [flake8](https://flake8.pycqa.org/)

```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true
}
```
