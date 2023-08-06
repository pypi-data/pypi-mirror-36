# KCK
The old two-hard-things joke ("There are two hard things in computer science: 
cache invalidation, naming things, and off-by-one errors") starts with cache
invalidation because it comes up so often.  Caching can mean 10X or even 1000X
performance improvements, so we developers love to cache things.

And, invariably, caching things means we have to come up with strategies for
keeping the cached data fresh and in-sync with the source data.  Event-based 
cache invalidation is one of the ways we can work to ensure that cached data is
reasonably fresh.  And it can be tricky.

KCK is a set of tools to build caches with less pain and it has some nifty
tricks to squeeze another 10X or 100X out of the performance numbers for certain
workloads.

## Features
* **Sophisticated data pipelines can be written simply.**  Folks with SQL chops can
  build a backend for their new React application in an afternoon.  With a little
  Python, it's pretty straightforward to turn petabytes of corporate data into
  simple statistics for the C-level dashboard.
* **It's really fast.**  KCK manages data flowing in and out of Postgres so it can keep
  its stable of data products up-to-date, but it serves data from a cache built on
  Cassandra and the data gets to the application immediately so long as it's in the
  cache.  And KCK helps make sure the data is in the cache and fresh, before an
  application needs it.
* **Plays well with others.**  KCK makes it easy to use SQL and SQLAlchemy, but it's
  Django-friendly too and it'll happily accept data from any source you can talk to
  with Python.
* **Includes HTTP Server with JWT.** KCK is accessible via an include HTTP server that
  can optionally use JWT to authenticate clients.
* **Makes tiny database servers look fast.** Seriously. KCK reduces database pressure
  to a minimum, then it spreads it out so your database writes don't have to compete
  with a deluge of read traffic from your web servers and background tasks.  And cached
  writes are on the TODO list.
* **Designed to scale.** Both the HTTP servers and the Cassandra cluster on which KCK
  depends can scale horizontally.

## Status
None of this code should be used in production.  It's getting there, but, for now, expect
issues and submit merge requests.

The core parts, in various stages of doneness, are the cache, the http service, the refresh
worker, and the process worker.  The status of each is detailed below.

### The cache
The cache is working and it's pretty nifty.  Cache misses can cause _primers_ to fire,
returning the data and storing it in the cache on the way out so it'll be more quickly
available the next time it's requested.  Cache entries can be invalidated or they can be
set to expire after a certain amount of time.  *But cache entries can also be automatically
refreshed as data is updated, or at a set interval, or even when the system boots up.*

### The HTTP service
The HTTP service is working.  It's very basic, just a /fetch and an /update and,
optionally, JWT authentication so it can be used as a backend for mobile apps or
newer Javascript web apps made with React or Angular. So there's a lot of power
in a pretty simple wrapper and it's easily consumed by other services, languages,
etc.

### The refresh and process workers are _in-progress_
To be fully-functional, there needs to be a refresh worker and a process worker running and
neither of those are working yet.

The process worker is pretty simple and a good chunk of use cases don't require it at all.
It mostly just needs to run a single method every so often so that will go quickly once
I sit down to write it.

The refresh worker, unfortunately, is more important than the process worker, so I'm
working on it first.  I've just completed an overhaul of the background refresh queue
code and it's working in a very simple way, but it needs to be scalable and it needs
to choose tasks to refresh a bit more carefully than it currently does before it's
performing up to spec.  So it's still a few weeks out.

## System overview
Every piece is scalable and the most user-facing components are the most scalable.
The diagram below shows the basics of the KCK system structure.



![Scaling KCK](https://gitlab.com/frameworklabs/kck/raw/master/misc/kck_system_design.png)\


## Quickstart

### Install KCK
To install the latest release of KCK, simply:
`pip install kck`
or add `kck` to the requirements.txt in your project and do a `pip install -r requirements.txt`

To install the development version, add this line to your requirements.txt:

`-e git+https://gitlab.com/frameworklabs/kck.git#egg=kck`

and do a `pip install -r requirements.txt`

### Setup
With the KCK package installed, it's time to craft a config file, define some environment
variables and create some directories.

#### Config file
First, the config.  It tells kck how to talk to your Cassandra cluster and to your data sources.
I recommend putting it next to all of the other settings files for your project.  Something like:
```cassandra:
    hosts: ["cassandra"]
    keyspace: my_project
    tables:
        primary_cache: pri_cache
        secondary_cache: sec_cache
        queued_updates: queued_updates
        queued_refreshes: queued_refreshes
        queued_refreshes_counter: queued_refreshes_counter

kck:
    prime_on_cache_miss: False
    primers_dirpath: /project/frameworklabs/my_project/kck/kprimers
    updaters_dirpath: /project/frameworklabs/my_project/kck/kupdaters
```

The Cassandra config is pretty straightforward.  Defining table names is not likely something that
users will need to change, so the configurability of that will change moving forward.  For now, copy.

For the kck section:

##### prime_on_cache_miss
if this is set to False, a cache miss results in an exception.  If True, the
request blocks until the primer for the requested key completes.

##### primers_dirpath
this defines the directory in which all the primers reside

##### updaters_dirpath
this defines the directory in which all the updaters reside

### Roadmap
#### Better config
the YAML is getting a bit tedious.  I'm inclined to move to SimpleConfig before this gets too far
along.

#### Architecture of apps that make use of KCK
defining the directories for updaters and primers is awkward.  I think we could be just as flexible
if we provide names of modules that contain updater and primer classes.
