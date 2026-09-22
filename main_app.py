import io
import base64
import streamlit as st
from pypdf import PdfReader, PdfWriter


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PragyanAI - PDF Merger",
    page_icon="📄",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("PragyanAI - PDF Merger")

st.write(
    "Upload multiple PDF files, arrange their order, "
    "view them, merge them, and download the final PDF."
)

st.info(
    "Built with Python + Streamlit + PyPDF"
)


# ============================================================
# SESSION STATE
# ============================================================

if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = []

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None


# ============================================================
# FUNCTION — DISPLAY PDF
# ============================================================

def display_pdf(pdf_file):

    pdf_bytes = pdf_file.getvalue()

    base64_pdf = base64.b64encode(
        pdf_bytes
    ).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="500"
        type="application/pdf">
    </iframe>
    """

    st.markdown(
        pdf_display,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION 1 — UPLOAD PDF
# ============================================================

st.header("1. Upload PDF")

uploaded_files = st.file_uploader(
    "Select PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)


# ============================================================
# STORE UPLOADED FILES
# ============================================================

if uploaded_files:

    # Store uploaded files only when first uploaded
    if not st.session_state.pdf_files:

        st.session_state.pdf_files = uploaded_files

    else:

        # Check whether new files were uploaded
        old_names = [
            file.name
            for file in st.session_state.pdf_files
        ]

        new_names = [
            file.name
            for file in uploaded_files
        ]

        if old_names != new_names:

            st.session_state.pdf_files = uploaded_files

            # Reset merged PDF
            st.session_state.merged_pdf = None


# ============================================================
# SECTION 2 — ARRANGE FILE ORDER
# ============================================================

if st.session_state.pdf_files:

    st.divider()

    st.header("2. Arrange File Order")

    st.write(
        "Use the ⬆️ and ⬇️ buttons to arrange the PDF files "
        "before merging."
    )

    files = st.session_state.pdf_files

    for index in range(len(files)):

        file = files[index]

        col1, col2, col3, col4 = st.columns(
            [1, 5, 1, 1]
        )

        with col1:

            st.write(
                f"**{index + 1}**"
            )

        with col2:

            st.write(
                f"📄 **{file.name}**"
            )

        with col3:

            # Move UP
            if st.button(
                "⬆️",
                key=f"up_{index}",
                disabled=(index == 0)
            ):

                files[index], files[index - 1] = (
                    files[index - 1],
                    files[index]
                )

                st.session_state.pdf_files = files

                st.rerun()

        with col4:

            # Move DOWN
            if st.button(
                "⬇️",
                key=f"down_{index}",
                disabled=(index == len(files) - 1)
            ):

                files[index], files[index + 1] = (
                    files[index + 1],
                    files[index]
                )

                st.session_state.pdf_files = files

                st.rerun()


# ============================================================
# SECTION 3 — VIEW UPLOADED FILES
# ============================================================

if st.session_state.pdf_files:

    st.divider()

    st.header("3. View Uploaded Files")

    st.write(
        "Select a PDF file to view it."
    )

    files = st.session_state.pdf_files

    pdf_options = []

    for index, file in enumerate(
        files,
        start=1
    ):

        pdf_options.append(
            f"PDF {index} - {file.name}"
        )

    selected_pdf = st.selectbox(
        "Select PDF",
        pdf_options
    )

    selected_index = pdf_options.index(
        selected_pdf
    )

    selected_file = files[selected_index]

    st.subheader(
        f"PDF {selected_index + 1}: "
        f"{selected_file.name}"
    )

    display_pdf(selected_file)


# ============================================================
# SECTION 4 — MERGE PDF
# ============================================================

if st.session_state.pdf_files:

    st.divider()

    st.header("4. Merge PDF")

    st.write(
        "The PDFs will be merged according to the order "
        "you arranged above."
    )

    # Show final order
    for index, file in enumerate(
        st.session_state.pdf_files,
        start=1
    ):

        st.write(
            f"**{index}.** {file.name}"
        )

    if len(st.session_state.pdf_files) < 2:

        st.warning(
            "⚠️ Please upload at least 2 PDF files to merge."
        )

    else:

        if st.button(
            "🔗 Merge PDF Files",
            type="primary",
            use_container_width=True
        ):

            try:

                # Create PDF writer
                writer = PdfWriter()

                # Add PDFs according to arranged order
                for file in st.session_state.pdf_files:

                    file.seek(0)

                    reader = PdfReader(file)

                    for page in reader.pages:

                        writer.add_page(page)

                # Create output buffer
                output = io.BytesIO()

                writer.write(output)

                writer.close()

                # Store merged PDF
                st.session_state.merged_pdf = (
                    output.getvalue()
                )

                st.success(
                    "✅ PDF files merged successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Error while merging PDFs: {e}"
                )


# ============================================================
# SECTION 5 — MERGED PDF
# ============================================================

if st.session_state.merged_pdf:

    st.divider()

    st.header("5. Merged PDF")

    st.success(
        "✅ Your merged PDF is ready!"
    )

    # --------------------------------------------------------
    # VIEW MERGED PDF
    # --------------------------------------------------------

    st.subheader("View Merged PDF")

    merged_base64 = base64.b64encode(
        st.session_state.merged_pdf
    ).decode("utf-8")

    merged_pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{merged_base64}"
        width="100%"
        height="600"
        type="application/pdf">
    </iframe>
    """

    st.markdown(
        merged_pdf_display,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # DOWNLOAD MERGED PDF
    # --------------------------------------------------------

    st.download_button(
        label="⬇️ Download Merged PDF",
        data=st.session_state.merged_pdf,
        file_name="merged_pdf.pdf",
        mime="application/pdf",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PragyanAI | Python + Streamlit + PyPDF"
)
