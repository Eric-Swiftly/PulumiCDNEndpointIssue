"""An Azure RM Python Pulumi program"""

from pulumi_azure_native import cdn
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("endpoint-demo", location="westus")

profile = cdn.Profile("demo-profile",
                      location="westus",
                      profile_name="demo-profile",
                      resource_group_name=resource_group.name,
                      sku=cdn.SkuArgs(name=cdn.SkuName.STANDARD_MICROSOFT))

endpoint = cdn.Endpoint(
    "demo-endpoint",
    endpoint_name="pulumi811", # must be globally unique
    location="westus",
    optimization_type=cdn.OptimizationType.GENERAL_WEB_DELIVERY,
    origins=[
        cdn.DeepCreatedOriginArgs(host_name="98.97.32.32", # Using a random IP so it makes Custom origin type and we don't need another Azure resource to point at
                                  name="endpoint-name", # Azure portal says can't be changed after creation
                                  http_port=80, # Should be updatable
                                  https_port=443, # Should be updatable
                                  priority=1, # Should be updatable between 1 and 5
                                  weight=1000) # Should be updatable between 1 and 1000
    ],
    profile_name=profile.name,
    query_string_caching_behavior=cdn.QueryStringCachingBehavior.IGNORE_QUERY_STRING,
    resource_group_name=resource_group.name)
