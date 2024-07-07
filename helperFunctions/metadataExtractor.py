import os

from .functionsForExtraction import (
    areas_of_law_extraction,
    court_extraction,
    judges_extraction,
    legal_representation_extraction,
    lex_citation_extraction,
    originating_court_extraction,
    other_citations_extraction,
    parties_extractor,
    suit_number_extraction,
    year_of_judgement,
)
from .usefulVariables.regex import apex_courts


async def MetadataProcessor(doc_path, text):
    metadata = {}

    # Extract CASE TITLE
    metadata["case_title"] = os.path.basename(doc_path).replace(
        os.path.splitext(doc_path)[1], ""
    )

    # PARTIES EXTRACTION
    parties_extractor(text, metadata)
    # Extract COURT
    court_extraction(text, metadata)

    # Extract DATE and YEAR
    year_of_judgement(text, metadata)

    # SUIT NUMBER EXTRACTION
    suit_number_extraction(text, metadata)
    # Extract Citation
    lex_citation_extraction(text, metadata)
    # Other citation numbers
    other_citations_extraction(text, metadata)

    # Extract AREAS OF LAW
    areas_of_law_extraction(text, metadata)

    # Semantic tags
    metadata["semantic_tags_0"] = "Caselaw"
    metadata["semantic_tags_1"] = "legal document"
    metadata["semantic_tags_2"] = "Case"
    if metadata["court"] in apex_courts:
        metadata["semantic-tags_3"] = "high_profile_case"

    # JUDGES EXTRACTIONS
    judges_extraction(text, metadata)

    # Extract LEGAL REPRESENTATION
    legal_representation_extraction(text, metadata)

    # ORIGINATING COURTS
    originating_court_extraction(text, metadata)
    # Generate unique doc_id
    metadata["doc_id"] = os.path.basename(doc_path).replace(
        os.path.splitext(doc_path)[1], ""
    )

    # Set doctype to "case"
    metadata["doctype"] = "case"

    return metadata
