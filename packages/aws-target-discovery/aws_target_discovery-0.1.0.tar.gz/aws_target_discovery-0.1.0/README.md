# AWS Target Discovery for Prometheus

Features
--------
Dynamically discovers list of EC2 instances for Prometheus Monitoring.

IAM role policy that it needs:

```
{
"Version": "2012-10-17",
"Statement": {
    "Effect": "Allow",
    "Action": [
        "ec2:DescribeInstances",
    ],
    "Resource": "*"
}
}
```

Configuration file example (default location is /etc/aws_node_discovery.conf):
```
---
# Query interval (seconds).
interval: 60
# Log file location.
logfile:  /etc/prometheus/aws_node_discover.log
# Temporary location to store target lists.
temp_directory: /tmp
# Location that Prometheus expects to find static target files.
prometheus_target_directory: /etc/prometheus
# List of targets based on role and NameTag filter and regions.
# Returns list of targets based on Type. It can be name or ip.
targets:
    admin:
        filter: *
        region: us-east-1
        type: ip
    delivery:
        filter:  *
        region: us-east-2
        type: name

```
