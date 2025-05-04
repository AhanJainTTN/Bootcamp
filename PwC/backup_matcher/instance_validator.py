"""
Input:
- Two data sources:
    1. Master File (Excel workbook, .xlsx format) containing reference data.
    2. Raw EC2 Data File (Excel workbook or CSV) with the current state of EC2 instances.

Task:
- Validate records in the Master File against the Raw EC2 Data.
- Identify which records from the Raw EC2 Data are present in the Master File and which are missing.
- Generate an output Excel file with validation results across two sheets.

TODO: Confirm whether we arw only concenrned with instances that exist in the Raw Data but are missing from the Master File (i.e. all the extra entries present in Raw Data absent from the Master file), and NOT on instances that exist in the Master File but are absent from the Raw Data.

TODO: What column to use for joining - InstanceID or InstanceName? Azure sheet values - repeated instance names - which column to use for joining? Should I just use InstanceID for Azure?

TODO: Ask what will be the nature of raw input data? Will it be an Excel workbook with different sheets? In that case, should the output file have two sheets corresponding to each sheet (Amazon -> Amazon (Present) | Amazon (Absent)) or just add a column indicating ASP, Amazon, Azure etc.

Validation Logic:
For each row in the Raw EC2 Data file:

1. Check if the InstanceName exists in the Master File:
    - If a match is found:
        - Copy the entire row from the Raw EC2 Data to "Present" in the output file.
        - Add a column named BackupCount_Match with values:
            - "Yes" if BackupCount in the Raw EC2 Data matches BackupCount in the Master File for the same InstanceName.
            - "No" if BackupCount does not match.
    - If no match is found:
        - Copy the entire row from the Raw EC2 Data to "Absent" in the output file (representing unmatched records).

2. In both "Present" and "Absent", append an additional column named Validation_Date containing the date on which the script was executed (i.e., the validation run date).

Output:
- A new Excel workbook containing:
    - "Present": Rows from Raw EC2 Data with matching InstanceNames in the Master File, including a BackupCount_Match column indicating match status.
    - "Absent": Rows from Raw EC2 Data where the InstanceName was not found in the Master File.
    - Both sheets include a Validation_Date column with the run date of the validation process.
"""

from datetime import datetime
import os
import pandas as pd

# Load raw_data wb, master_data wb
# for every sheet in raw_data wb
#   check if sheet exists in master_data_wb
#   if azure handle differently
#   else run validate_data function and append result of matched and missing to "Present" and "Absent" dataframe respectively
#   append sheet name to source column
#   dump dataframe to excel wb


def validate_instance_sheet(raw_data, master_data):
    merged_sheet = pd.merge(
        left=raw_data, right=master_data, how="left", on=["InstanceName"]
    )

    matched_rows = merged_sheet.loc[merged_sheet["InstanceID_y"].notna()]
    missing_rows = merged_sheet.loc[merged_sheet["InstanceID_y"].isna()]

    matched_df = raw_data.loc[matched_rows.index]
    missing_df = raw_data.loc[missing_rows.index]

    matched_df["BackupCountMatch"] = (
        matched_rows["BackupCount_x"] == matched_rows["BackupCount_y"]
    )

    return matched_df, missing_df


def reconcile_all_sheets(raw_data_file, master_data_file):
    raw_df = pd.read_excel(raw_data_file, sheet_name=None)
    master_df = pd.read_excel(master_data_file, sheet_name=None)

    reconciled_matched = list()
    reconciled_missing = list()

    for sheet_name in raw_df:
        if sheet_name != "Azure":
            matched_df, missing_df = validate_instance_sheet(
                raw_df[sheet_name], master_df[sheet_name]
            )
            matched_df = add_validation_metadata(matched_df, sheet_name)
            missing_df = add_validation_metadata(missing_df, sheet_name)

            reconciled_matched.append(matched_df)
            reconciled_missing.append(missing_df)

    return pd.concat(reconciled_matched), pd.concat(reconciled_missing)


def add_validation_metadata(df, source_sheet):
    df["Validation_Date_(MM/DD/YYYY)"] = datetime.today().strftime("%-m-%-d-%-Y")
    df["Source"] = source_sheet
    return df


def create_spreadsheet(matched_df, missing_df, output_file):
    with pd.ExcelWriter(output_file) as writer:
        matched_df.to_excel(writer, sheet_name="Present", index=False)
        missing_df.to_excel(writer, sheet_name="Absent", index=False)


def main():
    base_dir = os.path.dirname(__file__)
    raw_data_file = os.path.join(base_dir, "files", "ec2_validator_raw_data.xlsx")
    master_data_file = os.path.join(base_dir, "files", "ec2_validator_master_data.xlsx")
    output_file = os.path.join(base_dir, "files", "reconciled.xlsx")

    matched_df, missing_df = reconcile_all_sheets(raw_data_file, master_data_file)
    create_spreadsheet(matched_df, missing_df, output_file)


if __name__ == "__main__":
    main()
