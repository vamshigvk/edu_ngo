import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import PublicLayout from './components/layout/PublicLayout'
// Public marketing pages (replica of projecteduaccess.com)
import Home from './pages/public/Home'
import AboutUs from './pages/public/AboutUs'
import OurApproach from './pages/public/OurApproach'
import Team from './pages/public/Team'
import OurWork from './pages/public/OurWork'
import India from './pages/public/India'
import Afghanistan from './pages/public/Afghanistan'
import SriLanka from './pages/public/SriLanka'
import IndiaProgramme from './pages/public/IndiaProgramme'
import Advocacy from './pages/public/Advocacy'
import Resources from './pages/public/Resources'
import ResourcesGuides from './pages/public/ResourcesGuides'
import ResourcesWorkshops from './pages/public/ResourcesWorkshops'
import ResourcesKashmir from './pages/public/ResourcesKashmir'
import Contact from './pages/public/Contact'
// Platform pages
import Apply from './pages/public/Apply'
import StudentForm from './pages/public/StudentForm'
import MentorForm from './pages/public/MentorForm'
import Login from './pages/public/Login'
import Signup from './pages/public/Signup'
// Dashboards
import Admin from './pages/dashboard/Admin'
import Mentor from './pages/dashboard/Mentor'
import Mentee from './pages/dashboard/Mentee'
import Reviewer from './pages/dashboard/Reviewer'
import ProtectedRoute from './components/common/ProtectedRoute'

export default function App(){
  return (
    <Routes>
      <Route path="/" element={<PublicLayout />}>
        <Route index element={<Home/>} />

        {/* About */}
        <Route path="about-us" element={<AboutUs/>} />
        <Route path="our-approach" element={<OurApproach/>} />
        <Route path="team" element={<Team/>} />

        {/* Our work */}
        <Route path="our-work" element={<OurWork/>} />
        <Route path="india" element={<India/>} />
        <Route path="afghanistan" element={<Afghanistan/>} />
        <Route path="sri-lanka" element={<SriLanka/>} />
        <Route path="india-graduate-mentorship-programme" element={<IndiaProgramme/>} />

        {/* Advocacy */}
        <Route path="advocacy" element={<Advocacy/>} />

        {/* Resources */}
        <Route path="resources" element={<Resources/>} />
        <Route path="resources/guides" element={<ResourcesGuides/>} />
        <Route path="resources/workshops" element={<ResourcesWorkshops/>} />
        <Route path="resources/kashmir" element={<ResourcesKashmir/>} />

        {/* Contact */}
        <Route path="contact-us" element={<Contact/>} />

        {/* Platform */}
        <Route path="apply" element={<Apply/>} />
        <Route path="apply/student" element={<StudentForm/>} />
        <Route path="apply/mentor" element={<MentorForm/>} />
        <Route path="login" element={<Login/>} />
        <Route path="signup" element={<Signup/>} />

        {/* Dashboards */}
        <Route path="admin" element={<ProtectedRoute role="admin"><Admin/></ProtectedRoute>} />
        <Route path="mentor" element={<ProtectedRoute role="mentor"><Mentor/></ProtectedRoute>} />
        <Route path="mentee" element={<ProtectedRoute role="mentee"><Mentee/></ProtectedRoute>} />
        <Route path="review" element={<ProtectedRoute role="reviewer"><Reviewer/></ProtectedRoute>} />

        {/* Legacy path redirects */}
        <Route path="about" element={<Navigate to="/about-us" replace />} />
        <Route path="work" element={<Navigate to="/our-work" replace />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
