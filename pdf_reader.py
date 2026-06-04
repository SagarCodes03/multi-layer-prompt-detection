# pdf_reader.py

import fitz


# =========================================================
# PDF READER
# =========================================================

class PDFReader:

    def __init__(self):

        pass


    # =====================================================
    # EXTRACT TEXT
    # =====================================================

    def extract_text(self, pdf_path):

        full_text = ""

        try:

            # ---------------------------------------------
            # OPEN PDF
            # ---------------------------------------------

            document = fitz.open(pdf_path)

            # ---------------------------------------------
            # READ ALL PAGES
            # ---------------------------------------------

            for page_number in range(len(document)):

                page = document.load_page(
                    page_number
                )

                text = page.get_text()

                full_text += text + "\n"

            # ---------------------------------------------
            # CLOSE DOCUMENT
            # ---------------------------------------------

            document.close()

            # ---------------------------------------------
            # CLEAN OUTPUT
            # ---------------------------------------------

            full_text = full_text.strip()

            return full_text

        except Exception as e:

            print(
                f"\nPDF Extraction Error: {e}"
            )

            return ""


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    reader = PDFReader()

    pdf_path = r"C:\Users\Sagar Gowda H\Downloads\demo_prompt_injection_samples.pdf"

    extracted_text = reader.extract_text(
        pdf_path
    )

    print("\n" + "=" * 70)

    print("EXTRACTED PDF TEXT")

    print("=" * 70)

    print(extracted_text)