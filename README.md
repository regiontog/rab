Backup program
==============
TODO
----
1. Refactor docopt
2. Add docs
3. Implement logger
4. Make setup.py work
5. Make tests for syntax
6. Recognize modified files and handle them correctly

Featureset for v1.0.0
---------------------
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
