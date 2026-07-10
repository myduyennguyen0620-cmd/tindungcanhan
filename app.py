import streamlit as st

def main():
    st.set_page_config(page_title="Hệ thống Xét Duyệt Vay", layout="centered")
    st.title("🏦 Công Cụ Thẩm Định Vay Cá Nhân")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Thông tin khách hàng & Khoản vay")
        Tuoi = st.number_input("Tuổi khách hàng:", min_value=18, max_value=100, step=1, value=30)
        STV = st.number_input("Số tiền muốn vay (triệu đồng):", min_value=0.0, step=10.0, value=500.0)
        TGV = st.number_input("Thời gian muốn vay (số năm):", min_value=1.0, step=1.0, value=5.0)
        LSV = st.number_input("Lãi suất vay (VD: 0.1 cho 10%/năm):", min_value=0.0, format="%.3f", value=0.1)
        GTTSDB = st.number_input("Giá trị tài sản đảm bảo (triệu đồng):", min_value=0.0, step=50.0, value=1000.0)

    with col2:
        st.subheader("2. Thông tin tài chính")
        TN = st.number_input("Thu nhập 2 vợ chồng (triệu đồng/tháng):", min_value=0.0, step=5.0, value=30.0)
        SNTGD = st.number_input("Số người trong gia đình (người):", min_value=1, step=1, value=2)
        PTMC = st.number_input("Trả nợ khoản vay cũ (triệu đồng/tháng):", min_value=0.0, step=1.0, value=0.0)

    CPSH = 5  # Chi phí sinh hoạt (triệu/người/tháng)

    st.markdown("---")
    
    if st.button("🚀 XÉT DUYỆT HỒ SƠ", use_container_width=True):
        # Validate lỗi cơ bản
        if GTTSDB == 0:
            st.error("Lỗi: Giá trị tài sản đảm bảo phải lớn hơn 0.")
            return
            
        thu_nhap_con_lai = TN - (SNTGD * CPSH)
        if thu_nhap_con_lai <= 0:
            st.error("Lỗi: Thu nhập không đủ để trang trải chi phí sinh hoạt.")
            return

        # Tính toán các chỉ số
        LTV = STV / GTTSDB
        PTMM = (STV / (TGV * 12)) + (STV * (LSV / 12))
        DTI = (PTMC + PTMM) / thu_nhap_con_lai

        # Hiển thị chỉ số
        st.subheader("Kết quả chỉ số")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Chỉ số DTI (≤ 70%)", f"{DTI * 100:.1f}%")
        m_col2.metric("Chỉ số LTV (≤ 70%)", f"{LTV * 100:.1f}%")
        m_col3.metric("Tuổi (18 < Tuổi < 70)", f"{Tuoi}")

        # Logic Xét duyệt
        st.markdown("### Kết Luận")
        if DTI <= 0.7 and LTV <= 0.7 and 18 < Tuoi < 70:
            st.success("✅ KHÁCH HÀNG ĐƯỢC VAY")
        else:
            st.error("❌ KHÁCH HÀNG KHÔNG ĐƯỢC VAY")
            st.markdown("**Lý do từ chối:**")
            if DTI > 0.7:
                st.warning("- Tỷ lệ nợ trên thu nhập (DTI) vượt mức 70%.")
            if LTV > 0.7:
                st.warning("- Tỷ lệ khoản vay trên tài sản (LTV) vượt mức 70%.")
            if Tuoi <= 18 or Tuoi >= 70:
                st.warning("- Độ tuổi không nằm trong khung quy định (lớn hơn 18 và nhỏ hơn 70).")

if __name__ == "__main__":
    main()
