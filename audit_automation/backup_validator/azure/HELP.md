## Docs

NOTE: Cloud Shell provides persistent storage only when the Microsoft.CloudShell is registered. Once registered, Cloud Shell grants access to a Linux-based environment with a 5GB Azure Files share mounted as $HOME and ~/clouddrive.

https://learn.microsoft.com/en-us/azure/cloud-shell/persisting-shell-storage

https://learn.microsoft.com/en-us/rest/api/compute/virtual-machines/instance-view?view=rest-compute-2024-11-04&tabs=Python
https://learn.microsoft.com/en-us/rest/api/compute/virtual-machines/list-all?view=rest-compute-2024-11-04&tabs=Python#virtualmachine_listall_minimumset_gen
https://learn.microsoft.com/en-us/rest/api/virtualnetwork/network-interfaces/get?view=rest-virtualnetwork-2024-05-01&tabs=Python
https://learn.microsoft.com/en-us/rest/api/backup/backup-protected-items/list?view=rest-backup-2025-02-01&tabs=Python
https://learn.microsoft.com/en-us/rest/api/backup/backup-jobs/list?view=rest-backup-2025-02-01&tabs=Python
https://learn.microsoft.com/en-us/rest/api/backup/backup-jobs/list?view=rest-backup-2025-02-01&tabs=Python
https://learn.microsoft.com/en-us/rest/api/backup/recovery-points/list?view=rest-backup-2025-02-01&tabs=Python#examples
https://learn.microsoft.com/en-us/rest/api/backup/backup-protected-items/list?view=rest-backup-2025-02-01&tabs=Python

## Troubleshooting

### List Recovery Services Vaults in Azure

This script and command-line reference helps you list **Recovery Services Vaults** (`Microsoft.RecoveryServices/vaults`) in a specified Azure resource group.

#### Azure CLI Method

To list all Recovery Services Vaults in a resource group via the Azure CLI:

```bash
az resource list \
  --resource-group test-rg-1 \
  --resource-type "Microsoft.RecoveryServices/vaults" \
  --output table
  ```

#### Python SDK Method

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.recoveryservices import RecoveryServicesClient

# Authenticate and initialize client
subscription_id = "YOUR_SUB_ID"
credential = DefaultAzureCredential()
recovery_client = RecoveryServicesClient(credential, subscription_id)

# Define resource group
resource_group_name = "test-rg-1"

# List Recovery Services Vaults in the resource group
vaults = recovery_client.vaults.list_by_resource_group(resource_group_name)

# Print results
for vault in vaults:
    print(f"Vault Name: {vault.name}, Location: {vault.location}, Type: {vault.type}")