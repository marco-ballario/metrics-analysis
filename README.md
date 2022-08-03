# metrics-analysis

## Usage

To generate json data files:
```
python3 data-production.py
```
To generate static analysis graphs:
```
python3 static-analysis.py
```

## Graphs
- [Weighted Methods per Class (WMC)](#weighted-methods-per-class-wmc)
- [Magnitude (ABC)](#magnitude-abc)
- [Number of Public Methods (NPM)](#number-of-public-methods-npm)
- [Class Operation Accessibility (COA)](#class-operation-accessibility-coa)
- [Number of Public Attributes (NPA)](#number-of-public-attributes-npa)
- [Class Data Accessibility (CDA)](#class-data-accessibility-cda)
- [Size metrics comparison](#size-metrics-comparison)

### Weighted Methods per Class (WMC)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/wmc-static-analysis.png" width="100%"></div>

### Magnitude (ABC)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/abc-static-analysis.png" width="100%"></div>

### Number of Public Methods (NPM)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/npm-static-analysis.png" width="100%"></div>

### Class Operation Accessibility (COA)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/coa-static-analysis.png" width="100%"></div>

### Number of Public Attributes (NPA)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/npa-static-analysis.png" width="100%"></div>

### Class Data Accessibility (CDA)
Sum, minimum, maximum and average over a set of repository files.
<div align="center"><img src="./graphs/static-analysis/cda-static-analysis.png" width="100%"></div>

### Size metrics comparison
Compare ABC magnitude, Halstead estimated program length, PLOC and Cyclomatic Complexity metrics for a set of repositories.
<div align="center"><img src="./graphs/static-analysis/size-metrics-comparison.png" width="100%"></div>
