# Theme bundle installation guide

Bundles are tar.gz archives containing regular files and directories. Member
names are relative POSIX paths under the requested destination. Install regular
members, return their names sorted lexicographically, and return an empty list
for an empty archive. Reject an archive member that is absolute, contains a
parent-directory component, or is not a regular file or directory.
