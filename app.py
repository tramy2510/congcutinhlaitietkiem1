import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính tiền lãi theo phương pháp lãi đơn hoặc lãi kép.")

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

loai_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# NÚT TÍNH
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("Kỳ hạn phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất năm chuyển sang số thập phân
    lai_suat_nam = lai_suat / 100

    # =========================
    # XÁC ĐỊNH SỐ KỲ
    # =========================
    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        so_ky = ky_han
        thoi_gian_moi_ky = 1
        lai_suat_ky = lai_suat_nam / 12
        don_vi = "tháng"

    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        so_ky = ky_han / 3
        thoi_gian_moi_ky = 3
        lai_suat_ky = lai_suat_nam / 4
        don_vi = "quý"

    else:
        so_ky = 1
        thoi_gian_moi_ky = ky_han
        lai_suat_ky = lai_suat_nam * ky_han / 12
        don_vi = "cuối kỳ"

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        # Tổng lãi trong toàn bộ kỳ hạn
        tong_lai = so_tien_gui * lai_suat_nam * ky_han / 12

        tong_goc_lai = so_tien_gui + tong_lai

        # Lãi định kỳ
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_nam / 12
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_nam / 4
            )

        else:
            tien_lai_dinh_ky = tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            # Lãi kép theo tháng
            lai_suat_ky = lai_suat_nam / 12

            tien_cuoi_ky = (
                so_tien_gui
                * (1 + lai_suat_ky) ** ky_han
            )

            tong_lai = tien_cuoi_ky - so_tien_gui

            # Tiền lãi của kỳ đầu tiên
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_ky
            )

        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            # Lãi kép theo quý
            lai_suat_ky = lai_suat_nam / 4

            so_quy = ky_han / 3

            tien_cuoi_ky = (
                so_tien_gui
                * (1 + lai_suat_ky) ** so_quy
            )

            tong_lai = tien_cuoi_ky - so_tien_gui

            # Tiền lãi của quý đầu tiên
            tien_lai_dinh_ky = (
                so_tien_gui * lai_suat_ky
            )

        else:

            # Lãi kép cuối kỳ
            lai_suat_ky = lai_suat_nam / 12

            tien_cuoi_ky = (
                so_tien_gui
                * (1 + lai_suat_ky) ** ky_han
            )

            tong_lai = tien_cuoi_ky - so_tien_gui

            tien_lai_dinh_ky = tong_lai

        tong_goc_lai = so_tien_gui + tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{tien_lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_lai:,.0f} VNĐ"
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            f"{tong_goc_lai:,.0f} VNĐ"
        )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.divider()

    st.subheader("📝 Thông tin khoản gửi")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Số tiền gửi:** {so_tien_gui:,.0f} VNĐ")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")

    with col2:
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức tính:** {loai_lai}")

    st.write(f"**Hình thức lãnh lãi:** {hinh_thuc_lanh}")

    # =========================
    # GIẢI THÍCH
    # =========================
    with st.expander("📚 Xem công thức tính"):

        if loai_lai == "Lãi đơn":
            st.markdown("""
            **Công thức lãi đơn:**

            `Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12`

            **Tổng tiền nhận được:**

            `Tổng = Tiền gốc + Tiền lãi`
            """)

        else:
            st.markdown("""
            **Công thức lãi kép:**

            `Tổng tiền = Tiền gốc × (1 + lãi suất kỳ) ^ số kỳ`

            **Tổng tiền lãi:**

            `Tổng lãi = Tổng tiền - Tiền gốc`
            """)

    st.success("✅ Đã tính toán thành công!")
