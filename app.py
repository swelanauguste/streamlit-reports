import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dishonoured Cheque Dashboard", page_icon=":bar_chart:", layout="wide"
)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    # @st.cache_resource
    def get_data():
        df = pd.read_csv(uploaded_file)
        return df


    df = get_data()

    st.sidebar.header("Please Filter Here:")
    paid = st.sidebar.multiselect(
        "Select the Paid Status:",
        options=df["IsPaid"].unique(),
        default=df["IsPaid"].unique(),
    )

    banks = st.sidebar.multiselect(
        "Select the Bank:",
        options=df["Bank"].unique(),
        default=df["Bank"].unique(),
    )

    payee = st.sidebar.multiselect(
        "Select the Payee:",
        options=df["Payee"].unique(),
        default=df["Payee"].unique(),
    )

    issuer = st.sidebar.multiselect(
        "Select the Issuer:",
        options=df["Issuer"].unique(),
        default=df["Issuer"].unique(),
    )


    reason = st.sidebar.multiselect(
        "Select the Dishonour Reason:",
        options=df["DishonourReason"].unique(),
        default=df["DishonourReason"].unique(),
    )

    df_selection = df.query(
        "IsPaid == @paid & Bank == @banks & Payee == @payee & DishonourReason == @reason & Issuer == @issuer"
    )


    st.title(":bar_chart: Dishonoured Cheque Dashboard")
    st.markdown("##")


    total_cheque_amount = int(df_selection["Amount"].sum())
    total_paid_amount = int(df_selection[df_selection["IsPaid"] == True]["Amount"].sum())

    lc, rc = st.columns(2)
    with lc:
        st.subheader("Total Cheques:")
        st.subheader(f"${total_cheque_amount:,.2f}")
    with rc:
        st.subheader("Total Paid Cheques:")
        st.subheader(f"${total_paid_amount:,.2f}")

    st.markdown("---------")
    total_issuers = df_selection.groupby("Issuer").sum()[['Amount']].sort_values(by="Amount", ascending=False)
    total_payees = df_selection.groupby("Payee").sum()[['Amount']].sort_values(by="Amount", ascending=False)
    total_banks = df_selection.groupby("Bank").sum()[['Amount']].sort_values(by="Amount", ascending=False)
    total_paid = df_selection.groupby("IsPaid").sum()[['Amount']].sort_values(by="Amount", ascending=False)
    
    first, second, third, forth = st.columns(4)
    
    with first:
        st.subheader("Issuers:")
        st.dataframe(total_issuers)
        
    with second:
        st.subheader("Payees:")
        st.dataframe(total_payees)
   
    with third:
        st.subheader("Banks:")
        st.dataframe(total_banks)
        
    with forth:
        st.subheader("Paid:")
        st.dataframe(total_paid)

    st.markdown("---------")
    st.dataframe(df_selection)

    fig_paid = px.pie(
        df_selection.groupby("IsPaid").sum()[['Amount']].sort_values(by="Amount", ascending=False),
        values="Amount",
        names=df_selection.groupby("IsPaid").sum()[['Amount']].sort_values(by="Amount", ascending=False).index,
        title="<b>IsPaids</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white",
    )
    
    st.plotly_chart(fig_paid)