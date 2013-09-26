Backup program
==============
TODO
----
1. Create nosetests
2. Add docs
3. Make read_file(file) easier to read and understand
4. Work out the command syntax

Featureset for v1.0.0
----
* Deduplicates at block level
* Rabin sliding window to detirmine blocks
* Store hashes of blocks
* Store blocks encrypted?
* Create snapshots which only reference the blocls
* Restore from snapshot(entire and just single/multiple file(s))
* Mount snapshot (fuse)
    * Delete/create/change files
* Automated backups
* Client/Server
* Multiple systems, shared data
    * Multiple keys per block?
* Compression
* Deduplicate before sending over network
* Check for collisions
* Private/Public keys
