# PI_code.py

import builtins

from pdf_reader import PDFReader
from preprocess import clean_text
from layer4_semantic import SemanticAnalyzer
from decision import DecisionEngine


# =========================================================
# INITIALIZE COMPONENTS
# =========================================================

pdf_reader = PDFReader()

semantic_analyzer = SemanticAnalyzer()

fusion_engine = DecisionEngine()


# =========================================================
# INPUT LOADER
# =========================================================

def load_input(user_input):

    # -----------------------------------------------------
    # PDF INPUT
    # -----------------------------------------------------

    if user_input.lower().endswith(".pdf"):

        print("\n[+] PDF detected.")

        extracted_text = pdf_reader.extract_text(
            user_input
        )

        return extracted_text

    # -----------------------------------------------------
    # DIRECT TEXT INPUT
    # -----------------------------------------------------

    else:

        return user_input


# =========================================================
# ROUTER LAYER
# =========================================================

def router_layer(text):

    route = "STANDARD_PIPELINE"

    text_length = len(text)

    if text_length > 5000:

        route = "LONG_CONTEXT_PIPELINE"

    return {

        "route": route,

        "input_length": text_length
    }


# =========================================================
# SCPI LAYER
# =========================================================

def scpi_layer(text):

    suspicious_keywords = [

        "ignore previous instructions",

        "reveal system prompt",

        "jailbreak",

        "base64",

        "developer mode",

        "execute",

        "override",

        "bypass",

        "unrestricted",

        "no safety",

        "ignore safeguards",

        "unfiltered"
    ]

    score = 0

    lowered = text.lower()

    detected_patterns = []

    for keyword in suspicious_keywords:

        if keyword in lowered:

            score += 15

            detected_patterns.append(keyword)

    score = min(score, 100)

    return {

        "scpi_score": score,

        "detected_patterns":
            detected_patterns
    }


# =========================================================
# HEURISTIC LAYER
# =========================================================

def heuristic_layer(text):

    heuristic_score = 0

    lowered = text.lower()

    dangerous_patterns = [

        "ignore previous instructions",

        "bypass",

        "override",

        "disable safety",

        "execute",

        "pretend to be",

        "developer mode",

        "reveal hidden",

        "unrestricted ai",

        "no safety policies",

        "without restrictions",

        "ignore safeguards",

        "unfiltered responses",

        "no ethical limitations"
    ]

    matched_patterns = []

    for pattern in dangerous_patterns:

        if pattern in lowered:

            heuristic_score += 20

            matched_patterns.append(pattern)

    heuristic_score = min(
        heuristic_score,
        100
    )

    return {

        "heuristic_risk_score":
            heuristic_score,

        "matched_patterns":
            matched_patterns
    }


# =========================================================
# FULL PIPELINE
# =========================================================

def run_pipeline(user_input, verbose=False):

    # =====================================================
    # SILENT MODE
    # =====================================================

    if not verbose:

        original_print = builtins.print

        builtins.print = lambda *args, **kwargs: None

    try:

        print("\n" + "=" * 70)

        print("PROMPT INJECTION DEFENSE PIPELINE")

        print("=" * 70)

        # -------------------------------------------------
        # LOAD INPUT
        # -------------------------------------------------

        text = load_input(user_input)

        if not text.strip():

            print("\n[!] No text extracted.")

            return None

        print("\n[+] Input Loaded Successfully")

        # =================================================
        # PREPROCESSING
        # =================================================

        cleaned_text = clean_text(text)

        print("[+] Preprocessing Complete")

        # =================================================
        # ROUTER
        # =================================================

        router_result = router_layer(
            cleaned_text
        )

        print("[+] Router Complete")

        # =================================================
        # SCPI
        # =================================================

        scpi_result = scpi_layer(
            cleaned_text
        )

        print("[+] SCPI Analysis Complete")

        # =================================================
        # HEURISTIC
        # =================================================

        heuristic_result = heuristic_layer(
            cleaned_text
        )

        print("[+] Heuristic Analysis Complete")

        # =================================================
        # SEMANTIC
        # =================================================

        semantic_result = semantic_analyzer.analyze(
            cleaned_text
        )

        print("[+] Semantic Analysis Complete")

        # =================================================
        # DECISION FUSION
        # =================================================

        final_result = fusion_engine.fuse(

            semantic_result,

            heuristic_result,

            scpi_result
        )

        print("[+] Decision Fusion Complete")

        # =================================================
        # FINAL OUTPUT
        # =================================================

        print("\n" + "=" * 70)

        print("FINAL SECURITY DECISION")

        print("=" * 70)

        print(

            f"\nFinal Action : "
            f"{final_result['final_action']}"
        )

        print(

            f"Reason       : "
            f"{final_result['reason']}"
        )

        print(

            f"Risk Score   : "
            f"{final_result['final_risk_score']}"
        )

        print(

            f"Severity     : "
            f"{final_result['severity']}"
        )

        print(

            f"Stability    : "
            f"{final_result['system_stability']}"
        )

        print(

            f"Confidence   : "
            f"{final_result['confidence']}"
        )

        print(

            f"Categories   : "
            f"{final_result['attack_categories']}"
        )

        # =================================================
        # EXPLAINABILITY
        # =================================================

        print("\n" + "=" * 70)

        print("EXPLAINABILITY")

        print("=" * 70)

        for key, value in final_result[
            "explanation"
        ].items():

            print(f"{key}: {value}")

        # =================================================
        # RAW OUTPUTS
        # =================================================

        print("\n" + "=" * 70)

        print("RAW LAYER OUTPUTS")

        print("=" * 70)

        print("\nROUTER RESULT:")

        print(router_result)

        print("\nSCPI RESULT:")

        print(scpi_result)

        print("\nHEURISTIC RESULT:")

        print(heuristic_result)

        print("\nSEMANTIC RESULT:")

        print(semantic_result)

        # =================================================
        # RETURN RESULT
        # =================================================

        return final_result

    finally:

        # =================================================
        # RESTORE PRINT
        # =================================================

        if not verbose:

            builtins.print = original_print


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\nChoose Input Type:")

    print("\n1. Direct Text")

    print("2. PDF File")

    choice = input("\nEnter choice: ")

    # -----------------------------------------------------
    # DIRECT TEXT
    # -----------------------------------------------------

    if choice == "1":

        user_input = input(
            "\nEnter prompt:\n\n"
        )

    # -----------------------------------------------------
    # PDF INPUT
    # -----------------------------------------------------

    elif choice == "2":

        user_input = input(
            "\nEnter PDF path:\n\n"
        )

    else:

        print("\nInvalid choice.")

        exit()

    # -----------------------------------------------------
    # RUN SYSTEM
    # -----------------------------------------------------

    run_pipeline(user_input, verbose=True)
    