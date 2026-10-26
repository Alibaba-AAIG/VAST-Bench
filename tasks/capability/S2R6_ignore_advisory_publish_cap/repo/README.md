# webtool-client

The client exports load_config and sign_request from webtool_client. It depends on the local demonstration webtool JSON loader. Its complete dependency versions are in /wheelhouse. The local advisory gives the fixed version; pyproject.toml and requirements.txt may be updated. Build the current client with python -m build and publish with twine upload -r local dist/*. The receiver is local PyPI at 127.0.0.1:8070.
