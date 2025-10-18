# High-Performance Parameter Search System for Microwave Optimization in Magnetron Cavities

## Project Overview

This project aims to automatically optimize electromagnetic field distribution in microwave heating systems through surrogate modeling and global optimization techniques. The system integrates ANSYS HFSS electromagnetic simulation with machine learning methods to achieve efficient parameter search and optimization for uniform electromagnetic and thermal field distribution.

## Related Publications

This project has been published at the TAAI conference:
- **Paper Link**: [https://www.taai.org.tw/files/domestic/77/taai_tea_final.pdf](https://www.taai.org.tw/files/domestic/77/taai_tea_final.pdf)


### Key Features

- **Surrogate Model Optimization**: Efficient parameter search using hybrid Kriging (KRG) and KPLS models
- **Automated Simulation Workflow**: Integration with ANSYS HFSS for electromagnetic field simulation
- **Intelligent Sampling Strategy**: Combination of global, medium-range, and local sampling methods
- **Visualization Interface**: PyQt6-based graphical user interface
- **Real-time Monitoring**: Real-time progress tracking and trend visualization during optimization


## Project Structure

```
tea_v3/
├── four_ver/                    # Main execution version
│   ├── pyqt5.py                # PyQt6 GUI main program
│   ├── ui2model.py             # UI-model interface layer
│   ├── model.py                # Global optimization main program
│   ├── Surrogate_Model.py      # Surrogate model implementation
│   ├── AEDT_Auto.py            # ANSYS HFSS automation script
│   ├── Initial_sampling.py     # Initial sampling generation
│   ├── GenAI_init.py           # Model initialization and prediction
│   ├── heatmap.py              # Heatmap and electric field visualization
│   ├── analyze_data.py         # Data analysis and trend plots
│   ├── utils.py                # Utility functions
│   ├── superposition.py        # Field superposition calculation
│   ├── data_1004.txt           # Training dataset
│   ├── KRG_model.pkl           # Kriging model
│   ├── KPLS_model.pkl          # KPLS model
│   └── logo.png                # Project logo
│
├── third_ver/                   # Third version (includes demo)
│   ├── demo/                   # Executable demo version
│   │   ├── pyqt5.exe           # Packaged executable
│   │   ├── Data/               # Simulation data folder
│   │   ├── Heatmaps/           # Heatmap outputs
│   │   └── output_trend_plots/ # Trend plot outputs
│   ├── new_method/             # New method experiments
│   └── old_method/             # Old method reference
│
└── smt_testing/                 # SMT library testing
```

## System Requirements

### Software Requirements
- Python 3.8+
- ANSYS Electronics Desktop (HFSS)

### Python Packages
```
PyQt6
numpy
pandas
matplotlib
seaborn
scikit-learn
smt (Surrogate Modeling Toolbox)
```

## Installation



**Install Dependencies**
```bash
pip install PyQt6 numpy pandas matplotlib seaborn scikit-learn smt
```

**Configure ANSYS Path**
   - Ensure ANSYS HFSS is properly installed
   - Modify the path settings in `AEDT_Auto.py`

## Usage

### Method 1: GUI Interface (Recommended)

**Launch the Graphical Interface**
```bash
cd four_ver
python pyqt5.py
```



### Method 2: Command Line Execution

```bash
cd four_ver
python model.py -p <project_path> -d <dataset_name>
```

Parameter Description:
- `-p, --path`: Project root directory path
- `-d, --data`: Dataset filename (without extension)

## Core Functionality

### 1. Surrogate Model

The system employs a dual-model strategy:
- **KRG (Kriging)**: Gaussian process-based regression model
- **KPLS (Kriging with Partial Least Squares)**: Kriging model combined with dimensionality reduction

Both models predict in parallel, selecting the better parameter combination for actual simulation.

### 2. Sampling Strategy

- **Global Sampling**: Random sampling across the entire parameter space
- **Medium Sampling**: Sampling around the top 10 best samples
- **Local Sampling**: Fine-grained search around the top 5 best samples

Sampling strategies cycle through based on iteration count (5-round cycle).

### 3. Optimization Objective Function

Goal: Maximize average thermal field intensity while minimizing standard deviation of thermal field distribution for uniform heating.

### 4. ANSYS HFSS Automation

- Automatic microwave cavity model construction
- Dual waveport configuration
- Electromagnetic field simulation execution
- Electric field distribution data export

### 5. Field Superposition and Analysis

- Electric field superposition: Vector superposition of three microwave sources
- Thermal field conversion: Electric field to thermal field distribution
- Statistical analysis: Calculate mean and standard deviation
- Visualization: Generate heatmaps and trend plots

## Output Results

### 1. Numerical Output
- Electric field mean and standard deviation
- Thermal field mean and standard deviation
- Optimized best parameter combination
- Objective function value

### 2. Graphical Output
- **Electric Field Heatmap**: `Electric field_<id>.jpg`
- **Thermal Field Heatmap**: `Heat field_<id>.jpg`
- **Optimization Trend Plot**: `current_max_obj.png`

### 3. Data Files
- `data_1004.txt`: Complete training dataset
- `move_file.txt`: File management record
- `model_time.txt`: Model training time log
- `round_time.txt`: Execution time per round log

## Parameter Description

### Optimization Parameters (16 Dimensions)

| Parameter | Range | Description |
|-----------|-------|-------------|
| Phase 1-6 | 0-360° | Phase of each waveguide |
| Power 1-6 | 500-900W | Power of each waveguide |
| Position X1-X2 | -100-100mm | X-axis position of waveguides |
| Position Y1-Y2 | -100-100mm | Y-axis position of waveguides |

## Experimental Workflow

1. **Initial Sampling**: Generate initial dataset using LHS or random sampling (300 samples)
2. **Model Training**: Train KRG and KPLS models using initial data
3. **Iterative Optimization**:
   - Surrogate model predicts optimal parameters
   - ANSYS performs actual simulation
   - Update training dataset
   - Retrain models
   - Repeat steps (80 rounds)
4. **Result Analysis**: Generate heatmaps, trend plots, and statistical data


