<<<<<<< HEAD
# 🎯 SkillMatchAI

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.11.9-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?style=for-the-badge&logo=mongodb)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AI-Powered Internship Matching Platform**

*Connecting students to their dream internships using machine learning magic* ✨

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Tech Stack](#-tech-stack) • [License](#-license)

</div>

---

## 🌟 What is SkillMatchAI?

Ever wondered how Netflix knows what you want to watch? We do the same thing, but for **internships**! 🎓

SkillMatchAI uses **TF-IDF (Term Frequency-Inverse Document Frequency)** and **cosine similarity** to intelligently match students with internships based on their skills. No more endless scrolling through job boards – our AI does the heavy lifting!

### 🎬 The Story Behind This Project

This project was built through an epic journey of:
- ☕ Multiple debugging sessions
- 🔧 SSL certificate battles (we won!)
- 🐛 Python version upgrades
- 💪 Persistence and determination
- 🎉 And finally... SUCCESS!

*Built with passion, debugged with patience, and deployed with pride.*

---

## ✨ Features

### 🔐 **Secure Authentication**
- JWT-based token authentication
- Bcrypt password hashing
- Protected routes with role-based access

### 👥 **User Management**
- Complete user registration and login
- Profile management with skills and projects
- Secure password handling

### 💼 **Internship Listings**
- Full CRUD operations for internships
- Rich internship details (title, company, domain, skills, stipend)
- Search and filter capabilities

### 🤖 **AI-Powered Matching** (The Star of the Show!)
- **TF-IDF Vectorization**: Converts skills into numerical vectors
- **Cosine Similarity**: Calculates match scores (0.0 to 1.0)
- **Ranked Recommendations**: Get internships sorted by relevance
- **Matched Skills Highlighting**: See exactly which skills matched

### 📚 **Auto-Generated Documentation**
- Interactive Swagger UI at `/docs`
- ReDoc documentation at `/redoc`
- Try API endpoints directly in browser

---
=======
# SkillMatchAI - Intelligent Internship Matching Platform

🎓 An AI-powered internship matching platform that connects students with their ideal opportunities using TF-IDF algorithm and cosine similarity.

**Version**: 1.0 | **Status**: Production Ready ✅ | **Tech**: FastAPI + MongoDB + Vanilla JS

## 🌟 Features

### For Students
- **AI-Powered Matching**: Get personalized internship recommendations based on your skills
- **Profile Management**: Maintain your academic profile with branch, semester, and CGPA
- **Smart Applications**: Apply to internships and track your application status
- **Browse & Search**: Explore all available internships with advanced filters

### For Companies
- **Post Internships**: Create and manage internship opportunities
- **Skill-Based Targeting**: Attract candidates with specific skill sets
- **Application Management**: Review and manage incoming applications
- **Analytics Dashboard**: Track application metrics and performance

### For Admins/Schools
- **Comprehensive Analytics**: View system-wide statistics and insights
- **Student Management**: Monitor student profiles, block/unblock accounts
- **Branch Analytics**: Track students by branch with performance metrics (CGPA)
- **Internship Oversight**: Delete inappropriate internships
- **Top Performers**: View leaderboard of top students by CGPA
- **Application Insights**: Monitor internship application trends
>>>>>>> a09f447 (modifications and finaltouch on 22/10/2025)

## 🚀 Quick Start

### Prerequisites
<<<<<<< HEAD

- Python 3.11.9 or higher
- MongoDB 7.0 or higher
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/SkillMatchAI.git
cd SkillMatchAI

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment variables
cp .env.example .env
# Edit .env with your settings

# 6. Start MongoDB
# Windows:
net start MongoDB
# macOS:
brew services start mongodb-community
# Linux:
sudo systemctl start mongod

# 7. Run the application
uvicorn app.main:app --reload
```

### 🎉 You're Live!

Open your browser:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000

---

## 📖 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login user | ❌ |

### User Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/users/me` | Get current user profile | ✅ |
| `PUT` | `/api/users/me` | Update profile | ✅ |
| `DELETE` | `/api/users/me` | Delete account | ✅ |

### Internship Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/internships/` | Create internship | ✅ |
| `GET` | `/api/internships/` | List all internships | ✅ |
| `GET` | `/api/internships/{id}` | Get internship details | ✅ |
| `PUT` | `/api/internships/{id}` | Update internship | ✅ |
| `DELETE` | `/api/internships/{id}` | Delete internship | ✅ |

### 🎯 Matching Endpoints (Core Feature!)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/match/{user_id}` | Get matches for user | ✅ |
| `GET` | `/api/match/me/recommendations` | Get my recommendations | ✅ |

---

## 💡 Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "password": "securepass123",
    "skills": ["Python", "FastAPI", "Machine Learning"],
    "projects": ["Built REST API", "ML Classification Model"]
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "skills": ["Python", "FastAPI", "Machine Learning"],
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### 2. Create an Internship

```bash
curl -X POST "http://localhost:8000/api/internships/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Developer Intern",
    "company": "TechCorp",
    "domain": "Software Development",
    "required_skills": ["Python", "FastAPI", "MongoDB"],
    "description": "Build scalable REST APIs",
    "location": "Remote",
    "duration": "3 months",
    "stipend": "$500/month"
  }'
```

### 3. Get Personalized Recommendations 🎯

```bash
curl -X GET "http://localhost:8000/api/match/me/recommendations" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439012",
    "title": "Backend Developer Intern",
    "company": "TechCorp",
    "domain": "Software Development",
    "required_skills": ["Python", "FastAPI", "MongoDB"],
    "description": "Build scalable REST APIs",
    "match_score": 0.8756,
    "matched_skills": ["Python", "FastAPI"]
  }
]
```

---

## 🧠 How the Matching Algorithm Works

```
┌─────────────────┐
│  User Skills    │
│ ["Python",      │
│  "FastAPI",     │
│  "MongoDB"]     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   TF-IDF Vectorization  │
│   [0.5, 0.3, 0.8, ...]  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Cosine Similarity      │
│  Calculate angle        │
│  between vectors        │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Match Score: 0.8756    │
│  (87.56% match!)        │
└─────────────────────────┘
```

**Match Score Interpretation:**
- 🔥 **0.8 - 1.0**: Excellent match
- ✅ **0.6 - 0.8**: Good match
- 👍 **0.4 - 0.6**: Moderate match
- 🤔 **0.0 - 0.4**: Poor match

---
=======
- Python 3.8+
- MongoDB (running locally or remote connection)
- Modern web browser

### Installation

1. **Clone or download the project**
```bash
cd BPUT
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**
Create a `.env` file in the root directory:
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=skillmatchai_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

6. **Start the server**
```bash
python run.py
```

The server will start at: `http://localhost:8000`

### Access the Application

- **Frontend**: Open `frontend/index.html` in your browser
- **API Documentation**: Visit `http://localhost:8000/docs`
- **ReDoc**: Visit `http://localhost:8000/redoc`

## 👥 User Roles

### 1. Student
- Register with skills and academic details (branch, semester, CGPA)
- Receive AI-powered internship recommendations
- Apply to internships
- Track application status

### 2. Company
- Post internship opportunities
- Manage posted internships
- View applications

### 3. Admin/School
- Access comprehensive analytics dashboard
- View students by branch with average CGPA
- Monitor top performing students
- Block/unblock student accounts
- Delete any internship posting
- View application statistics
>>>>>>> a09f447 (modifications and finaltouch on 22/10/2025)

## 🏗️ Project Structure

```
<<<<<<< HEAD
SkillMatchAI/
│
├── 📁 app/
│   ├── 📄 __init__.py
│   ├── 📄 main.py                 # FastAPI app entry point
│   ├── 📄 config.py               # Configuration settings
│   │
│   ├── 📁 models/
│   │   ├── 📄 user.py            # User Pydantic models
│   │   └── 📄 internship.py      # Internship models
│   │
│   ├── 📁 routes/
│   │   ├── 📄 auth.py            # Authentication routes
│   │   ├── 📄 users.py           # User routes
│   │   ├── 📄 internships.py     # Internship routes
│   │   └── 📄 matching.py        # Matching routes ⭐
│   │
│   ├── 📁 services/
│   │   ├── 📄 auth_service.py    # JWT & password handling
│   │   ├── 📄 user_service.py    # User business logic
│   │   ├── 📄 internship_service.py
│   │   └── 📄 matching_service.py # TF-IDF algorithm ⭐
│   │
│   └── 📁 database/
│       └── 📄 db.py               # MongoDB connection
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env.example               # Environment template
├── 📄 .gitignore                 # Git ignore rules
├── 📄 README.md                  # You are here!
└── 📄 LICENSE                    # MIT License
```

---

## 🛠️ Tech Stack

### Backend Framework
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)

### Database
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Motor](https://img.shields.io/badge/Motor-Async-brightgreen?style=flat-square)

### Authentication & Security
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![Bcrypt](https://img.shields.io/badge/Bcrypt-003B57?style=flat-square)

### Machine Learning
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)

### Data Validation
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)

---

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
APP_NAME=SkillMatchAI
APP_VERSION=1.0.0
DEBUG=True

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=skillmatchai_db

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

**🔒 Security Note:** Never commit your `.env` file to version control!

---

## 🧪 Testing

### Manual Testing via Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs
3. Register a user
4. Authorize with the JWT token (click 🔒 button)
5. Create internships
6. Test the matching endpoint!

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "SkillMatchAI",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## 🚀 Deployment

### Docker (Coming Soon!)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku, Railway, Render

This app is ready to deploy on any platform that supports Python and MongoDB!

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see below for details.

```
MIT License

Copyright (c) 2024 SkillMatchAI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Built with ❤️ by a passionate developer who believes in the power of AI to connect talent with opportunities.**

- GitHub: [@Ashutosh3021](https://github.com/Ashutosh3021)
- Project Link: [SkillMatchAI](https://github.com/Ashutosh3021/SkillMatchAI)

---

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **MongoDB** - For the flexible NoSQL database
- **scikit-learn** - For the ML algorithms that make matching possible
- **The entire Python community** - For building awesome tools
- **Coffee** ☕ - For keeping us awake during debugging sessions
- **Stack Overflow** - For answers to questions we didn't know we had
- **You** - For checking out this project!

---

## 🌟 Show Your Support

If this project helped you, please give it a ⭐️!

**Found a bug?** Open an issue!  
**Have an idea?** Start a discussion!  
**Want to contribute?** Send a PR!

---

## 📊 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/SkillMatchAI?style=social)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/SkillMatchAI?style=social)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/SkillMatchAI)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/YOUR_USERNAME/SkillMatchAI)

---

## 🎯 Roadmap

- [x] Core API with FastAPI
- [x] MongoDB Integration
- [x] JWT Authentication
- [x] TF-IDF Matching Algorithm
- [ ] User dashboards
- [ ] Email notifications
- [ ] Advanced filtering
- [ ] Machine learning model improvements
- [ ] Mobile app (Flutter/React Native)
- [ ] Real-time notifications
- [ ] Analytics dashboard

---

## 💬 Contact & Support

Have questions? Need help?

- 📧 Email: your.email@example.com
- 💬 Open an [Issue](https://github.com/YOUR_USERNAME/SkillMatchAI/issues)
- 🐦 Twitter: [@YourTwitter](https://twitter.com/yourhandle)

---

<div align="center">

**Made with 💻 and ☕ by developers, for developers**

⭐ **Star us on GitHub** — it motivates us a lot!

[Report Bug](https://github.com/YOUR_USERNAME/SkillMatchAI/issues) • [Request Feature](https://github.com/YOUR_USERNAME/SkillMatchAI/issues)

---

*"Matching dreams with opportunities, one algorithm at a time."* ✨

</div>
=======
BPUT/
├── app/
│   ├── models/           # Pydantic models
│   │   ├── user.py
│   │   ├── internship.py
│   │   └── application.py
│   ├── routes/           # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── internships.py
│   │   ├── applications.py
│   │   ├── matching.py
│   │   └── admin.py      # New: Admin endpoints
│   ├── services/         # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── internship_service.py
│   │   ├── application_service.py
│   │   ├── matching_service.py
│   │   └── admin_service.py  # New: Admin operations
│   ├── database/         # Database connection
│   │   └── db.py
│   ├── config.py         # Configuration
│   └── main.py          # FastAPI app
├── frontend/            # Frontend files
│   ├── index.html       # Main UI with all dashboards
│   ├── app.js          # JavaScript logic
│   ├── styles.css      # Styling
│   └── theme.css       # Theme variables
├── requirements.txt    # Python dependencies
├── run.py             # Server startup script
└── README.md          # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `DELETE /api/users/me` - Delete user account

### Internships
- `POST /api/internships/` - Create internship
- `GET /api/internships/` - Get all internships
- `GET /api/internships/{id}` - Get specific internship
- `PUT /api/internships/{id}` - Update internship
- `DELETE /api/internships/{id}` - Delete internship

### Applications
- `POST /api/applications/` - Create application
- `GET /api/applications/me` - Get my applications
- `DELETE /api/applications/{id}` - Withdraw application

### Matching
- `GET /api/match/me/recommendations` - Get personalized recommendations
- `POST /api/match/calculate` - Calculate match for specific internship

### Admin (New - Phase 4 & 5)
- `GET /api/admin/analytics/overview` - System overview statistics
- `GET /api/admin/analytics/students-by-branch` - Students grouped by branch
- `GET /api/admin/analytics/students-by-semester` - Students by semester
- `GET /api/admin/analytics/top-students` - Top performers by CGPA
- `GET /api/admin/analytics/internships` - Internship analytics by domain
- `GET /api/admin/analytics/applications` - Application analytics
- `GET /api/admin/analytics/placement` - **NEW**: Placement tracking analytics
- `GET /api/admin/analytics/company-hiring` - **NEW**: Company hiring statistics
- `GET /api/admin/students/unplaced` - **NEW**: Unplaced students list
- `GET /api/admin/students` - Get all students (with filters)
- `GET /api/admin/internships` - Get all internships with stats
- `POST /api/admin/students/{id}/block` - Block student
- `POST /api/admin/students/{id}/unblock` - Unblock student
- `DELETE /api/admin/internships/{id}` - Delete any internship

## 🎨 User Interface

### Landing Page
- Modern, responsive design
- Role selection (Student, Company, Admin/School)
- Feature highlights
- How it works section

### Student Dashboard
- Personalized recommendations with match scores
- Application tracking
- Profile management with academic details
- Browse all internships

### Company Dashboard
- Create internship postings
- Manage existing postings
- View applications (coming soon)

### Admin Dashboard
- **Analytics Section**:
  - Overview cards (students, companies, internships, applications)
  - **NEW**: Placement tracking charts (placed/searching/not placed)
  - **NEW**: Placement type distribution (internship/job/both)
  - **NEW**: Salary statistics by placement type
  - **NEW**: Company hiring statistics with sorting
  - Students by branch with average CGPA
  - Top performing students leaderboard
- **Interactive Filters** (NEW):
  - Filter by branch (CSE, ECE, ME, EE, CE)
  - Filter by semester (1-8)
  - Filter by placement status
  - Apply/Reset filter functionality
- **Students Section**:
  - View all student profiles
  - Block/unblock student accounts
  - See academic performance (branch, semester, CGPA)
  - **NEW**: View placement status
- **Internships Section**:
  - View all internships with application counts
  - Delete any internship posting
- **Unplaced Students** (NEW):
  - List of students without placements
  - Sorted by CGPA
  - **Export to CSV** functionality

## 🤖 AI Matching Algorithm

The platform uses TF-IDF (Term Frequency-Inverse Document Frequency) with cosine similarity to match students with internships:

1. **Skill Vectorization**: Convert student skills and internship requirements into TF-IDF vectors
2. **Similarity Calculation**: Compute cosine similarity between vectors
3. **Score Generation**: Generate match percentage (0-100%)
4. **Ranking**: Sort recommendations by match score

## 🔐 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- Protected admin endpoints
- Input validation with Pydantic
- Account blocking capability for admins

## 📊 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  role: String,  // "student", "company", "admin"
  hashed_password: String,
  skills: [String],
  projects: [String],
  branch: String,       // e.g., "CSE", "ECE", "ME"
  semester: Number,     // 1-8
  cgpa: Number,         // 0.0-10.0
  // NEW: Placement tracking fields
  placement_status: String,  // "placed", "searching", "not_placed"
  company_placed: String,    // Company name if placed
  salary_package: Number,    // Salary in LPA
  placement_type: String,    // "internship", "job", "both"
  is_blocked: Boolean,
  created_at: DateTime,
  updated_at: DateTime
}
```

### Internships Collection
```javascript
{
  _id: ObjectId,
  title: String,
  company: String,
  domain: String,
  required_skills: [String],
  description: String,
  location: String,
  duration: String,
  stipend: String,
  posted_by: String,  // User ID
  created_at: DateTime,
  updated_at: DateTime
}
```

### Applications Collection
```javascript
{
  _id: ObjectId,
  student_id: String,
  internship_id: String,
  status: String,  // "pending", "accepted", "rejected"
  applied_at: DateTime
}
```

## 🔄 Future Enhancements

- [ ] Email notifications
- [ ] Resume upload
- [ ] Interview scheduling
- [x] ~~Advanced analytics with charts~~ ✅ **COMPLETED (Phase 4)**
- [x] ~~Export reports (CSV)~~ ✅ **COMPLETED (Phase 4)**
- [ ] Export reports (PDF/Excel)
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Real-time chat between students and companies
- [x] ~~Placement tracking~~ ✅ **COMPLETED (Phase 4)**
- [x] ~~Interactive filters~~ ✅ **COMPLETED (Phase 4)**
- [x] ~~Company hiring statistics~~ ✅ **COMPLETED (Phase 4)**

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure MongoDB is running
- Check MONGODB_URI in .env file
- Verify network connectivity

### Authentication Errors
- Clear browser localStorage
- Check if SECRET_KEY is set in .env
- Verify token hasn't expired

### Blocked Account
- Contact admin to unblock your account
- Admins can unblock from Admin Dashboard > Students

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Developer Notes

### Creating an Admin Account

Admin accounts must be created with the role field:

```python
# Register via API with role="admin"
POST /api/auth/register
{
  "name": "Admin User",
  "email": "admin@example.com",
  "password": "SecurePass123",
  "role": "admin",
  "skills": [],
  "projects": []
}
```

Or directly in MongoDB:
```javascript
db.users.insertOne({
  name: "Admin",
  email: "admin@school.edu",
  role: "admin",
  hashed_password: "$2b$12$...",  // Use bcrypt to hash password
  skills: [],
  projects: [],
  is_blocked: false,
  created_at: new Date(),
  updated_at: new Date()
})
```

### Student Academic Fields

When students register, they can include:
- `branch`: Department/Branch (CSE, ECE, ME, etc.)
- `semester`: Current semester (1-8)
- `cgpa`: Current CGPA (0.0-10.0)

These fields are optional during registration but recommended for better analytics.

## 📧 Support

For issues or questions, please check the API documentation at `/docs` or contact the development team.

---

## 🎉 Phase 4 & 5 Enhancements (Latest)

### What's New in Phase 4 & 5

We've added comprehensive **placement tracking** and **advanced analytics** to the admin dashboard:

#### 📊 Placement Analytics
- **Placement Overview**: Visual breakdown of placed/searching/not placed students
- **Placement Rate**: Real-time calculation of overall placement percentage
- **Placement Type Distribution**: Charts showing internship vs job vs both
- **Salary Statistics**: Average, min, max salary by placement type

#### 🔍 Interactive Filters
- **Branch Filter**: Filter students by CSE, ECE, ME, EE, CE
- **Semester Filter**: Filter by semester (1-8)
- **Placement Status Filter**: View placed, searching, or not placed students
- **Multi-criteria**: Combine filters for precise results

#### 🏢 Company Hiring Stats
- **Hiring Metrics**: Students hired per company
- **Salary Insights**: Average salary offered by each company
- **Interactive Sorting**: Click to sort by hire count (ascending/descending)
- **Visual Tables**: Clean, sortable data presentation

#### 📥 Unplaced Students List
- **Smart List**: Unplaced students sorted by CGPA
- **Export to CSV**: One-click download of student data
- **Comprehensive Data**: Name, email, branch, semester, CGPA, skills
- **Date-stamped Files**: Automatic filename with current date

#### 🧪 Testing & Validation
- **Test Script**: `test_phase4_5.py` for creating test data
- **Validation Suite**: Automated endpoint testing
- **Sample Data**: Pre-configured students with various placement statuses

### How to Use Phase 4 & 5 Features

1. **Login as Admin**: Use `admin@bput.edu` / `Admin@123`
2. **View Analytics**: See placement charts and statistics
3. **Apply Filters**: Select branch, semester, or placement status
4. **Sort Companies**: Click "Sort by Hired" to toggle order
5. **Export Data**: Click "Export CSV" on unplaced students list

### Testing Phase 4 & 5

Run the test script to create sample data:
```bash
python test_phase4_5.py
# Choose option 1 to create test data
# Choose option 2 to validate analytics
# Choose option 3 for both
```

### Documentation
- **Full Details**: See `PHASE_4_5_COMPLETE.md` for comprehensive documentation
- **Implementation**: All code is production-ready and tested
- **Performance**: Optimized MongoDB aggregations and client-side filtering

---

**Built with ❤️ using FastAPI, MongoDB, and Vanilla JavaScript**
>>>>>>> a09f447 (modifications and finaltouch on 22/10/2025)
