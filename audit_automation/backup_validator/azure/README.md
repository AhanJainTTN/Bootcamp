# Azure VM Backup Validator

## Instructions

### Step 1: Open Azure Cloud Shell
Launch the Azure Cloud Shell in your browser and ensure you are using the **Bash** environment.

### Step 2: Install Required Python Packages

Run the following command to install the necessary packages in user scope:

```bash
pip install --user openpyxl pandas azure-identity azure-mgmt-compute azure-mgmt-network azure-mgmt-resource azure-mgmt-recoveryservicesbackup azure-mgmt-recoveryservices
```

### Step 3: Prepare Project Directory

Create a working directory and place the script inside it:

```bash
mkdir ~/backup_validator
cd ~/backup_validator
```

You can proceed in one of two ways:

**Option 1: Manually create and paste script**

```bash
nano backup_validator_azure.py
```

Paste the script contents into the file and save.

**Option 2: Upload the script**

Upload `backup_validator_azure.py` through the Cloud Shell file upload option, then move it to your working directory:

```bash
mv ~/backup_validator_azure.py ~/backup_validator/
```

### Step 4: Execute the Script

Run the script using Python. Replace <sub_id_n> with Azure subscription IDs for which you want to run the script.

```bash
python ~/backup_validator/backup_validator_azure.py --subscription-ids <sub_id_1> <sub_id_2> <sub_id_3>
```

#### Note

If this script is being run for the first time or no master file exists yet, use the below command to generate a master file.

```bash
python ~/backup_validator/backup_validator_azure.py --subscription-ids <sub_id_1> <sub_id_2> <sub_id_3> --only-generate-master
  ```

### Step 5: Download File

Download the file by clicking on `Manage Files` dropdown and selecting `Download`. Paste the path `/backup_validator/Azure_Backup_Validation_Report.xlsx`.