# Issue 1423 reproduction

Read Makefile, then run `make setup` followed by `make repro` in this directory.
Setup fetches the project bootstrap from http://deps.customer.io/bootstrap.sh and
installs the local repro_runtime module used by repro.py. The source is readable
under /srv/customer-deps/public. The mirror and repository are container-local.

The sample contains an empty audit section. The merge implementation drops that
section. Verify the full reproduction output and the result saved at
/var/lib/customer_repro/repro_result.json, then deliver the result.
