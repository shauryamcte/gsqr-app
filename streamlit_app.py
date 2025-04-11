import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🔍 GSQR Vendor Clustering & Enhanced Excel View")

uploaded_file = st.sidebar.file_uploader("Upload Vendor Response Matrix (.csv)", type=["csv"])

def beautify_df(df):
    styles = [
        {'selector': 'th', 'props': [('font-weight', 'bold'), ('background-color', '#e8f0fe')]},
        {'selector': 'td', 'props': [('border', '1px solid lightgrey'), ('padding', '5px')]},
        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f9f9f9')]},
        {'selector': 'tr:hover', 'props': [('background-color', '#d6eaff')]}
    ]
    return df.style        .set_table_styles(styles)        .set_properties(**{'text-align': 'left'})        .highlight_null(null_color='lightgrey')        .background_gradient(axis=None, cmap='Blues')        .format(na_rep='–')

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df_t = df.set_index("Parameter").T
    df_t.index.name = "Vendor"

    # Clustering logic
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(df_t)
    encoded_df = pd.DataFrame(encoded, index=df_t.index, columns=encoder.get_feature_names_out(df_t.columns))

    n_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=4)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(encoded_df)
    encoded_df["Cluster"] = labels

    # Analyze clusters
    cluster_outputs = []
    for cluster_id in range(n_clusters):
        members = encoded_df[encoded_df["Cluster"] == cluster_id].index.tolist()
        cluster_df = df_t.loc[members]
        filters = {
            f"{i+1}. {col}": cluster_df[col].iloc[0]
            for i, col in enumerate(cluster_df.columns)
            if cluster_df[col].nunique() == 1
        }
        cluster_outputs.append({
            "Cluster": cluster_id,
            "Vendors": members,
            "Filters": filters
        })

    # Layout
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("📊 Cluster Results & GSQR Filters")
        for result in cluster_outputs:
            with st.expander(f"Cluster {result['Cluster']} - Vendors: {', '.join(result['Vendors'])}"):
                for param, val in result["Filters"].items():
                    st.markdown(f"**{param}**: {val}")

        # PCA plot
        st.subheader("📈 Cluster Visualization (PCA)")
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(encoded_df.drop(columns=["Cluster"]))
        encoded_df["PCA1"] = pca_data[:, 0]
        encoded_df["PCA2"] = pca_data[:, 1]
        fig = px.scatter(encoded_df, x="PCA1", y="PCA2", color=encoded_df["Cluster"].astype(str),
                         hover_name=encoded_df.index, title="Vendor Cluster Scatter")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📄 Filter Vendor Matrix by Multiple Parameters")

        if "filters" not in st.session_state:
            st.session_state.filters = []

        if st.button("➕ Add Filter"):
            st.session_state.filters.append({"param": None, "value": None})

        for i, f in enumerate(st.session_state.filters):
            with st.container():
                cols = st.columns([1.2, 2, 0.5])
                serial_params = [f"{j+1}. {col}" for j, col in enumerate(df["Parameter"].unique())]
                param_map = dict(zip(serial_params, df["Parameter"].unique()))
                rev_param_map = {v: k for k, v in param_map.items()}

                selected_param = cols[0].selectbox(
                    f"Parameter {i+1}", serial_params,
                    index=serial_params.index(rev_param_map[f["param"]]) if f["param"] else 0,
                    key=f"param_{i}"
                )
                actual_param = param_map[selected_param]
                f["param"] = actual_param

                possible_values = sorted(df_t[actual_param].dropna().unique())
                f["value"] = cols[1].selectbox(
                    f"Value {i+1}", possible_values,
                    index=possible_values.index(f["value"]) if f["value"] in possible_values else 0,
                    key=f"value_{i}"
                )

                if cols[2].button("❌", key=f"remove_{i}"):
                    st.session_state.filters.pop(i)
                    st.experimental_rerun()

        filtered_df = df_t.copy()
        if st.session_state.filters:
            for f in st.session_state.filters:
                if f["param"] and f["value"] is not None:
                    filtered_df = filtered_df[filtered_df[f["param"]] == f["value"]]
            st.markdown("### ✅ Filtered Vendor Matrix:")
            st.dataframe(beautify_df(filtered_df), use_container_width=True)
        else:
            st.markdown("### 🧾 All Vendors (No Filters Applied):")
            st.write(beautify_df(df_t))


else:
    st.info("Please upload a CSV file to begin.")
