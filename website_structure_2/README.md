# Material Estimation Web Application

This project is a Flask web application that estimates building materials and facade areas based on uploaded images and location coordinates.

## Setup Instructions

Follow these steps to set up the environment and run the application using the CMD terminal on Windows.

### 1. Clone the Repository

First, clone the repository to your local machine. Navigate to the project directory using CMD:

cd path_to_your_directory\AIAStudioG03\website_structure_2

### 2. Create a Virtual Environment

Create a virtual environment named `myenv`:

python -m venv myenv

### 3. Activate the Virtual Environment

Activate the virtual environment using the following command:

myenv\Scripts\activate

### 4. Install Dependencies

With the virtual environment activated, install the dependencies listed in `requirements.txt`:

pip install -r requirements.txt

### 5. Run the Flask Application

Now that all dependencies are installed, you can run your Flask application:

python app.py

### 6. Access the Application

Open your web browser and navigate to:

http://127.0.0.1:5000/

to access the application.

## File Structure

- `app.py`: Main application file to run the Flask app.
- `facade_calc.py`: Script for facade calculations.
- `requirements.txt`: List of dependencies for the project.
- `templates/index.html`: HTML template for the web page.

## Dependencies

The following libraries are required and listed in `requirements.txt`:

- Flask
- requests
- Pillow
- torch
- transformers
- matplotlib
- numpy
- tensorflow
- osmnx
- geopandas
- shapely
- pandas
- pyproj
- joblib

## Contact

For any issues or questions, please contact Mohammad.

---

Follow these instructions to set up and run the Material Estimation web application successfully.
