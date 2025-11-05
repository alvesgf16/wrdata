# WRData

A Python-based data scraper and analyzer for League of Legends: Wild Rift champion statistics. WRData automatically collects, processes, and analyzes champion performance metrics across different lanes, providing tier rankings based on statistical analysis.

## 🎮 Features

- **Automated Data Collection**: Scrapes champion statistics from Wild Rift data sources using Selenium
- **Multi-Lane Analysis**: Processes champion data for all five lanes (Top, Jungle, Mid, Bot, Support)
- **Statistical Tiering**: Implements sophisticated algorithms to rank champions into performance tiers (S+, S, A, B, C)
- **Adjusted Metrics**: Calculates adjusted win rates based on pick rates and statistical distributions
- **Multiple Output Formats**: Exports data to Excel (.xlsx) and CSV formats
- **Outlier Detection**: Filters statistical outliers for more accurate tier assignments
- **Internationalization Support**: Built-in translation system for champion names and game terms

## 📋 Requirements

- Python 3.10 or higher
- Chrome/Chromium browser (for web scraping)

## 🚀 Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/alvesgf16/wrdata.git
cd wrdata
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install the package:
```bash
pip install -e .
```

For development with testing tools:
```bash
pip install -e ".[dev]"
```

## 💻 Usage

### Command Line Interface

Run the data collection and analysis:

```bash
wrdata
```

This command will:
1. Fetch current champion statistics from the data source
2. Process and analyze the data for each lane
3. Calculate adjusted win rates and assign tiers
4. Export results to `res/wrdata.xlsx` and `res/wrdata.csv`

### As a Python Module

```python
from wrdata.core.orchestrator import process_champions

# Process all champions and generate output files
process_champions()
```

## 📊 Output

The tool generates two output files in the `res/` directory:

- **wrdata.xlsx**: Excel file with formatted data and multiple sheets per lane
- **wrdata.csv**: CSV file with all champion data in a single table

Each champion entry includes:
- Champion name
- Lane
- Win rate
- Pick rate
- Ban rate
- Adjusted win rate
- Tier classification

## 🏗️ Project Structure

```
wrdata/
├── src/wrdata/
│   ├── adapters/          # Output adapters and writers
│   │   └── writers/       # CSV and XLSX writer implementations
│   ├── cli/               # Command-line interface
│   ├── config/            # Application settings
│   ├── core/              # Core orchestration logic
│   ├── data/              # Data fetching and models
│   │   ├── models/        # Champion and enum definitions
│   │   └── parsers/       # HTML parsing logic
│   ├── domain/            # Business logic (analysis, processing)
│   ├── i18n/              # Internationalization support
│   │   └── mappings/      # Translation mappings
│   └── exceptions.py      # Custom exceptions
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── pyproject.toml         # Project metadata and dependencies
└── requirements.txt       # Production dependencies
```

## 🧪 Testing

The project includes comprehensive test coverage with unit, integration, and end-to-end tests.

### Running Tests

The project is configured via `pytest.ini` to automatically include coverage reporting with branch tracking. Simply run:

```bash
python -m pytest
```

This automatically:
- Runs all tests with verbose output
- Measures code coverage with branch tracking
- Generates HTML, XML, and terminal coverage reports
- Shows missing lines in the terminal output

### Test Categories

Run specific test categories using markers:

```bash
# By test type
python -m pytest -m unit
python -m pytest -m integration
python -m pytest -m e2e

# Exclude slow tests
python -m pytest -m "not slow"
```

### Coverage Reports

After running tests, coverage reports are available:
- **Terminal**: Displayed automatically with missing lines
- **HTML**: Open `htmlcov/index.html` in your browser
- **XML**: `coverage.xml` for CI/CD integration

### Current Coverage

- **Overall**: 92% (448 statements, 413 covered)
- **Branch Coverage**: 90% (42 branches, 2 covered)
- Most modules at 100% coverage
- All critical paths tested

**Note**: Tests must be run using `python -m pytest` (not just `pytest`) to ensure proper module path resolution for imports.

## 🔧 Configuration

Key configuration options can be found in `src/wrdata/config/settings.py`:

### Scraping Configuration
- `source_url`: Data source URL
- `timeout`: Page load timeout (default: 10s)
- `headless`: Run browser in headless mode (default: True)
- `window_size`: Browser window dimensions

### Output Configuration
- `output_directory`: Output file directory (default: "res")
- `default_filename`: Base name for output files (default: "wrdata")
- `supported_formats`: Export formats (default: ["xlsx", "csv"])

### Analysis Configuration
- `number_of_tiers`: Number of tier classifications (default: 5)
- `tier_names`: Tier labels (default: ["S+", "S", "A", "B", "C"])

## 🤝 Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run code quality checks:
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## 📝 Algorithm Details

### Tiering System

The tier assignment algorithm:

1. **Win Rate Adjustment**: Calculates an adjustment factor based on pick rate to normalize performance metrics
2. **Outlier Filtering**: Uses statistical boundaries (mean ± 2σ) to remove extreme outliers
3. **Distribution Analysis**: Divides the remaining champions into performance tiers
4. **Final Assignment**: Assigns each champion to a tier based on their adjusted win rate

This approach ensures that high-performing champions with low pick rates (potentially niche picks) are not unfairly penalized, while popular champions are appropriately weighted.

## 🐛 Error Handling

The application uses custom exceptions for clear error reporting:

- `ScrapingError`: Issues during data collection
- `DataProcessingError`: Problems with data analysis
- `OutputError`: File writing failures

All errors are logged with detailed information for debugging.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Gabriel Alves**
- GitHub: [@alvesgf16](https://github.com/alvesgf16)

## 🙏 Acknowledgments

- Data sourced from League of Legends: Wild Rift official statistics
- Built with Selenium for robust web scraping
- Uses NumPy for statistical calculations

## ⚠️ Disclaimer

This tool is for educational and analytical purposes only. Please respect the terms of service of data sources and use responsibly.

---

**Note**: Wild Rift champion statistics and meta can change frequently with game updates. Run the tool regularly to maintain up-to-date tier lists.
