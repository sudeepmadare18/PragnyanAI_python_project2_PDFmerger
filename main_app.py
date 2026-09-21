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
    "Upload multiple PDF files, view them individually, "
    "check their order, merge them, and download the result."
)

st.info(
    "Built with Python + Streamlit + PyPDF"
)


# ============================================================
# SESSION STATE
# ============================================================

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None

if "merged_filename" not in st.session_state:
    st.session_state.merged_filename = "merged_pdf.pdf"


# ============================================================
# FUNCTION — PDF VIEWER
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
# SECTION 1 — UPLOAD PDF FILES
# ============================================================

st.header("1. Upload PDF Files")

uploaded_files = st.file_uploader(
    "Select PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)


# ============================================================
# SECTION 2 — PDF ORDER
# ============================================================

if uploaded_files:

    st.divider()

    st.header("2. PDF Upload Order")

    st.write(
        "The PDFs below are arranged according to "
        "the order in which they appear in the uploaded file list."
    )

    for index, uploaded_file in enumerate(
        uploaded_files,
        start=1
    ):

        file_size = uploaded_file.size / 1024

        st.write(
            f"### {index}. {uploaded_file.name}"
        )

        st.caption(
            f"PDF {index} | "
            f"File Size: {file_size:.2f} KB"
        )


# ============================================================
# SECTION 3 — VIEW PDFs ONE BY ONE
# ============================================================

if uploaded_files:

    st.divider()

    st.header("3. View PDF Files One by One")

    st.write(
        "Select a PDF below to view its contents."
    )

    # Create names for dropdown
    pdf_options = []

    for index, uploaded_file in enumerate(
        uploaded_files,
        start=1
    ):

        pdf_options.append(
            f"PDF {index} - {uploaded_file.name}"
        )

    selected_pdf = st.selectbox(
        "Select PDF to View",
        pdf_options
    )

    # Find selected PDF
    selected_index = pdf_options.index(
        selected_pdf
    )

    selected_file = uploaded_files[
        selected_index
    ]

    st.subheader(
        f"Viewing PDF {selected_index + 1}: "
        f"{selected_file.name}"
    )

    # Display PDF
    display_pdf(selected_file)


# ============================================================
# SECTION 4 — MERGE PDF FILES
# ============================================================

if uploaded_files:

    st.divider()

    st.header("4. Merge PDF Files")

    st.write(
        "The PDFs will be merged in the following order:"
    )

    for index, uploaded_file in enumerate(
        uploaded_files,
        start=1
    ):

        st.write(
            f"**{index}.** {uploaded_file.name}"
        )

    st.write("")

    if st.button(
        "🔗 Merge PDF Files",
        type="primary",
        use_container_width=True
    ):

        if len(uploaded_files) < 2:

            st.warning(
                "⚠️ Please upload at least 2 PDF files."
            )

        else:

            try:

                # Create PDF writer
                pdf_writer = PdfWriter()

                # Add PDFs in upload order
                for uploaded_file in uploaded_files:

                    uploaded_file.seek(0)

                    pdf_reader = PdfReader(
                        uploaded_file
                    )

                    # Add every page
                    for page in pdf_reader.pages:

                        pdf_writer.add_page(page)

                # Create memory buffer
                output_buffer = io.BytesIO()

                # Write merged PDF
                pdf_writer.write(
                    output_buffer
                )

                pdf_writer.close()

                # Store merged PDF
                st.session_state.merged_pdf = (
                    output_buffer.getvalue()
                )

                st.session_state.merged_filename = (
                    "merged_pdf.pdf"
                )

                st.success(
                    f"✅ Successfully merged "
                    f"{len(uploaded_files)} PDF files!"
                )

            except Exception as e:

                st.session_state.merged_pdf = None

                st.error(
                    f"❌ Error while merging PDFs: {e}"
                )


# ============================================================
# SECTION 5 — MERGED PDF STATUS
# ============================================================

if st.session_state.merged_pdf:

    st.divider()

    st.header("5. Merged PDF Status")

    st.success(
        "✅ PDF files have been merged successfully."
    )

    merged_size = (
        len(st.session_state.merged_pdf) / 1024
    )

    st.write(
        f"**Output File:** "
        f"{st.session_state.merged_filename}"
    )

    st.write(
        f"**Merged File Size:** "
        f"{merged_size:.2f} KB"
    )

    st.write(
        "The merged PDF is ready to view and download."
    )


# ============================================================
# SECTION 6 — VIEW MERGED PDF
# ============================================================

if st.session_state.merged_pdf:

    st.divider()

    st.header("6. View Merged PDF")

    # Convert merged bytes to base64
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


# ============================================================
# SECTION 7 — DOWNLOAD MERGED PDF
# ============================================================

if st.session_state.merged_pdf:

    st.divider()

    st.header("7. Download Merged PDF")

    st.download_button(
        label="⬇️ Download Merged PDF",
        data=st.session_state.merged_pdf,
        file_name=st.session_state.merged_filename,
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
