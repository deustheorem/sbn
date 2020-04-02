SBN was created to facilitate a desire to speed up the process of connecting to
AWS instances with SSH. But it can solve a variety of issues related to getting
information from AWS about EC2 instances.

This python script uses the AWS Boto3 SDK.

**Warning** This is still under heavy development use with caution.

Table of Contents
-----------------

  * [Requirements](#requirements)
      * [AWS](#aws)
      * [Python](#python)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Examples](#examples)

Requirements
------------

### AWS
If you don't already possess a AWS account with access keys go ahead and obtain
those. Read-only access to ec2 should be all that is needed.

### Python
I've only tested with python 3.8.2.

boto3 is required, this is the AWS Python SDK of choice. To install run:
`pip3 install boto3`

Installation
------------

Local user install:

`cp sbn.py ${HOME}/.local/bin/`

For global install:

`cp sbn.py /usr/local/bin/`

Usage
-----

```
sbn.py -n <Instance Name> -d <Instance Private DNS> -r <Regions>

    -n <Instance Name>
        The Name tag of requested instance(s), -r is requirement
        Output will be a list of instances with <Instance Name>
    -d <Instance Private DNS>
        The private DNS of requested instance
        Output will be details about requested instance
    -r <Regions>
        A comma seperated list of regions to search
        e.g. us-east-1,eu-west-2,ca-central-1
```

Examples
--------

The following is the reason it was created.

`ssh $(sbn.py -n test_instances -r us-east-1,us-east-2 | fzf --preview 'sbn.py -d {}')`

If Bash is your shell of choice you can create a function in your `.bashrc` file.

```
function sbn() {
    ssh $(sbn.py -n ${1} -r us-east-1,us-west-2 | fzf --preview 'sbn.py -d {}')
}
```

Then it can be called by: `sbn test_instances`.

The preview can be removed by modifing the fzf command.

Contributions
-------------

1. Create issue if one doesn't exist
2. Fork it
3. Create your feature branch (`git checkout -b my-new-feature`)
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create a new pull request


