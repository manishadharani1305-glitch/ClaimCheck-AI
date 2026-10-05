import streamlit as st
import re
from PIL import Image
from ocr import extract_text_from_image
from llm import verify_claims


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ClaimCheck AI",
    page_icon="🔍",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "claim_text" not in st.session_state:
    st.session_state.claim_text = ""

if "reference_text" not in st.session_state:
    st.session_state.reference_text = ""

if "verification_result" not in st.session_state:
    st.session_state.verification_result = ""

if "ocr_completed" not in st.session_state:
    st.session_state.ocr_completed = False


# ============================================================
# FUNCTION: CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    text = text.replace(
        "**",
        ""
    )

    return text.strip()


# ============================================================
# FUNCTION: DISPLAY VERIFICATION REPORT
# ============================================================

def display_verification_report(result):

    claims = re.findall(
        r"(?:^|\n)\s*CLAIM\s+\d+\s*\n(.*?)(?=\n\s*CLAIM\s+\d+\s*\n|\n\s*SUMMARY\b|$)",
        result,
        flags=re.IGNORECASE | re.DOTALL
    )

    supported = 0
    contradicted = 0
    unverified = 0

    st.markdown(
        "### 🔎 Detailed Claim Analysis"
    )

    if not claims:

        st.warning(
            "⚠️ The AI response could not be formatted correctly."
        )

        st.markdown(
            "### 🤖 AI Response"
        )

        st.text(result)

        return

    # ========================================================
    # DISPLAY EACH CLAIM
    # ========================================================

    for index, claim_block in enumerate(
        claims,
        start=1
    ):

        claim_block = claim_block.strip()

        # ----------------------------------------------------
        # FIND STATUS
        # ----------------------------------------------------

        status_match = re.search(
            r"Status\s*:\s*"
            r"(SUPPORTED|CONTRADICTED|UNVERIFIED)",
            claim_block,
            flags=re.IGNORECASE
        )

        if status_match:

            status = status_match.group(1).upper()

        else:

            status = "UNVERIFIED"

        # ----------------------------------------------------
        # FIND CLAIM
        # ----------------------------------------------------

        claim_match = re.search(
            r"Claim\s*:\s*"
            r"(.*?)(?=\n\s*Status\s*:)",
            claim_block,
            flags=re.IGNORECASE | re.DOTALL
        )

        if claim_match:

            claim_text = clean_text(
                claim_match.group(1)
            )

        else:

            claim_text = "Claim information unavailable"

        # ----------------------------------------------------
        # FIND EVIDENCE
        # ----------------------------------------------------

        evidence_match = re.search(
            r"Evidence\s*:\s*"
            r"(.*?)(?=\n\s*Explanation\s*:)",
            claim_block,
            flags=re.IGNORECASE | re.DOTALL
        )

        if evidence_match:

            evidence = clean_text(
                evidence_match.group(1)
            )

        else:

            evidence = "No evidence provided"

        # ----------------------------------------------------
        # FIND EXPLANATION
        # ----------------------------------------------------

        explanation_match = re.search(
            r"Explanation\s*:\s*(.*)",
            claim_block,
            flags=re.IGNORECASE | re.DOTALL
        )

        if explanation_match:

            explanation = clean_text(
                explanation_match.group(1)
            )

        else:

            explanation = "No explanation provided"

        # ====================================================
        # SUPPORTED
        # ====================================================

        if status == "SUPPORTED":

            supported += 1

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### ✅ Claim {index} — SUPPORTED"
                )

                st.markdown(
                    f"**Claim:** {claim_text}"
                )

                st.markdown(
                    f"**Evidence from Reference:** {evidence}"
                )

                st.markdown(
                    f"**Explanation:** {explanation}"
                )

        # ====================================================
        # CONTRADICTED
        # ====================================================

        elif status == "CONTRADICTED":

            contradicted += 1

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### ❌ Claim {index} — CONTRADICTED"
                )

                st.markdown(
                    f"**Claim:** {claim_text}"
                )

                st.markdown(
                    f"**Evidence from Reference:** {evidence}"
                )

                st.markdown(
                    f"**Explanation:** {explanation}"
                )

        # ====================================================
        # UNVERIFIED
        # ====================================================

        else:

            unverified += 1

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### ⚠️ Claim {index} — UNVERIFIED"
                )

                st.markdown(
                    f"**Claim:** {claim_text}"
                )

                st.markdown(
                    f"**Evidence from Reference:** {evidence}"
                )

                st.markdown(
                    f"**Explanation:** {explanation}"
                )

    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    st.markdown(
        "### 📈 Verification Summary"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "✅ Supported",
            supported
        )

    with col2:

        st.metric(
            "❌ Contradicted",
            contradicted
        )

    with col3:

        st.metric(
            "⚠️ Unverified",
            unverified
        )

    total_claims = (
        supported
        + contradicted
        + unverified
    )

    st.markdown(
        f"**📌 Total Claims Analyzed: {total_claims}**"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🔍 ClaimCheck AI"
)

st.subheader(
    "OCR & LLM-Based Document Claim Verification System"
)

st.write(
    "Upload a claim document and a reference document. "
    "ClaimCheck AI extracts the text using OCR and "
    "verifies the claims using an AI language model."
)


st.divider()


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.markdown(
    "## 📂 Upload Documents"
)

col1, col2 = st.columns(2)


# ============================================================
# CLAIM DOCUMENT
# ============================================================

with col1:

    st.markdown(
        "### 📄 Claim Document"
    )

    claim_file = st.file_uploader(
        "Upload the document containing the claim",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        key="claim"
    )


# ============================================================
# REFERENCE DOCUMENT
# ============================================================

with col2:

    st.markdown(
        "### 📚 Reference Document"
    )

    reference_file = st.file_uploader(
        "Upload the reference/evidence document",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        key="reference"
    )


# ============================================================
# CHECK DOCUMENTS
# ============================================================

documents_uploaded = (
    claim_file is not None
    and reference_file is not None
)


# ============================================================
# DISPLAY UPLOADED DOCUMENTS
# ============================================================

if documents_uploaded:

    st.divider()

    st.markdown(
        "## 📑 Uploaded Documents"
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # CLAIM IMAGE
    # --------------------------------------------------------

    with col1:

        claim_image = Image.open(
            claim_file
        )

        st.image(
            claim_image,
            caption="Claim Document",
            use_container_width=True
        )

    # --------------------------------------------------------
    # REFERENCE IMAGE
    # --------------------------------------------------------

    with col2:

        reference_image = Image.open(
            reference_file
        )

        st.image(
            reference_image,
            caption="Reference Document",
            use_container_width=True
        )


    st.divider()


    # ========================================================
    # OCR BUTTON
    # ========================================================

    st.markdown(
        "## 🔍 Step 1 — Extract Document Text"
    )

    if st.button(
        "🔍 Extract Text from Documents",
        use_container_width=True
    ):

        with st.spinner(
            "🔍 Extracting text using OCR..."
        ):

            try:

                # Extract Claim Document text

                claim_text = extract_text_from_image(
                    claim_image
                )


                # Extract Reference Document text

                reference_text = extract_text_from_image(
                    reference_image
                )


                # Save Claim OCR text

                if claim_text:

                    st.session_state.claim_text = (
                        claim_text.strip()
                    )

                else:

                    st.session_state.claim_text = ""


                # Save Reference OCR text

                if reference_text:

                    st.session_state.reference_text = (
                        reference_text.strip()
                    )

                else:

                    st.session_state.reference_text = ""


                # Clear previous AI result

                st.session_state.verification_result = ""


                # ====================================================
                # CHECK CLAIM OCR
                # ====================================================

                if st.session_state.claim_text:

                    st.success(
                        "✅ Claim Document OCR completed successfully!"
                    )

                else:

                    st.error(
                        "❌ No text detected in the Claim Document."
                    )


                # ====================================================
                # CHECK REFERENCE OCR
                # ====================================================

                if st.session_state.reference_text:

                    st.success(
                        "✅ Reference Document OCR completed successfully!"
                    )

                else:

                    st.error(
                        "❌ No text detected in the Reference Document."
                    )


                # ====================================================
                # FINAL OCR CHECK
                # ====================================================

                if (
                    st.session_state.claim_text
                    and st.session_state.reference_text
                ):

                    st.session_state.ocr_completed = True

                    st.success(
                        "🎉 OCR extraction completed successfully! "
                        "Both documents are ready for AI verification."
                    )

                else:

                    st.session_state.ocr_completed = False


            except Exception as e:

                st.session_state.ocr_completed = False

                st.error(
                    "❌ OCR extraction failed."
                )

                st.exception(e)


# ============================================================
# DISPLAY EXTRACTED TEXT
# ============================================================

if (
    st.session_state.ocr_completed
    and st.session_state.claim_text
    and st.session_state.reference_text
):

    st.divider()

    st.markdown(
        "## 📝 Extracted Document Text"
    )

    col1, col2 = st.columns(2)


    # ========================================================
    # CLAIM OCR TEXT
    # ========================================================

    with col1:

        st.markdown(
            "### 📄 Claim Document Text"
        )

        st.text_area(
            "Extracted Claim Text",
            value=st.session_state.claim_text,
            height=350,
            key="claim_display"
        )


    # ========================================================
    # REFERENCE OCR TEXT
    # ========================================================

    with col2:

        st.markdown(
            "### 📚 Reference Document Text"
        )

        st.text_area(
            "Extracted Reference Text",
            value=st.session_state.reference_text,
            height=350,
            key="reference_display"
        )


    st.divider()


    # ========================================================
    # AI VERIFICATION
    # ========================================================

    st.markdown(
        "## 🧠 Step 2 — AI Claim Verification"
    )

    st.write(
        "The AI compares the claims from the claim document "
        "with the information available in the reference "
        "document."
    )


    if st.button(
        "🧠 Start Verification",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 AI is analyzing the claims..."
        ):

            try:

                result = verify_claims(
                    st.session_state.claim_text,
                    st.session_state.reference_text
                )

                st.session_state.verification_result = (
                    result
                )

                st.success(
                    "🎉 AI verification completed successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ AI verification failed."
                )

                st.exception(e)


# ============================================================
# VERIFICATION REPORT
# ============================================================

if st.session_state.verification_result:

    st.divider()

    st.markdown(
        "## 📊 Verification Report"
    )

    display_verification_report(
        st.session_state.verification_result
    )


# ============================================================
# NEW VERIFICATION
# ============================================================

if (
    st.session_state.ocr_completed
    or st.session_state.verification_result
):

    st.divider()

    if st.button(
        "🔄 Start New Verification",
        use_container_width=True
    ):

        st.session_state.claim_text = ""

        st.session_state.reference_text = ""

        st.session_state.verification_result = ""

        st.session_state.ocr_completed = False

        st.rerun()


# ============================================================
# INITIAL MESSAGE
# ============================================================

if not documents_uploaded:

    st.info(
        "👆 Upload both the Claim Document and "
        "Reference Document to begin verification."
    )