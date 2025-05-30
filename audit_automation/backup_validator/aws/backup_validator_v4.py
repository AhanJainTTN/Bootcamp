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

    # Loading master data file
    master_data_file = os.path.join(base_dir, "files", "ec2_validator_master_data.xlsx")
    master_data = pd.read_excel(master_data_file, sheet_name=None)

    output_sheets = {}
    for accountid, rows_list in backup_data_dict.items():
        try:
            master_df = master_data[accountid]
        except KeyError as e:
            print(f"{accountid} absent in master sheet: {e}")
            continue

        raw_df = pd.DataFrame(rows_list)

        matched_df, missing_df = validate_sheet(raw_df, master_df)

        output_sheets[accountid] = matched_df
        output_sheets[f"{accountid}_Missing"] = missing_df

    # Convert each DataFrame to JSON string and set as environment variable
    for sheet_name, df in output_sheets.items():
        try:
            df_dict = df.to_dict(orient="records")
            df_str = json.dumps(df_dict)
            # os.environ[sheet_name] = df_str
        except Exception as e:
            print(f"Failed to set env var for {sheet_name}: {e}")


def load_from_json(json_path):
    with open(json_path, "r") as file:
        return json.load(file)


def main():
    process_all_sheets()


if __name__ == "__main__":
    main()
