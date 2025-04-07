# Smart Chekad   
**A Django-based CRM web application**  

---

## Getting Started  
To set up and run this project locally, follow the steps below:  

### Prerequisites  
Make sure you have the following installed:  
- Python 3.8 or higher  
- PostgreSQL 13+ (with a database created)  
- Git  

---

### Installation  
1. **Clone the repository:**  
   ```bash  
   git clone https://github.com/arzjafar/smartchekad.git  
   cd mycrm  
   ```  

2. **Create and activate a virtual environment:**  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```  

3. **Install backend dependencies:**  
   ```bash  
   pip install -r backend/requirements/base.txt  
   pip install -r backend/requirements/dev.txt  
   ```  

4. **Set up the `.env` file:**  
   - Copy `backend/.env.sample` to `backend/.env` and fill in the values:  
     ```bash
     cp backend/.env.sample backend/.env
     ```
     Example `.env` content:  
     ```
     SECRET_KEY=your-very-secure-secret-key
     DB_NAME=mycrm_dev
     DB_USER=postgres
     DB_PASSWORD=yourpassword
     DB_HOST=localhost
     DB_PORT=5432
     ```

5. **Configure the database:**  
   - Create a PostgreSQL database:  
     ```bash  
     createdb mycrm_dev  
     ```  
   - Or use your preferred database name and update it in `.env`.

6. **Apply migrations:**  
   ```bash  
   cd backend  
   python manage.py migrate --settings=my_crm.settings.dev  
   ```  

7. **Run the development server:**  
   ```bash  
   python manage.py runserver --settings=my_crm.settings.dev  
   ```  
   Access the app in your browser at `http://localhost:8000`.  

8. **(Optional) Set up the frontend:**  
   If you’re using the React frontend:  
   ```bash  
   cd ../frontend  
   npm install  
   npm start  
   ```  
   Access the frontend at `http://localhost:3000`.

---

## Features  
- **Contact Management**: Add, view, edit, and search contacts.   

---

## Customization  
- Replace the logo
---

## Contributing  
Contributions are welcome! To contribute:  
1. Fork the repository.  
2. Create a new branch: `git checkout -b feature/your-feature-name`.  
3. Commit your changes: `git commit -m "Add your feature"`.  
4. Push to your branch: `git push origin feature/your-feature-name`.  
5. Submit a pull request.  

---

## License  
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.