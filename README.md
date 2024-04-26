<img align="right" src="https://raw.github.com/cliffano/oricat/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/oricat/workflows/CI/badge.svg)](https://github.com/cliffano/oricat/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/oricat/badge.svg)](https://snyk.io/test/github/cliffano/oricat)
[![Published Version](https://img.shields.io/pypi/v/oricat.svg)](https://pypi.python.org/pypi/oricat)
<br/>

Oricat
------

Oricat is a Python CLI for categorising image files by orientation.

This package is intended as a companion for [AWS Tag Editor](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging-resources.html). While AWS Tag Editor is useful for tagging multiple resources in one go, it has no easy way to re-run the tagging since you have to use the AWS console UI, and its resource filtering capability is quite limited, making it hard to select resources with-more-than basic logic.

Using oricat, you can easily re-run the tagging by running the CLI again. And with its support of YAML configuration, it allows you to define multiple tagsets which you can reuse and mix and match with the resources, you can construct your own mapping between the resources and the relevant tags and tagsets. You can generate your own YAML configuration using Python scripts, or any other programming language, allowing you to construct a more complex filtering logic.

Installation
------------

    pip3 install oricat

Usage
-----

Create a configuration file, e.g. `oricat.yaml`:

    ---
    tagsets:
      - name: common
        tags:
          - key: CostCentre
            value: FIN-123
          - key: Organisation
            value: World Enterprise
          - key: Description
            value: AWS Resource
      - name: prod
        tags:
          - key: EnvType
            value: prod
          - key: Availability
            value: 24x7
      - name: nonprod
        tags:
          - key: EnvType
            value: non-prod
          - key: Availability
            value: on-demand
    resources:
      - arn: 'arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail'
        tags:
          - key: Description
            value: High availability SSM document
        tagsetnames:
          - common
          - prod
      - arn: 'arn:aws:s3:::world-enterprise/development/logo.jpg'
        tags:
          - key: Description
            value: World Enterprise logo
        tagsetnames:
          - common
          - nonprod

And then run `oricat` CLI and pass the configuration file path:

    oricat --conf-file oricat.yaml

It will write the log messages to stdout:

    [oricat] INFO Loading configuration file oricat.yaml
    [oricat] INFO Loading 3 tagset(s)...
    [oricat] INFO Loading 2 resource(s)...
    [oricat] INFO Adding resource arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'High availability SSM document'}
    [oricat] INFO Adding resource arn:aws:s3:::world-enterprise/development/logo.jpg to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'World Enterprise logo'}

And if the tagging failed (e.g. due to rate exceeded), it will log the following error messages:

    [oricat] ERROR Failed to apply tags to 1 resource(s):
    [oricat] ERROR arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail: 400 - Throttling - Rate exceeded
    [oricat] ERROR arn:aws:s3:::world-enterprise/development/logo.jpg: 400 - Throttling - Rate exceeded

### YAML includes

oricat supports YAML includes using , so you can split your configuration into multiple files:

    ---
    tagsets:
      - !include include.d/tagset.yaml
    resources: !include include.d/resources.yaml

Include files should be put under `include.d/`` folder relative to the configuration file.

The included tagset file `include.d/tagset.yaml`:

    ---
    name: common
    tags:
      - key: CostCentre
        value: FIN-123
      - key: Organisation
        value: World Enterprise
      - key: Description
        value: AWS Resource

The included resources file `include.d/resources.yaml`:

    ---
    - arn: 'arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail'
      tags:
        - key: Description
          value: High availability SSM document
      tagsetnames:
        - common
        - prod
    - arn: 'arn:aws:s3:::world-enterprise/development/logo.jpg'
      tags:
        - key: Description
          value: World Enterprise logo
      tagsetnames:
        - common
        - nonprod

### Dry run

You can also run oricat in dry-run mode by adding `--dry-run` flag:

    oricat --conf-file oricat.yaml --dry-run

During dry-run mode, oricat log messages will be labeled with `[dry-run]`:

    [dry-run] [oricat] INFO Loading configuration file oricat.yaml
    [dry-run] [oricat] INFO Loading 3 tagset(s)...
    [dry-run] [oricat] INFO Loading 2 resource(s)...
    [dry-run] [oricat] INFO Adding resource arn:aws:ssm:ap-southeast-2:123456789012:document/high-avail to a batch with tags {'CostCentre': 'FIN-123', 'Organisation': 'World Enterprise', 'Description': 'AWS Resource', 'EnvType': 'prod', 'Availability': '24x7', 'Description': 'High availability SSM document'}

### Batch size

In order to optimise the number of API calls, resources with identical tags are put into batches. By default, the batch size is 5.
You can run oricat with a custom batch size `--batch-size <number>` flag:

    oricat --conf-file oricat.yaml --batch-size 10

### Delay

In order to avoid rate exceeded error, you can run oricat with a custom delay `--delay <number>` flag:

    oricat --conf-file oricat.yaml --delay 5

By default, the delay is 2 seconds. The delay is applied between each batch of tagging API calls.

Please note that AWS limits the number of tagging API (`tag_resources`) calls to [maximum of 5 calls per second](https://docs.aws.amazon.com/general/latest/gr/arg.html).

Configuration
-------------

These are the configuration properties that you can use with `oricat` CLI.
Some example configuration files are available on [examples](examples) folder.

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `tagsets[]` | Array | A list of one or more tagsets. Any tagset can be associated with any resource, and the resource will include the tags specified in the tagset. | |
| `tagsets[].name` | String | The name of the tagset. | `common` |
| `tagsets[].tags[]` | Array | A list of one or more key-value pair tags within the tagset. | |
| `tagsets[].tags[].key` | String | The tag key. | `CostCentre` |
| `tagsets[].tags[].value` | String | The tag value. | `FIN-123` |
| `resources[]` | Array | A list of one or more AWS resources. Each of the resource has a corresponding list of tags, along with the tags from tagsets. | |
| `resources[].arn` | String | AWS resource [ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html). | `arn:aws:s3:::world-enterprise/development/logo.jpg` |
| `resources[].tags[]` | Array | A list of one or more key-value pair tags of the resource. | |
| `resources[].tags[].key` | String | The tag key. | `Description` |
| `resources[].tags[].value` | String | The tag value. | `Some description` |
| `resources[].tagsetnames[]` | Array | A list of one or more tagset names. All tags within the tagsets specified are included in the resource. | |

Permissions
-----------

The AWS credentials used to run `oricat` CLI must have [the following permissions](https://docs.aws.amazon.com/ARG/latest/userguide/gettingstarted-prereqs.html):

* Permission to use AWS Resource Groups API
* Permission to tag resources for individual AWS services that you want to tag

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/oricat/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/oricat/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/oricat/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/oricat/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/oricat/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/oricat/doc/sphinx/index.html)
