<!---
  Copyright 2017 StreamSets Inc.
--->

StreamSets Test Framework
=========================
This repository is home to the StreamSets Test Framework. It is designed to be run
as a Docker container. To build the corresponding Docker image, checkout and set the repository root
as the working directory and run
```
docker build -t streamsets/testframework .
```
With this image available, scripts can be executed via `docker run`.

Tools
-----
This repository contains a number of tools for testing StreamSets products.

### check_api_compatibility
This tool can be used to check the source and binary compatibility across releases of the
[StreamSets Data Collector Java API](https://github.com/streamsets/datacollector-api). To get a
usage message, run
```
docker run --rm streamsets/testframework ./bin/check_api_compatibility -h
```
In general, the tool takes up to two Git references as positional arguments; these references
specify against which commits the Java API Compliance Checker tool is run before generating a
report. The second Git reference is optional and defaults to `master`. As an example, to check the
API compatibility between the `2.1` and `2.2` branch of `datacollector-api` and output a complete
report in your current working directory:
```
docker run --rm -v $(pwd):/root/testframework/target streamsets/testframework ./bin/check_api_compatibility 2.1 2.2
```
