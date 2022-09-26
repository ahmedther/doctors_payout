from oracle_config import Ora
import pandas as pd
from excel_maker import Support

# Step 1: From documentation
# Run OP Query for the month
sup = Support()
db = Ora()
ip_data, ip_column = db.doctor_payout_IP_KH(
    from_date="13-Sep-2022", to_date="13-Sep-2022"
)
df_dp_ip_kh = pd.DataFrame(data=ip_data, columns=list(ip_column))
df_dp_ip_kh = sup.add_name_source_column(
    df_dp_ip_kh, "Source of Data", "IP Admitting Doc wise rev rep"
)
# sup.excel_generator(excel_data=df_dp_ip_kh, page_name="Doctors_Payout_IP")

# Run IP Query for the month
db = Ora()
op_data, op_column = db.doctor_payout_OP_KH(
    from_date="26-Aug-2022", to_date="26-Aug-2022"
)
df_dp_op_kh = pd.DataFrame(data=op_data, columns=list(op_column))
df_dp_op_kh = sup.add_name_source_column(
    df_dp_op_kh, "Source of Data", "Op Rev share for Ext Doc Rep"
)
# sup.excel_generator(excel_data=df_dp_op_kh, page_name="Doctors_Payout_OP")

# creates a log file and report errors
sup.error_log()

# Concatanate both datafreames into one main dataframe
main_dataframe = sup.concat_dataframes(df_dp_ip_kh, df_dp_op_kh)

# Filter out and remove all emergency charges
main_dataframe = sup.filter_out_emergency(main_dataframe)

# Collect Garbase and delete unused dataframe objects
df_dp_ip_kh = sup.delete_dataframe(df_dp_ip_kh)
df_dp_op_kh = sup.delete_dataframe(df_dp_op_kh)


doctors_list_df = pd.read_excel("doctors_list.xlsx")

main_dataframe = sup.filter_aplicable_doctor(main_dataframe, doctors_list_df)

sup.excel_generator(excel_data=main_dataframe, page_name="test")
