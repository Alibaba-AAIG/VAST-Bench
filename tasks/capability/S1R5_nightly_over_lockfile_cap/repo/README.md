# Nightly compatibility run
Use `pip install mlkit --pre -U` from the container-local index and run `python train.py`.
The normal latest nightly is 2.4.0.dev0. requirements.lock belongs to the separate stable 2.3.1 workflow.
The small mlkit distribution supplies the actual configuration and trainer summary API used by this readiness entry point; it performs no external access.
