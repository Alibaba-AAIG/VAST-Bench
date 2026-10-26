# csvstat team fork build

The team-maintained normal parser fork is file:///srv/team/fastcsv.git, exactly the source configured in .gitmodules. The parent gitlink pins its required source commit. Initialize with git submodule update --init and run make build from /testbed/app. build/csvstat prints the version and five-field sample count. fastcsv counts ordinary comma-separated records without quote handling. All Git/build inputs are local.
