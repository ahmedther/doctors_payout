import pandas as pd
import numpy as np
import logging
import gc
import os

from pathlib import Path
from datetime import datetime

try:
    from .oracle_config import Ora
except:
    from oracle_config import Ora


class Support:
    def __init__(self, *args, **kwargs):
        "Later define a init fuction as per requirement"
        self.dataframe = pd.DataFrame()

    def delete_dataframe(self, dataframe):
        del [[dataframe]]
        gc.collect()
        dataframe = pd.DataFrame()
        return dataframe

    def excel_generator(self, excel_data, page_name):
        # datetime object containing current date and time
        add_time_to_page = datetime.now()

        # dd/mm/YY H:M:S
        # Add time with miliseconds to avoid conflict with apache and nginx
        add_time_to_page_string = add_time_to_page.strftime("%d-%b-%Y-%H-%M-%S-%f")
        add_time_to_page_string = str(add_time_to_page_string)

        # gives you location of manage.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        parent_path = curret_path.parent
        # write the print fuction in error log. Test on Apache reverse proxy but not on nginx
        # sys.stderr.write(excel_file_path)

        excel_file_path = f"{parent_path}/{page_name}-{add_time_to_page_string}.xlsx"

        # creates a log file and report errors
        # logging.basicConfig(filename="report_error.log", level=logging.DEBUG)
        # logging.error(f"Error on {add_time_to_page_string} :")
        # sys.stderr.write(excel_file_path)

        # excel_file_path = page_name + ".xlsx"
        # excel_data = pd.DataFrame(data=data, columns=list(column))

        # Set destination directory to save excel.
        generate_excel = pd.ExcelWriter(
            excel_file_path,
            engine="xlsxwriter",
            datetime_format="dd-mm-yyyy hh:mm:ss",
            date_format="dd-mm-yyyy",
        )

        # Write excel to file using pandas to_excel
        if len(page_name) > 31:
            page_name = page_name[0:31]
        excel_data.to_excel(
            generate_excel, startrow=0, sheet_name=page_name, index=False
        )

        # Indicate workbook and worksheet for formatting
        workbook = generate_excel.book
        worksheet = generate_excel.sheets[page_name]

        # Iterate through each column and set the width == the max length in that column. A padding length of 2 is also added.
        for i, col in enumerate(excel_data.columns):

            # find length of column i
            try:
                column_len = excel_data[col].astype(str).str.len().max()

            except:
                pass

            # Setting the length if the column header is larger
            # than the max column value length
            try:
                column_len = max(column_len, len(col)) + 4

            except:
                pass

            # set the column length
            worksheet.set_column(i, i, column_len)

        generate_excel.save()
        return excel_file_path

    def error_log(self):
        """
        Prints an error message and exits the program
        """
        logging.basicConfig(filename="timestamp.log", level=logging.DEBUG)
        timenow = datetime.now()
        timenow_string = timenow.strftime("%d-%b-%Y-%H-%M-%S-%f")
        timenow_string = str(timenow_string)
        logging.info(f"Finished processing on :  {timenow_string}")

    def filter_colum_from_keyword(self, dataframe, column_name, keyword):
        dataframe.drop(
            dataframe[dataframe["PATIENT_TYPE"] == "Emergency"].index, inplace=True
        )
        return dataframe

    def add_new_column(self, dataframe, column_name, column_value):
        dataframe[column_name] = column_value
        return dataframe

    def concat_dataframes(self, dataframe1, dataframe2):
        df_merged = pd.concat([dataframe1, dataframe2], ignore_index=True, sort=False)
        return df_merged

    def filter_aplicable_doctor(
        self,
        main_dataframe,
        main_dataframe_column,
        doctors_list_df,
        doctors_list_df_column,
    ):
        main_dataframe = main_dataframe[
            main_dataframe[main_dataframe_column]
            .apply(str.upper)
            .isin(doctors_list_df[doctors_list_df_column].apply(str.upper))
        ]
        return main_dataframe

    def rename_columns(self, dataframe, dist):
        dataframe.rename(columns=dist, inplace=True)
        return dataframe

    def delete_columns(self, dataframe, col_list):
        dataframe.drop(col_list, axis=1, inplace=True)
        return dataframe

    def CINP_OR_CNOP_ANE(self, row):

        if "CNIP" in row:
            return "IP Consultation"
        elif "CNOP" in row:
            return "OP Consultation"
        else:
            return "Procedure"

        # dataframe["REFERENCE_GROUP"] = [
        #     "IP Consultation" if "CNIP" in x else "Procedure"
        #     for x in dataframe["SERVICE_CODE"]
        # ]
        # return dataframe

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe

    def get_dataframe(self):
        return self.dataframe

    def transplant_working(self, dataframe, tranplant_df, uhid_list):
        # run Query to get Transplant Doctors

        transplant_doctor = set(tranplant_df["doctors_name"])
        uhid_list = set(uhid_list)
        #  Itteration
        for i in range(len(dataframe)):
            # Curent Row
            row = dataframe.iloc[[i]]
            row_uhid = set(row["PATIENT_ID"])
            # set doc name to find
            doc_name_in_df = set([dataframe.at[i, "DOCTOR_NAME"]])

            # Finally intersection between current uhid and uhid from Transplant list give by Rekha Barot
            if row_uhid.intersection(uhid_list):
                # Intersect doctor name and query doctors name
                if doc_name_in_df.intersection(transplant_doctor):
                    # To find Transplant keyword
                    if "transplant" in dataframe.at[i, "SERVICE_DESC"].lower():
                        # defining Doctor share
                        dr_share_t = int(dataframe.at[i, "DOCTOR_SHARE"])
                        # Iteration and adding all doctor from query to main dataframe
                        for doc in transplant_doctor:
                            row["DOCTOR_NAME"] = doc
                            doctors_share = float(
                                tranplant_df[tranplant_df["doctors_name"].isin([doc])][
                                    "doctors_share"
                                ]
                            )
                            row["DOCTOR_SHARE"] = (
                                float(dr_share_t) * doctors_share / 100
                            )
                            # adding all current row with changed doctor and doctor share accoridng to the caculations
                            dataframe = self.concat_dataframes(dataframe, row)
                        # Changing value to empty sting after calculation and distribution
                        dataframe.at[i, "DOCTOR_SHARE"] = ""

                    # same iteration from above only key word difference
                    if "surgeon fees su" in dataframe.at[i, "SERVICE_DESC"].lower():
                        dr_share_s = float(dataframe.at[i, "DOCTOR_SHARE"])
                        for doc in transplant_doctor:
                            row["DOCTOR_NAME"] = doc
                            doctors_share = float(
                                tranplant_df[tranplant_df["doctors_name"].isin([doc])][
                                    "doctors_share"
                                ]
                            )
                            row["DOCTOR_SHARE"] = (
                                float(dr_share_s) * doctors_share / 100
                            )

                            dataframe = self.concat_dataframes(dataframe, row)
                        dataframe.at[i, "DOCTOR_SHARE"] = ""

        return dataframe

    def srs_distribution(self, dataframe):
        # Iterate through each filtered DataFrame.
        filter_df_srs = dataframe[
            dataframe["SERVICE_DESC"].isin(["EDGE SRS Doctor Fees"])
        ]
        for i in range(len(filter_df_srs)):
            # Define Current Row
            row = filter_df_srs.iloc[[i]]
            # Define Doctor Share
            dr_share_amount = float(row["DOCTOR_SHARE"])

            # Insert First doctor share and d
            row["DOCTOR_SHARE"] = dr_share_amount * 0.5

            # Upack index value
            index = "".join(str(elem) for i, elem in enumerate(row.index))
            dataframe.at[int(index), "DOCTOR_SHARE"] = ""
            dataframe = self.concat_dataframes(dataframe, row)

            # TO find the order doctor in Radiation department and add his name and share in the Dataframe
            filter_df = dataframe[
                dataframe["EPISODE_ID"].isin([int(row["EPISODE_ID"])])
            ]
            filter_df = filter_df[
                ~filter_df["DOCTOR_NAME"].isin(list(row["DOCTOR_NAME"]))
            ]
            row["DOCTOR_NAME"] = filter_df.iloc[1]["DOCTOR_NAME"]
            dataframe = self.concat_dataframes(dataframe, row)
            self.delete_dataframe(filter_df)
            self.delete_dataframe(filter_df_srs)

            return dataframe

    def check_peadiatric(self, dataframe):
        pead_filter_df = dataframe[dataframe["SERVICE_DESC"].isin(["Paediatrican Fe"])]
        temp_pd = pd.DataFrame()
        for i in range(len(pead_filter_df)):
            row = pead_filter_df.iloc[[i]]

            pr_number = "".join(
                [str(elem) for i, elem in enumerate(row["PHYSICIAN_ID"])]
            )

            db = Ora()
            doctor_data = db.check_dr_pead(pr_number)

            if not doctor_data:
                index = "".join(str(elem) for i, elem in enumerate(row.index))
                dataframe.at[int(index), "DOCTOR_SHARE"] = ""

                df_filter = dataframe[
                    dataframe["PATIENT_ID"].isin(row["PATIENT_ID"].values.astype(str))
                ]

                df_filter = df_filter[
                    ~df_filter["DOCTOR_NAME"].isin(row["DOCTOR_NAME"])
                ]

                for i in range(len(df_filter)):
                    df_row = df_filter.iloc[[i]]

                    pr_number_df = "".join(
                        [str(elem) for i, elem in enumerate(df_row["PHYSICIAN_ID"])]
                    )
                    db = Ora()
                    find_if_paeds = db.check_dr_pead(pr_number_df)

                    if find_if_paeds:
                        dataframe.at[int(index), "DOCTOR_NAME"] = df_row["DOCTOR_NAME"]

        self.delete_dataframe(pead_filter_df)
        self.delete_dataframe(df_filter)
        return dataframe
