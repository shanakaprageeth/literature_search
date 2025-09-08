# Copilot Instructions for prisma_search

- Follow the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology for all literature review features.
- Allow user input for research topic or keywords. If only topic is provided, implement keyword extraction.
- Accept and store initial PRISMA-related values (e.g., inclusion/exclusion criteria, databases, date ranges).
- Output must include:
  - PRISMA method data for literature review methods section
  - CSV export of selected publication list
- If manual abstract review is required, notify the user and provide clear guidelines and methodology text for inclusion in the literature review.
- Ensure all code is modular, well-documented, and user-friendly.
- Use clear prompts and error messages for user interactions.
