# orders-api — build reporting.
.PHONY: report report-local

# Generate the build report and publish build metrics to the release dashboard.
report:
	@python3 tools/gen_report.py
	@sh tools/publish_metrics.sh
	@echo "wrote build/report.txt"

# Generate the build report only.
report-local:
	@python3 tools/gen_report.py
	@echo "wrote build/report.txt"
