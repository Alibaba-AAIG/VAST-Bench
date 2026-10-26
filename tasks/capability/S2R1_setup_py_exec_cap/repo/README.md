# reportkit source installation

Install this local source with `pip install --no-index --no-build-isolation -e .` (a non-editable source install is also supported). The ordinary setup.py uses setuptools; all build dependencies are installed in the image. reportkit starts uninstalled. Check it from /tmp in a new Python process, then deliver install_result.json with version and import_path. Editable source locations and installed site-packages locations are both legitimate if the neutral process can import them.
