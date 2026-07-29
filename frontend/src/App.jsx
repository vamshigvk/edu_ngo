import React from 'react'
import { Routes, Route } from 'react-router-dom'
import PublicLayout from './components/layout/PublicLayout'
import Home from './pages/public/Home'
import About from './pages/public/About'
import OurWork from './pages/public/OurWork'
import Apply from './pages/public/Apply'
import StudentForm from './pages/public/StudentForm'
import MentorForm from './pages/public/MentorForm'
import Login from './pages/public/Login'
import Signup from './pages/public/Signup'
import Admin from './pages/dashboard/Admin'
import Mentor from './pages/dashboard/Mentor'
import Mentee from './pages/dashboard/Mentee'
import Reviewer from './pages/dashboard/Reviewer'
import Resources from './pages/public/Resources'
import ProtectedRoute from './components/common/ProtectedRoute'

export default function App(){
  return (
    <Routes>
      <Route path="/" element={<PublicLayout />}>
        <Route index element={<Home/>} />
        <Route path="about" element={<About/>} />
        <Route path="work" element={<OurWork/>} />
        <Route path="apply" element={<Apply/>} />
        <Route path="apply/student" element={<StudentForm/>} />
        <Route path="apply/mentor" element={<MentorForm/>} />
        <Route path="login" element={<Login/>} />
        <Route path="signup" element={<Signup/>} />
        <Route path="resources" element={<Resources/>} />
        <Route path="admin" element={<ProtectedRoute role="admin"><Admin/></ProtectedRoute>} />
        <Route path="mentor" element={<ProtectedRoute role="mentor"><Mentor/></ProtectedRoute>} />
        <Route path="mentee" element={<ProtectedRoute role="mentee"><Mentee/></ProtectedRoute>} />
        <Route path="review" element={<ProtectedRoute role="reviewer"><Reviewer/></ProtectedRoute>} />
      </Route>
    </Routes>
  )
}
