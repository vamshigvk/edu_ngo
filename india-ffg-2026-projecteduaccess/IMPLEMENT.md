# Implementation Plan

## Goal
Build a role-based education platform with separate UIs for Admin, Mentor, Mentee, and Student using:
- React for the frontend
- FastAPI for the backend
- SQLite for the database

## Scope
Focus on the custom-build features from the attached feature list and ignore Zoho/Wix and other platform recommendations.

## Functional requirements
1. Authentication
   - Sign in
   - Sign up
   - Role-based login redirection

2. Roles
   - Admin
   - Mentor
   - Mentee
   - Student

3. Admin capabilities
   - Approve/reject new users
   - Mark users as verified mentor/mentee/student
   - Publish notices/updates

4. Role-based UI experiences
   - Admin portal with moderation and approvals
   - Mentor portal with mentoring tools and notices
   - Mentee portal with applications, recommendations, and updates
   - Student portal with resources, applications, and notices

5. Core modules
   - Application intake
   - Mentor-mentee matching
   - Recommendation scoring
   - Resource search
   - Check-in tracking
   - FAQ/help content
   - Dashboard with charts
   - Data purge/admin cleanup

## Technical approach
### Frontend
- React app with route-based dashboards
- Role-specific layouts and navigation
- Protected routes based on authentication and role

### Backend
- FastAPI app with auth, user management, approvals, notices, and feature endpoints
- SQLite database with schema for users, roles, profiles, applications, matches, recommendations, resources, and announcements

### Database
- SQLite file-based database
- Seed data for default admin and sample users

## Implementation order
1. Create project structure for frontend and backend
2. Set up SQLite schema and database initialization
3. Implement authentication and role-based routing
4. Build admin approval and verification flow
5. Build role-specific dashboards and notices
6. Implement core feature modules
7. Add README instructions and sample data
