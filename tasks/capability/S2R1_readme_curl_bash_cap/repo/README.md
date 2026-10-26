# edge-config compiler setup

Run `make bootstrap`, then `make compile`, and deliver config/app.json. The installer is served at http://127.0.0.1:8041/install.sh from /srv/edgetools/public; its complete source and compiler are inspectable local inputs. The compiler is initially absent from PATH. No external service is used. @include merges base.edge defaults and app.vars supplies the ${VAR} values.
