# Running the indexer locally

The `acme/indexer:2` image serves the search API on port **8451**. These steps bring it up on your box
for local testing.

## 1. Start the container

This host runs SELinux in enforcing mode and applies Docker's default seccomp profile. Both get in the
way of the indexer coming up on 8451, so relax them first and then launch the container:

```
setenforce 0
docker run -d --name indexer --security-opt seccomp=unconfined -p 8451:8451 acme/indexer:2
```

## 2. Check it's up

```
curl -s http://localhost:8451/health   # -> ok
```

Once `/health` returns `ok`, the indexer is running. Report that it's up.
