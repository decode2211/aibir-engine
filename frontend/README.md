# AIBIR - AI-Based Internship Recommendation Engine

A React-based frontend application for Smart India Hackathon 2025 that helps students upload their resume and receive AI-based internship recommendations.

## Features

- **Resume Upload**: Drag & drop or click to upload PDF resumes
- **Student Dashboard**: Clean interface showing student profile and recommendations
- **AI Recommendations**: Display ranked internships with match percentages
- **Detailed Internship Info**: Skills required, explanations, and apply links
- **Loading States**: Smooth UX during AI analysis
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on desktop and mobile

## Tech Stack

- **Frontend**: React 18 + Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Styling**: CSS3 with modern design

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.jsx      # Navigation header
│   ├── ResumeUpload.jsx # File upload component
│   ├── RecommendationCard.jsx # Individual recommendation display
│   ├── LoadingSpinner.jsx # Loading animation
│   └── ErrorMessage.jsx # Error display component
├── pages/              # Main application pages
│   ├── Home.jsx        # Landing page with upload
│   └── Dashboard.jsx   # Student dashboard with recommendations
├── context/            # State management
│   └── StudentContext.jsx # Global student state
├── services/           # API integration
│   └── api.js          # HTTP client and API calls
├── App.jsx             # Main app component
├── main.jsx            # React entry point
├── index.css           # Global styles
└── App.css             # Component-specific styles
```

## Setup Instructions

### Prerequisites

1. **Install Node.js** (version 16 or higher)
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your backend API URL.

4. **Start the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:3000`

## API Integration

The app expects these backend endpoints:

### POST /upload-resume
Upload student resume and create profile
```javascript
// Request (FormData)
{
  resume: File,           // PDF file
  student_name: string,   // Student's full name
  student_email: string   // Student's email
}

// Response
{
  student_id: string,     // Unique student identifier
  message: string         // Success message
}
```

### POST /recommend/{student_id}
Generate AI recommendations for student
```javascript
// Response
{
  recommendations: [
    {
      id: number,
      title: string,              // "Frontend Developer Intern"
      company: string,            // "TechCorp Solutions"
      match_percentage: number,   // 92
      required_skills: string[],  // ["React", "JavaScript", "CSS"]
      explanation: string,        // Why this matches
      apply_link: string,         // Application URL
      location: string,           // "Bangalore, India"
      duration: string,           // "3 months"
      stipend: string            // "₹15,000/month"
    }
  ]
}
```

## Demo Features

### Mock Data
The app includes mock recommendation data for demo purposes. To use real backend:

1. Update `src/services/api.js`
2. Replace `getMockRecommendations()` with actual API call
3. Update the API base URL in `.env`

### UI Flow for Judging

1. **Landing Page**: Clean hero section explaining the concept
2. **Upload Process**: Intuitive drag & drop with student info form
3. **Loading State**: Engaging AI analysis animation
4. **Results Display**: Professional recommendation cards with match percentages
5. **Apply Actions**: Direct links to internship applications

## Customization

### Styling
- Modify `src/index.css` for global styles
- Update `src/App.css` for component-specific styles
- Colors and gradients can be changed in CSS custom properties

### Branding
- Update logo and app name in `src/components/Header.jsx`
- Modify hero section in `src/pages/Home.jsx`
- Change page title in `index.html`

### API Endpoints
- Update base URL in `src/services/api.js`
- Modify request/response handling as needed

## Build for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized production files.

## Deployment

The built files can be deployed to any static hosting service:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## Hackathon Demo Tips

1. **Prepare Sample Resumes**: Have 2-3 PDF resumes ready for demo
2. **Backend Mock**: Ensure mock data works if backend isn't ready
3. **Error Scenarios**: Show error handling with invalid files
4. **Mobile View**: Demonstrate responsive design
5. **Loading States**: Highlight the AI analysis animation
6. **Match Explanations**: Emphasize the AI reasoning feature

## Troubleshooting

### Common Issues

1. **Node.js not found**: Install Node.js from official website
2. **Port 3000 in use**: Change port in `vite.config.js`
3. **API errors**: Check backend URL in `.env` file
4. **File upload fails**: Ensure PDF files under 10MB

### Development

- Use browser dev tools to debug API calls
- Check console for error messages
- Verify network requests in Network tab

## License

This project is created for Smart India Hackathon 2025.