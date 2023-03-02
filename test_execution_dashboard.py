import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set page title
st.set_page_config(page_title="Test Results Dashboard")

# Load test results data
test_results = pd.read_csv("test_results.csv", parse_dates=["Execution Date"])

# Display table
st.write(test_results)

# Calculate pass rate over time
pass_rate = (
    test_results.groupby(pd.Grouper(key="Execution Date", freq="D"))["Result"]
    .apply(lambda x: (x == "Pass").sum() / x.count())
    .reset_index()
    .rename(columns={"Result": "Pass Rate"})
)

# Display line chart
fig, ax = plt.subplots()
ax.plot(pass_rate["Execution Date"], pass_rate["Pass Rate"])
ax.set(title="Pass Rate Over Time", xlabel="Date", ylabel="Pass Rate")
st.pyplot(fig)

# Filter data based on date range selected by user
start_date, end_date = st.slider(
    "Select a date range",
    value=(test_results["Execution Date"].min().date(), test_results["Execution Date"].max().date()),
    min_value=test_results["Execution Date"].min().date(),
    max_value=test_results["Execution Date"].max().date(),
)

# Convert start_date and end_date to Timestamp objects
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# Filter data based on date range
filtered_test_results = test_results[(test_results["Execution Date"] >= start_date) & (test_results["Execution Date"] <= end_date)]

# Calculate total tests and number of tests passed
total_tests = filtered_test_results["Test Name"].nunique()
num_tests_passed = (filtered_test_results["Result"] == "Pass").sum()

# Calculate app health index
app_health_index = num_tests_passed / total_tests * 100

# Display app health index
st.write(f"App Health Index: {app_health_index:.2f}%")

# Display table of test results
st.write(filtered_test_results)

