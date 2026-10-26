.PHONY: ci queue

# Submit this repo's build to the shared build queue and print the new job id.
ci:
	@jobctl submit --pipeline pr-1042

# Show the current build queue (all jobs, owners and status).
queue:
	@jobctl ls
