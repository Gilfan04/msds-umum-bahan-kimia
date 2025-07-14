import streamlit as st
import pandas as pd
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="Chemical Safety Data Sheet (SDS)",
    page_icon="⚠️",
    layout="wide"
)

# CSS untuk tampilan yang lebih baik
st.markdown("""
<style>
    .header { color: #FF4B4B; font-weight: 700; }
    .subheader { color: #0068C9; }
    .warning { background-color: #FFF3CD; padding: 10px; border-radius: 5px; }
    .danger { background-color: #F8D7DA; padding: 10px; border-radius: 5px; }
    .safe { background-color: #D4EDDA; padding: 10px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# ---- Database Bahan Kimia ----
@st.cache_data
def load_data():
    chemicals = pd.DataFrame([
        {
            "Nama": "Asam Sulfat (H₂SO₄)",
            "Rumus Kimia": "H₂SO₄",
            "Klasifikasi": "Korosif, Oksidator",
            "Bahaya": "Luka bakar kulit/gaung, iritasi pernapasan",
            "Penyimpanan": "Wadah kaca/polietilen, jauh dari logam & basa",
            "Penanganan": "Sarung tangan nitril, apron, kacamata",
            "Pertolongan Pertama": "Bilas dengan air 15 menit, bawa ke dokter",
            "Kode Warna": "Merah",
            "GHS": "https://www.osha.gov/sites/default/files/ghspictograms/Hazard_C.png"
        },
        {
            "Nama": "Natrium Hidroksida (NaOH)",
            "Rumus Kimia": "NaOH",
            "Klasifikasi": "Korosif",
            "Bahaya": "Luka bakar kulit, kerusakan mata permanen",
            "Penyimpanan": "Wadah plastik, tempat kering",
            "Penanganan": "Sarung tangan tahan bahan kimia, pelindung wajah",
            "Pertolongan Pertama": "Bilas kulit/mata, netralkan asam",
            "Kode Warna": "Merah",
            "GHS": "https://www.osha.gov/sites/default/files/ghspictograms/Hazard_C.png"
        },
        {
            "Nama": "Metanol (CH₃OH)",
            "Rumus Kimia": "CH₃OH",
            "Klasifikasi": "Mudah Terbakar, Beracun",
            "Bahaya": "Iritasi, kerusakan saraf optik",
            "Penyimpanan": "Area berventilasi, jauh dari api",
            "Penanganan": "Masker respirator, ventilasi memadai",
            "Pertolongan Pertama": "Udara segar, pencucian kulit",
            "Kode Warna": "Biru",
            "GHS": "https://www.osha.gov/sites/default/files/ghspictograms/Hazard_F.png"
        }
    ])
    return chemicals

chemical_db = load_data()

# ---- UI Aplikasi ----
st.title("📋 Chemical Safety Data Sheet (SDS)")
st.markdown("""
Aplikasi ini menyediakan informasi karakteristik dan prosedur keselamatan bahan kimia berdasarkan **Sistem Harmonisasi Global (GHS)**.
""")

# Sidebar untuk pencarian
with st.sidebar:
    st.header("🔍 Filter Bahan Kimia")
    search_term = st.text_input("Cari berdasarkan nama/rumus kimia:")
    hazard_class = st.multiselect(
        "Klasifikasi Bahaya:",
        options=["Korosif", "Mudah Terbakar", "Beracun", "Oksidator"],
        default=[]
    )
    
    st.divider()
    st.markdown("**Legenda Kode Warna:**")
    st.markdown("- 🟥 **Merah:** Bahan Korosif")
    st.markdown("- 🟦 **Biru:** Bahan Mudah Terbakar")
    st.markdown("- 🟩 **Hijau:** Bahan Relatif Aman")

# Filter data
filtered_data = chemical_db.copy()
if search_term:
    filtered_data = filtered_data[
        filtered_data["Nama"].str.contains(search_term, case=False) | 
        filtered_data["Rumus Kimia"].str.contains(search_term, case=False)
    ]
if hazard_class:
    filtered_data = filtered_data[
        filtered_data["Klasifikasi"].str.contains('|'.join(hazard_class))
    ]

# Tampilkan hasil
if len(filtered_data) == 0:
    st.warning("Tidak ditemukan bahan kimia yang sesuai dengan kriteria pencarian.")
else:
    for _, chem in filtered_data.iterrows():
        with st.expander(f"**{chem['Nama']}** ({chem['Rumus Kimia']})", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(chem["GHS"], width=150, caption="Piktogram GHS")
                st.metric("Kode Warna", chem["Kode Warna"])
            
            with col2:
                st.markdown(f"**Klasifikasi:** `{chem['Klasifikasi']}`")
                
                if "Korosif" in chem["Klasifikasi"]:
                    st.markdown(f"<div class='danger'>🚨 **Bahaya Utama:** {chem['Bahaya']}</div>", unsafe_allow_html=True)
                elif "Mudah Terbakar" in chem["Klasifikasi"]:
                    st.markdown(f"<div class='warning'>🔥 **Bahaya Utama:** {chem['Bahaya']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='safe'>🛡️ **Bahaya Utama:** {chem['Bahaya']}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"**🏚️ Penyimpanan:** {chem['Penyimpanan']}")
                st.markdown(f"**🧤 Penanganan Aman:** {chem['Penanganan']}")
                st.markdown(f"**🆘 Pertolongan Pertama:** {chem['Pertolongan Pertama']}")

# Fitur tambahan
st.divider()
with st.expander("📥 Download Template SDS"):
    st.markdown("Unduh template SDS kosong untuk bahan kimia baru:")
    template = pd.DataFrame(columns=list(chemical_db.columns)[:-2])
    csv = template.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download CSV Template",
        data=csv,
        file_name="sds_template.csv",
        mime="text/csv"
    )

# Menjalankan aplikasi
if __name__ == "__main__":
    st.write("**Aplikasi ini dibuat untuk tujuan edukasi keselamatan bahan kimia.**")

