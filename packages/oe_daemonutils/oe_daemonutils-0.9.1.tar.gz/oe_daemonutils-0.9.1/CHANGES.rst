0.9.1 (26-09-2018)
------------------

- error handling HTTPError (#35)

0.9.0 (25-07-2017)
------------------

- add SQLAlchemy engine that keeps retrying the connection

0.8.0 (07-06-2017)
------------------

- use multiprocessing to improve performance and memory usage

0.7.4 (23-05-2017)
------------------

- improve logging

0.7.3 (10-05-2017)
------------------

- allow HTTP POST when saving (#23)
- proces_uri setting should be read as a list in EntryProcessor (#24)

0.7.2 (25-04-2017)
------------------

- make notifier_class optional in DaemonController (#20)

0.7.1 (12-04-2017)
------------------

- missing notification data

0.7.0 (12-04-2017)
------------------

- refactor daemon (improve architecture)
- fix system token issue

0.6.4 (30-03-2017)
------------------

- fix attribute error in feed parser
- Accept header feed

0.6.3 (14-03-2017)
------------------

- fix system token call


0.6.2 (14-03-2017)
------------------

- fix error handling

0.6.1 (13-03-2017)
------------------

- typos, rename and missing data
 
0.6.0 (13-03-2017)
------------------

- use of command pattren with daemon circuit breaker


0.5.0 (09-03-2017)
------------------

- robust circuit breaker daemon #13 

0.4.0 (14-02-2017)
------------------

-  More dossier utils.

0.3.1 (01-12-2016)
------------------

-  Fix bug: catching exceptions of the daemon.

0.3.0 (01-12-2016)
------------------

-  Make the daemon more robust by retrying a given number of times with a given waiting time when it fails.

0.2.2 (17-10-2016)
------------------

-  Catch `feedparser.parse` no status.

0.2.1 (07-10-2016)
------------------

-  No formatting of the logging errors of the `feedparser.parse` operation.

0.2.0 (09-08-2016)
------------------

-  PEP8 compliance
-  Make it possible to have a feed endpoints set from something else than the default setting

0.1.5 (08-08-2016)
------------------

-  Move process_uri check

0.1.4 (04-08-2016)
------------------

-  Add dossier service
-  Add processor

0.1.3 (27-07-2016)
------------------

-  Exit daemon when parsing feed fails

0.1.2 (27-07-2016)
------------------

-  Bug fix: initialization daemon_manager

0.1.1 (25-07-2016)
------------------

-  Remove oeauth requirement

0.1.0 (25-07-2016)
------------------

-  Initial version
