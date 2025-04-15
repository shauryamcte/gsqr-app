# 📄 README.md — GSQR Vendor Clustering & Filter Explorer

https://gsqr-app-6dk9e2jeijbthcm4w73yxw.streamlit.app/


## 🚀 Overview
This Streamlit application enables data-driven vendor evaluation for GSQR (General Staff Qualitative Requirements) formulation. It allows users to upload a vendor matrix, automatically cluster vendors based on their capabilities, visualize them in 2D space using PCA, and interactively filter and analyze vendor data.

---

## 📦 Features
- 📁 Upload and visualize vendor response matrix (CSV)
- 📊 Cluster vendors using **KMeans clustering**
- 🧠 Encode categorical parameters using **OneHotEncoder**
- 📉 Visualize clusters using **PCA (Principal Component Analysis)**
- 🧾 Display filters shared by all vendors in each cluster
- 🔎 Interactive sidebar to **filter vendors by multiple parameters**
- 📥 Download a sample vendor matrix for reference
- 📋 Beautified Excel-like view of the filtered vendor matrix

---

## 📁 File Requirements
The uploaded CSV file (`Vendor_Response_Matrix.csv`) must be structured as:

| Parameter              | Vendor A | Vendor B | Vendor C |
|------------------------|----------|----------|----------|
| Encryption             | AES-128  | AES-256  | None     |
| Range                  | 10 km    | 5 km     | 3 km     |
| Battery Life           | 10 hrs   | 8 hrs     | 6 hrs     |

The application expects the first column to be titled `Parameter`, and subsequent columns to be vendor names.

---

## 🧠 Core Functions Explained

### `beautify_df(df)`
- Returns a styled Pandas DataFrame with alternating row colors, highlighted headers, and background gradients for visual polish.
- Used to visually enhance the appearance of the vendor matrix within the app.

### `OneHotEncoder(sparse_output=False)`
- Transforms categorical text values (e.g., `AES-256`) into binary numeric vectors.
- Ensures ML models like KMeans can process non-numeric data.

### `KMeans(n_clusters=n)`
- Clusters the encoded vendor data into `n` groups based on feature similarity.
- Each vendor is assigned a cluster number, shown in both the cluster filter section and PCA scatter plot.

### `PCA(n_components=2)`
- Reduces the high-dimensional OneHotEncoded data into 2 components for plotting.
- Used to create a 2D visual representation of how vendors group together.

---

## 📊 App Layout

### Left Column (`col1`):
- 🔍 Cluster-based filter discovery
- 📌 Expander showing which parameters are consistent across all vendors in each cluster
- 📈 PCA scatter plot of vendor clusters

### Right Column (`col2`):
- 🧾 Multi-filter dropdowns (Parameter + Value)
- ➕ Add/❌ Remove filters dynamically
- ✅ See filtered vendor matrix in a stylized, color-coded format

---

## 🧪 How to Use

1. **Start the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Upload your `Vendor_Response_Matrix.csv`** using the sidebar

3. **Adjust number of clusters** from the sidebar

4. **Analyze suggested GSQR filters** cluster-by-cluster

5. **Apply multiple filters** from the right panel to shortlist vendors

6. **Download the sample CSV** from the sidebar for formatting reference

---

## 📥 Sample Download Button
```python
with open("Vendor_Response_Matrix.csv", "rb") as file:
    st.sidebar.download_button(
        label="Download Sample CSV",
        data=file,
        file_name="Vendor_Response_Matrix.csv",
        mime="text/csv"
    )
```
---

## 📌 Requirements
Make sure to include this in your `requirements.txt`:
```txt
pandas
scikit-learn
streamlit
plotly
```

---

## 👨‍💻 Author
Built and deployed by **Shaurya Sood** ([@shauryamcte](https://github.com/shauryamcte))

For enhancements or integrations, raise an issue or PR.

---

## ✅ Example Use Case
This tool is ideal for:
- Defense procurement evaluators
- Internal RFP filter design
- AI-assisted GSQR formulation
- Pre-qualification matrix pruning

---

## 🛡️ Disclaimer
This tool is a decision-support system and does not enforce compliance with formal procurement policies. Always validate final selections independently.
