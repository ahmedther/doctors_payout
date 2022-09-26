from oracle_config import Ora
import pandas as pd
from excel_maker import Support

sup = Support()

# Step 1 : Maiking the main DataFrame
df_dp_ip_kh = pd.read_excel("resources/ip_payout.xlsx")
df_dp_ip_kh = sup.add_name_source_column(
    df_dp_ip_kh, "SOURCE OF DATA", "IP Admitting Doc wise rev rep"
)
# sup.excel_generator(excel_data=df_dp_ip_kh, page_name="test")

df_dp_op_kh = pd.read_excel("resources/op_payout.xlsx")
df_dp_op_kh = sup.add_name_source_column(
    df_dp_op_kh, "SOURCE OF DATA", "Op Rev share for Ext Doc Rep"
)
main_dataframe = sup.concat_dataframes(df_dp_ip_kh, df_dp_op_kh)
df_dp_ip_kh = sup.delete_dataframe(df_dp_ip_kh)
df_dp_op_kh = sup.delete_dataframe(df_dp_op_kh)

# Delete Emergency Servie and Charges
main_dataframe = sup.filter_out_emergency(main_dataframe)

#
doctors_list_df = pd.read_excel("doctors_list.xlsx")

main_dataframe = sup.filter_aplicable_doctor(main_dataframe, doctors_list_df)

sup.excel_generator(excel_data=main_dataframe, page_name="test")
