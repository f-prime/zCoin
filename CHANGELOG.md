0.0.8
=====

* Fixed the eval() exploit. 

0.0.3
=====

* Better handling of get_db and get_nodes

0.0.2
=====

* Nodes now do a check of version and will not communicate with other versions of nodes.
* get_nodes now does a check sum on each segment. If the hashes do not match it will be rejected.
