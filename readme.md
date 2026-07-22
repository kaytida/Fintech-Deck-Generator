# DeckGen AI — Autonomous Presentation Engine

A Streamlit-powered application for AI-driven presentation generation from enterprise financial data.

## Features

- 📊 Interactive financial data explorer
- 💰 Budget vs. Actual variance analysis
- 🎯 Quarter-over-quarter comparisons
- 📈 Real-time data visualizations with Plotly
- 📥 CSV data export functionality

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/
│   ├── q1.csv            # Q1 financial data
│   └── q2.csv            # Q2 financial data
├── css/
│   └── styles.css        # Original HTML styling (reference)
├── js/
│   ├── app.js            # Original JS logic (reference)
│   └── dataLoader.js     # Original data loader (reference)
├── index.html            # Original HTML version (archived)
└── readme.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone/Navigate to the project:**
```bash
cd d:\Fintech-Deck-Generator
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`

## Usage

### Home Tab
- Overview of DeckGen AI's problem statement and solution
- Key benefits and workflow steps
- Quick navigation to the Demo

### Demo Tab
- **Filters**: Select Quarter, Department, and Category
- **Metrics**: View total budget, actual spending, variance, and overrun count
- **Visualizations**: 
  - Budget vs Actual comparison charts
  - Variance distribution analysis
- **Data Export**: Download filtered data as CSV

## Data Format

The CSV files in the `data/` directory should have the following columns:

```
quarter,department,category,budget_usd,actual_usd
```

Example:
```
Q1,Engineering,Software Infrastructure,420000,435000
Q1,Engineering,Cloud Compute,380000,372000
```

## Customization

### Adding More Quarters
Simply add new CSV files to the `data/` directory with the same format. They'll be automatically loaded by the app.

### Styling
- Streamlit uses its built-in theming system (see inline CSS in `app.py`)
- Plotly charts use the `plotly_dark` template for consistency
- Colors can be customized in the CSS section at the top of `app.py`

## Technology Stack

- **Streamlit** — Web framework for data apps
- **Pandas** — Data manipulation and analysis
- **Plotly** — Interactive visualizations
- **Python** — Core language

## Original Version

The original HTML/CSS/JavaScript version is preserved in:
- `index.html` — Original web UI
- `css/styles.css` — Original styling
- `js/app.js` — Tab navigation logic
- `js/dataLoader.js` — Data loading utilities

## Future Enhancements

- [ ] PowerPoint deck generation (python-pptx integration)
- [ ] LLM-powered narrative generation
- [ ] More advanced forecasting and trend analysis
- [ ] Multi-file upload for dynamic data
- [ ] Real database connectivity
- [ ] User authentication and role-based access

## License

Hackathon Prototype © 2024
