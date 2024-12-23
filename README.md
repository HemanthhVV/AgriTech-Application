# AgriTech-Application

A Django-based web application for an agritech company to handle geotagged images captured by their workforce during ground operations. The solution should allow the company to extract data from the images, store and display the data dynamically, and visualize operations on a map.


---

## **Features**
- **User Authentication:**
  - Secure login/logout functionality.

- **Image Upload and Processing:**
  - Users can upload agricultural images with metadata like latitude, longitude, farmer details, etc.
  - An interactive image viewer and delete options.

- **Geospatial Mapping:**
  - Displays a map interface with agricultural data points.
  - Integrated with Leaflet for dynamic map interactions.

- **Responsive Design:**
  - Optimized for use on vrious screen sizes.
  - Built with Bootstrap and Tailwind CSS for a modern and accessible interface.

---

## **Installation**

### **Prerequisites**
- Python 3.8+
- Django 4.0+
- A database (e.g., PostgreSQL or SQLite for development)
- Any OCR component

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/HemanthhVV/AgriTech-Application.git
   cd agritech
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate   # For Linux/macOS
   env\Scripts\activate      # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables:
   - Create a `.env` file and define the following variables:
     ```
     SECRET_KEY=<your_secret_key>
     EMAIL_HOST=<your_email_host>
     EMAIL_HOST_USER=<your_email_address>
     EMAIL_HOST_PASSWORD=<your_email_password>
     # Add the OCR Secrets(For services like AWS Textract,etc.)
     ```

5. Apply migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Access the app at:
   ```
   http://127.0.0.1:8000/
   ```

---

## **Usage**
1. Register or log in to the platform.
2. Upload agricultural images via the "Add Data" button.
3. View uploaded images, their details, and interact with map data.
4. Use the search bar to find specific data points.
5. Admins can manage data and perform deletion actions.

---

## **Tech Stack**
- **Backend:** Django (Python)
- **Frontend:** HTML,Bootstrap, Tailwind CSS, Leaflet
- **Database:** PostgreSQL

---

## **Assumptions Made During Development**
- The user will upload valid images in supported formats like `.jpg` and `.png`.
- Latitude and longitude metadata will be accurate and available for uploaded images.
- The database is correctly set up and operational before launching the app.
- Email server configurations are correctly defined in the environment.
- The application is hosted on a server with sufficient resources to handle concurrent requests.


---

## **Known Issues**
- No validation for extremely large image uploads.
- The map interface might have limited functionality offline due to Leaflet's dependency on online resources.

---


## **License**
- This project is licensed under the GNU GENERAL PUBLIC LICENSE.


