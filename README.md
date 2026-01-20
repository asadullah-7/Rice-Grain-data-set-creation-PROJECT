# 🌾 Rice Grain Variety Dataset Creation
This repository contains an automated pipeline for creating a high-quality dataset of rice grain varieties. The system segments individual grains from raw images, performs real-world scale calibration, and extracts essential morphological and color features.

# 📌 Project Overview
The goal of this project is to build a structured dataset of 15 different rice varieties for a variety identification system.

Roll No: L1F23BSCS0225

Toolbox: Python (Scikit-image, NumPy, Pandas)

Constraint: No OpenCV was used as per project requirements.

# 📂 Folder Structure
The script expects the following directory layout:

Plaintext

/Project_Root
├── CODE/
│   └── main_script.py            # The main processing script
├── Grain_Images/                 # Output: Individual cropped grains
├── Rejected/                     # Output: Images with detection issues
├── rice_metadata_final.csv       # Output: Extracted features in CSV
└── Variety_Folders/              # Input: Original images (e.g., Basmati, SuperKainat)
# 🛠️ Processing Pipeline
The script follows a rigorous image processing pipeline:

Preprocessing: Converts raw images to grayscale and applies Otsu's Thresholding for background subtraction.

Noise Removal: Uses morphological operations (remove_small_objects and remove_small_holes) to clean the binary mask.

Scale Calibration: Detects a reference object (30mm Pepsi Cap) to calculate the mm_per_pixel ratio.

Feature Extraction:

Orientation: Calculates the angle of each grain.

Alignment: Rotates grains to a vertical position.

Morphometry: Measures Height and Width in millimeters.

Color Analysis: Computes the average RGB values.

Output Generation: Saves cropped grain images using the specified naming convention and generates a CSV metadata file.

# 🚀 How to Run
Clone the repository:


git clone https://github.com/your-username/rice-grain-dataset.git
Install Dependencies:



pip install numpy pandas scikit-image scipy
Execute the script: Navigate to the CODE/ directory and run:



python main_script.py
# 📊 Features in Metadata
The generated rice_metadata_final.csv includes:

Grain Image Name: Unique filename per grain.

Variety Name: The category of the rice.

Dimensions: Height and Width in mm.

Color Profile: Average R, G, and B values.

⚠️ Academic Integrity
This project was developed for the Introduction to Image Processing (IIP) course. The use of built-in functions for segmentation and region properties is compliant with the project constraints.
