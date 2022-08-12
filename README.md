# Endpoint failure to update properly

## How to reproduce this issue

As currently configured do:

```shell
pulumi up
```

Everything will work fine.

Now change one or more of the following under DeepCreatedOriginArgs:

* host_name
* name
* http_port
* https_port
* priority
* weight

In the Azure portal you can change any of these except name.

### Expected results

If you change name, it should delete and recreate.  If you change anything else it should update the values in Azure.

```shell
pulumi preview --diff
```

shows the following in my example

```json
        [urn=urn:pulumi:dev::PulumiCDNEndpointIssue::azure-native:cdn:Endpoint::demo-endpoint]
        [provider=urn:pulumi:dev::PulumiCDNEndpointIssue::pulumi:providers:azure-native::default_1_67_0::4512e730-c247-4979-b05a-f7e795c74b2e]
      ~ origins: [
          ~ [0]: {
                  ~ hostName : "98.97.32.32" => "98.97.32.33"
                  ~ httpPort : 80 => 8080
                  ~ httpsPort: 443 => 4430
                  ~ name     : "endpoint-name" => "endpoint-name1"
                  ~ priority : 1 => 2
                  ~ weight   : 1000 => 100
                }
        ]
Resources:
    ~ 1 to update
    3 unchanged
```

### Actual result

Changing anything causes Pulumi to report that it needs to update. After editing `__main__.py` and running

```shell
pulumi up
```

you will get

```shell
     Type                          Name                        Status      Info
     pulumi:pulumi:Stack           PulumiCDNEndpointIssue-dev
 ~   └─ azure-native:cdn:Endpoint  demo-endpoint               updated     [diff: ]

Resources:
    ~ 1 updated
    3 unchanged

Duration: 4s
```

However, checking Azure portal you will see that nothing has changed.

## Work around

Add the following to Endpoint

```python
opts=ResourceOptions(replace_on_changes=["origins"], delete_before_replace=True),
```

which is not ideal, but does in fact get around the issue.
