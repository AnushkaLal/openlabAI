# OpenLab AI 🔬
### An Agentic Data Science Team for Scientific Exploration

**OpenLab AI is a multi-agent, AI-assisted data science platform that turns raw datasets into structured, interpretable research reports.**

Powered by **Gemma 4 through Ollama**, OpenLab brings together specialized AI agents that collaborate on data quality assessment, research planning, statistical interpretation, and scientific peer review.

The goal is simple: make rigorous data analysis more accessible without treating AI-generated conclusions as unquestionable scientific facts.

---

## The Problem

Data is central to modern STEM research, but getting from a raw CSV to a defensible scientific conclusion requires several different skills.

Students and early-stage researchers often need to:

- Identify missing values, duplicates, unusual observations, and data-quality issues.
- Decide which statistical methods are appropriate for a research question.
- Interpret correlations and descriptive statistics correctly.
- Understand limitations and potential confounding variables.
- Produce a readable report with evidence, visualizations, and scientific caveats.

These tasks are often handled separately, making the analysis process difficult to follow and easy to get wrong.

**OpenLab AI brings these stages into one coordinated workflow.** Instead of asking a general-purpose chatbot to do everything, it assigns distinct responsibilities to specialized agents and grounds numerical conclusions in Python-computed results.

## How OpenLab AI Works

```text
                    Research Question
                            |
                            v
                       Input CSV
                            |
                            v
                 +---------------------+
                 |    Data Auditor     |
                 | Quality assessment  |
                 +---------------------+
                            |
                            v
                 +---------------------+
                 | Research Scientist  |
                 | Analysis planning   |
                 +---------------------+
                            |
                            v
                 +---------------------+
                 | Python Data Tools   |
                 | Statistics & plots  |
                 +---------------------+
                            |
                            v
                 +---------------------+
                 | Analysis Engineer   |
                 | Result interpretation|
                 +---------------------+
                            |
                            v
                 +---------------------+
                 |   Peer Reviewer     |
                 | Evidence & caveats   |
                 +---------------------+
                            |
                            v
                 +---------------------+
                 |   Research Report   |
                 | Markdown + visuals  |
                 +---------------------+
```

The agents work in sequence, with each role contributing a different perspective. Python remains responsible for the numerical calculations, and the final report brings the evidence, interpretations, review, and limitations together.

## The Specialized Agent Team

| Agent | Responsibility |
|---|---|
| **Data Auditor** | Explains data-quality risks based on measured audit results. |
| **Research Scientist** | Proposes an analysis plan aligned with the research question and available columns. |
| **Analysis Engineer** | Interprets computed statistics without inventing numerical results. |
| **Peer Reviewer** | Checks whether interpretations are supported by evidence and flags unsupported claims, confounding, and limitations. |

This separation of responsibilities makes the workflow easier to inspect and helps prevent one general-purpose prompt from being responsible for every stage of a scientific investigation.

The agents do not operate as independent sources of truth. They share a common evidence base, and their conclusions remain subject to human verification.

## Powered by Gemma 4

OpenLab AI uses **Gemma 4 via Ollama**, allowing the agent team to use an accessible model interface without requiring a separate model integration for every role.

The model is used for tasks that benefit from language understanding and scientific reasoning:

- Explaining measured data-quality issues.
- Developing research plans from natural-language questions.
- Translating statistical results into understandable interpretations.
- Reviewing conclusions for unsupported claims and scientific caveats.

Each agent receives a role-specific system prompt and the relevant structured context. Shared guardrails establish common expectations for evidence, uncertainty, and scientific language.

A language model can explain a correlation, but it should not be the authority on the numerical value of that correlation.

OpenLab separates the two responsibilities:

- **Python and scientific libraries:** calculate statistics, inspect the dataset, and generate plots.
- **Gemma 4:** interpret the measured evidence, suggest analytical approaches, and critique conclusions.

This hybrid design makes the output more inspectable than a workflow that asks an LLM to estimate or invent statistical results directly.

## Data Science Capabilities

The current implementation supports exploratory analysis of tabular CSV datasets.

### Data quality assessment

The audit measures:

- Number of rows and columns.
- Missing values and missing-value percentages.
- Duplicate rows.
- Data types and unique-value counts.
- Constant columns and potential high-cardinality columns.
- Potential numerical outliers using the interquartile-range method.

These are diagnostic signals, not automatic proof that a value is incorrect.

### Statistical analysis

Python computes:

- Descriptive statistics, including count, mean, standard deviation, quartiles, minimum, and maximum.
- Pearson correlations between eligible numerical column pairs.
- Correlation p-values and sample sizes.
- Correlation rankings based on absolute coefficient magnitude.

The current analysis is exploratory. Pearson correlation measures linear association and does not establish causation.

### Visual analysis

OpenLab generates visualizations to make patterns easier to investigate.

**Correlation matrix**

Shows pairwise correlations among numerical variables, making strong positive and negative associations easier to spot.

**Distribution plots**

Show the distributions of numerical variables, helping users inspect spread, skew, concentration, and potential anomalies.

These visuals complement the numerical results rather than replacing statistical interpretation.

## Scientific Guardrails

Scientific usefulness requires more than producing plausible-looking prose. OpenLab includes guardrails at the model-prompt and execution levels.

### 1. Evidence-grounded responses

Agents are instructed to use supplied evidence, avoid inventing measurements or computations, and acknowledge insufficient information.

### 2. Deterministic numerical authority

Statistical values are calculated by Python. Agents interpret those results instead of generating numerical findings from memory.

### 3. Correlation is not causation

Agents are explicitly instructed not to treat observational correlations as proof of causal relationships.

### 4. Role separation

Each agent has a defined responsibility. The auditor assesses data quality, the scientist plans, the analyst interprets, and the reviewer critiques.

### 5. Bounded model retries

Model requests have a limited number of attempts and request timeouts. A failing model call should not trigger an endless retry loop.

### 6. Explicit error reporting

Failed agent calls are recorded in an errors file and disclosed in the report. Critical failures, such as invalid input or failed computations, are reported separately.

A report completed with agent errors is marked as potentially incomplete.

### 7. No arbitrary AI-generated code execution

The current workflow uses predefined Python tools rather than executing arbitrary code generated by an agent. The model cannot independently modify the analysis pipeline through its response.

### 8. Human verification

The peer reviewer is advisory, not a guarantee of correctness. Reports should be checked against the underlying dataset, statistical assumptions, domain knowledge, and relevant literature before being used to support scientific conclusions.

These guardrails reduce certain failure modes; they do not eliminate model errors or establish scientific validity automatically.

## Example Use Case

Consider a student investigating:

> How are humidity and PM2.5 related in this dataset?

OpenLab can:

1. Audit the dataset for missing values and quality concerns.
2. Suggest an analysis plan using available variables.
3. Calculate descriptive statistics and numerical correlations.
4. Generate a correlation matrix and distribution plots.
5. Ask the analysis agent to interpret the measured relationship.
6. Ask the peer reviewer to flag unsupported claims and possible confounders.
7. Produce a structured Markdown report containing the evidence and limitations.

If rainfall is also associated with humidity and PM2.5, for example, the reviewer can flag it as a potential confounding variable. The current pipeline does not automatically establish whether rainfall explains the relationship; additional analysis would be required.

The same workflow can be applied to other CSV datasets, provided the research question is appropriate for the available variables and methods.

## Architecture and Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Language model | Gemma 4 | Language-based scientific reasoning |
| Model interface | Ollama | Model access and request handling |
| Programming language | Python | Pipeline orchestration and computation |
| Data processing | pandas, NumPy | Tabular data handling and numerical operations |
| Statistics | SciPy | Pearson correlation and statistical calculations |
| Visualizations | Matplotlib | Correlation matrices and distributions |
| Output format | Markdown and JSON | Reports, audit records, and computed results |
| Interface | Command-line CLI | Reproducible investigation runs |

## Project Structure

```text
openlab-ai/
├── data/
│   ├── air_quality.csv
│   └── penguins.csv
├── outputs/
│   ├── report_air_quality.md
│   ├── audit_air_quality.json
│   ├── analysis_air_quality.json
│   ├── errors_air_quality.json
│   └── plots_air_quality/
├── src/
│   └── openlab/
│       ├── agents/
│       │   ├── auditor.py
│       │   ├── scientist.py
│       │   ├── analyst.py
│       │   └── reviewer.py
│       ├── core/
│       │   └── llm.py
│       ├── tools/
│       │   ├── data_audit.py
│       │   ├── statistics.py
│       │   └── visualization.py
│       ├── reporting/
│       │   └── report.py
│       └── cli.py
├── requirements.txt
└── README.md
```

Dataset-specific filenames keep outputs from different datasets separate. Re-running an investigation with the same dataset name and output directory overwrites that dataset's previous outputs.

## Getting Started

### Prerequisites

- Python 3.10 or newer.
- [Ollama](https://ollama.com/download).
- Access to a Gemma 4 model supported by your Ollama installation.
- Git (optional).

### 1. Clone or open the project

```bash
git clone <repository-url>
cd openlab-ai
```

If you already have the project locally, navigate directly to its root directory.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gemma 4 through Ollama

Sign in to Ollama if required for your cloud model, then verify the exact model name available to your installation:

```bash
ollama list
ollama run gemma4:31b-cloud
```

The configured model name in `src/openlab/core/llm.py` must match the model identifier supported by your Ollama installation. The example above uses `gemma4:31b-cloud`; use the exact identifier shown by Ollama if it differs.

Keep the existing Ollama endpoint configured in the code unless you intentionally change the connection method.

### 4. Install dependencies

The `requirements.txt` file should contain:

```text
pandas
numpy
scipy
matplotlib
requests
```

### 5. Run an investigation

```bash
PYTHONPATH=src python -m openlab.cli investigate \
  data/air_quality.csv \
  --question "How are humidity and PM2.5 related in this dataset?"
```

To investigate another dataset:

```bash
PYTHONPATH=src python -m openlab.cli investigate \
  data/penguins.csv \
  --question "How are penguin body mass and flipper length related?"
```

### 6. Inspect the outputs

```bash
open outputs/report_air_quality.md
open outputs/plots_air_quality/correlation.png
cat outputs/audit_air_quality.json
cat outputs/analysis_air_quality.json
cat outputs/errors_air_quality.json
```

The generated report includes the research question, audit findings, analysis plan, computed results, agent interpretations, peer review, visualizations, limitations, and execution errors.

## From Student Analysis to Research Workflows

OpenLab is designed around a practical educational need: students should be able to investigate data, understand their analytical choices, and learn to question conclusions rather than simply accept generated answers.

Its specialized-agent architecture also provides a foundation for more demanding research workflows.

Potential future extensions include:

- Dataset-specific statistical tests and regression.
- Group-wise analysis and control for confounding variables.
- Reproducible experiment configurations and run histories.
- Research references and source verification.
- Human review checkpoints for sensitive or high-impact conclusions.
- Domain-specific agent teams for environmental science, biology, public health, and other STEM fields.

These are future directions, not claims about features already implemented. Scaling toward research use would require additional statistical validation, reproducibility controls, data governance, and domain-specific evaluation.

## Current Limitations

OpenLab is an exploratory analysis assistant, not an autonomous scientific discovery system.

- Input is currently focused on CSV datasets.
- Statistical analysis is primarily descriptive and correlation-based.
- Correlations are not automatically computed separately for each category or group.
- Potential confounders are flagged for investigation but are not automatically resolved.
- The peer-review verdict is generated by an LLM and is not independent scientific certification.
- The current workflow does not automatically revise an analysis based on reviewer feedback.
- Cloud model use sends the supplied prompt context to the configured cloud provider; sensitive data should be handled accordingly.
