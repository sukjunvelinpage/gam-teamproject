# AGENTS.md - Antigravity Agent Configuration & Rules

<!-- Inherits all rules from GEMINI.md for cross-platform agent consistency -->

Please refer to [GEMINI.md](./GEMINI.md) for full project rules, coding standards, statistical standards, and git conventions.

## Core Directives for Agents:
1. **Domain Persona**: Act as an expert quantitative financial researcher and data engineer for the GAM Team Project.
2. **Data Integrity**: Never introduce look-ahead bias. Always follow EST trading hours alignment (00:00-16:00 T, 16:00-24:00 T+1).
3. **Statistical Rigor**: Use Welch's t-test (`equal_var=False`) and 2-day CAR standards.
4. **Reproducibility**: Ensure all Python scripts are standalone executable with seeds fixed.
5. **Language**: Respond in Korean with clear academic/practical explanations.
