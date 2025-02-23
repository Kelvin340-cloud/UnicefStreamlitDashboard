# Import necessary libraries.
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set the layout to wide mode
st.set_page_config(layout="wide")

# load the preprocessed Dataset
@st.cache_data # To store the results

def data():
    return pd.read_csv('processed_data.csv')

df = data()

# Creating a streamlit sidebar
st.sidebar.image('logo.png', use_container_width=True) # Logo
st.sidebar.title("Filter Options")

# Dropdown Menu to select comparison type
comparison_type = st.sidebar.radio("Select Comparison Type", ("Single Month", "Comparative Analysis"))

# Condition for the Single Month
if comparison_type == "Single Month":
    # Dropdown to select a month
    selected_month = st.sidebar.selectbox("Select a Month", df['Month'].unique())

    # Dropdown to select a category with an option for "All"
    categories = ['All'] + df['Category'].unique().tolist()
    selected_category = st.sidebar.selectbox("Select a Category", categories)

    # Filter the dataset by the selected month and category
    if selected_category == 'All':
        filtered_df = df[df['Month'] == selected_month]
    else:
        filtered_df = df[(df['Month'] == selected_month) & (df['Category'] == selected_category)]

    # Streamlit Dashboard for Single Month
    st.title("Media Data Trends Dashboard")
    st.subheader(f"Trends for {selected_month} - {selected_category}")

    # Set the style for the plots
    sns.set(style="whitegrid")

    # Define a custom sky blue color palette
    custom_palette = sns.color_palette(["tomato", "orange", "gold", "yellowgreen", "mediumseagreen"])


    # Create a 2x2 grid for the plots
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), constrained_layout=True)  # Make the platform wide

    # Plot 1: Count of stories per category
    category_count = filtered_df['Category'].value_counts()
    sns.barplot(x=category_count.index, y=category_count.values, ax=axes[0, 0], hue=category_count.index, palette=custom_palette)
    axes[0, 0].set_xlabel('Category', fontsize=12)
    axes[0, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].set_title('Number of Stories by Category', fontsize=14, loc='center')


    # Plot 2: Tonality distribution
    tonality_count = filtered_df['Tonality'].value_counts()
    tonality_colors = sns.color_palette("pastel")[0:len(tonality_count)]
    axes[0, 1].pie(tonality_count, labels=tonality_count.index, autopct='%1.1f%%', colors=tonality_colors, startangle=90, wedgeprops=dict(width=0.4))
    axes[0, 1].set(aspect='equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    axes[0, 1].set_title('Tonality Distribution', fontsize=14, loc='center')


    # Plot 3: Media Type Distribution
    media_type_count = filtered_df['Media Type'].value_counts()
    sns.barplot(x=media_type_count.index, y=media_type_count.values, ax=axes[1, 0], palette=custom_palette)
    axes[1, 0].set_xlabel('Media Type', fontsize=12)
    axes[1, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].set_title('Media Type Distribution', fontsize=14, loc='center')

    # Plot 4: Top 10 Themes
    top_themes = filtered_df['Theme'].value_counts().head(10)
    sns.barplot(x=top_themes.values, y=top_themes.index, ax=axes[1, 1], palette=custom_palette)
    axes[1, 1].set_xlabel('Number of Stories', fontsize=12)
    axes[1, 1].set_ylabel('Theme', fontsize=12)
    axes[1, 1].set_title('Top 10 Themes', fontsize=14, loc='center')

    # Adjust layout and show the plots
    st.pyplot(fig)


# Condition for the Comparative Analysis
elif comparison_type == "Comparative Analysis":
    # Dropdowns to select two months for comparison
    month1 = st.sidebar.selectbox("Select First Month", df['Month'].unique())
    month2 = st.sidebar.selectbox("Select Second Month", df['Month'].unique())

    # Filter the dataset by the selected months
    df_month1 = df[df['Month'] == month1]
    df_month2 = df[df['Month'] == month2]

    # Streamlit Dashboard for Comparative Analysis
    st.title("Comparative Media Data Trends Dashboard")
    st.subheader(f"Comparing {month1} and {month2}")

    # Set the style for the plots
    sns.set(style="whitegrid")

    # Define a custom sky blue color palette
    custom_palette = sns.color_palette(["tomato", "orange", "gold", "yellowgreen", "mediumseagreen"])

    # Create a 2x2 grid for the plots
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), constrained_layout=True)  # Make the platform wide

    # Plot 1: Count of stories per category for both months
    category_count1 = df_month1['Category'].value_counts()
    category_count2 = df_month2['Category'].value_counts()
    category_counts = pd.DataFrame({
        month1: category_count1,
        month2: category_count2
    }).fillna(0)
    category_counts.plot(kind='bar', ax=axes[0, 0], color=['tomato', 'mediumseagreen'])
    axes[0, 0].set_xlabel('Category', fontsize=12)
    axes[0, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 0].set_title('Number of Stories by Category', fontsize=14, loc='center')

    # Plot 2: Tonality distribution for both months
    tonality_count1 = df_month1['Tonality'].value_counts()
    tonality_count2 = df_month2['Tonality'].value_counts()
    tonality_counts = pd.DataFrame({
        month1: tonality_count1,
        month2: tonality_count2
    }).fillna(0)
    tonality_counts.plot(kind='bar', ax=axes[0, 1], color=['tomato', 'mediumseagreen'])
    axes[0, 1].set_xlabel('Tonality', fontsize=12)
    axes[0, 1].set_ylabel('Number of Stories', fontsize=12)
    axes[0, 1].set_title('Tonality Distribution', fontsize=14, loc='center')

    # Plot 3: Media Type Distribution for both months
    media_type_count1 = df_month1['Media Type'].value_counts()
    media_type_count2 = df_month2['Media Type'].value_counts()
    media_type_counts = pd.DataFrame({
        month1: media_type_count1,
        month2: media_type_count2
    }).fillna(0)
    media_type_counts.plot(kind='bar', ax=axes[1, 0], color=['tomato', 'mediumseagreen'])
    axes[1, 0].set_xlabel('Media Type', fontsize=12)
    axes[1, 0].set_ylabel('Number of Stories', fontsize=12)
    axes[1, 0].set_title('Media Type Distribution', fontsize=14, loc='center')

    # Plot 4: Top 10 Themes for both months
    top_themes1 = df_month1['Theme'].value_counts().head(10)
    top_themes2 = df_month2['Theme'].value_counts().head(10)
    top_themes = pd.DataFrame({
        month1: top_themes1,
        month2: top_themes2
    }).fillna(0)
    top_themes.plot(kind='barh', ax=axes[1, 1], color=['tomato', 'mediumseagreen'])
    axes[1, 1].set_xlabel('Number of Stories', fontsize=12)
    axes[1, 1].set_ylabel('Theme', fontsize=12)
    axes[1, 1].set_title('Top 10 Themes', fontsize=14, loc='center')

    # Adjust layout and show the plots
    st.pyplot(fig)

st.sidebar.image('mediawatch.png', use_container_width=True) 

# Add the footer logo and trademark statement at the bottom
#st.markdown("---")
#col1, col2 = st.columns([4, 1])  # Adjust column width for footer logo and trademark statement
#with col1:
    #st.image('mediawatch.png', use_column_width='auto', width=5)  # Replace 'footer_logo.png' with your footer logo file and adjust width as needed
#with col2:
    #st.markdown("**A Product of Farsight Africa**", unsafe_allow_html=True)