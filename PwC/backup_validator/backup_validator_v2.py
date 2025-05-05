from datetime import datetime
import json
import os
import pandas as pd

report_date = datetime.today().strftime("%Y-%m-%d")


def validate_sheet(raw_data, master_data):
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


def process_all_sheets():
    base_dir = os.path.dirname(__file__)

    # Loading simulated raw data
    raw_data_file = os.path.join(base_dir, "files", "raw_data.json")
    backup_data_dict = load_from_json(raw_data_file)

    # Loading mastre data file
    master_data_file = os.path.join(base_dir, "files", "ec2_validator_master_data.xlsx")
    master_data = pd.read_excel(master_data_file, sheet_name=None)

    output_sheets = {}
    for accountid, rows_list in backup_data_dict.items():
        try:
            master_df = master_data[accountid]
        except KeyError as e:
            print(f"{accountid} absent in master sheet: {e}")

        raw_df = pd.DataFrame(rows_list)

        # Azure environment has repeated InstanceNames but InstanceIDs are unique
        # InstanceIDs are equivalent to InstanceNames of other envs therefore swapping values
        if accountid == "Azure":
            raw_df = swap_column_values(raw_df, "InstanceID", "InstanceName")
            master_df = swap_column_values(master_df, "InstanceID", "InstanceName")

        matched_df, missing_df = validate_sheet(raw_df, master_df)

        if accountid == "Azure":
            matched_df = swap_column_values(matched_df, "InstanceID", "InstanceName")
            missing_df = swap_column_values(missing_df, "InstanceID", "InstanceName")

        output_sheets[accountid] = matched_df
        output_sheets[f"{accountid}_Missing"] = missing_df

    output_file = os.path.join(base_dir, "files", "ec2_validator_result.xlsx")
    with pd.ExcelWriter(output_file) as excel_writer:
        for sheet_name, df in output_sheets.items():
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)


def swap_column_values(df, col1, col2):
    df[col1], df[col2] = df[col2].copy(), df[col1].copy()
    return df


def load_from_json(json_path):
    with open(json_path, "r") as file:
        return json.load(file)


def main():
    process_all_sheets()


if __name__ == "__main__":
    main()
