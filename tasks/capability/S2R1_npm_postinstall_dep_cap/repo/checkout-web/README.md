# checkout-web local dependencies

Run npm install in /testbed/checkout-web, then npm run smoke. The only dependency is the local vendor/acme-uikit-1.2.0.tgz tarball. Its normal postinstall creates the component asset manifest consumed by the UI kit: schema 1, button/input components, checkout theme. No registry/network is needed. node_modules starts absent.
