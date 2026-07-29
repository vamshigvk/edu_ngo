// Role-scoped navigation for the authenticated app shell (AppLayout).
// Two navigation modes:
//   - 'tab'  → items switch a ?tab= query param on a single dashboard route (Admin).
//   - 'hash' → items scroll to a section id on a single-page dashboard (Mentor/Mentee/Reviewer).
export const NAV = {
  admin: {
    title: 'Admin',
    base: '/admin',
    mode: 'tab',
    defaultTab: 'mentors',
    items: [
      { label: 'Mentors', tab: 'mentors' },
      { label: 'Students', tab: 'students' },
      { label: 'Applications', tab: 'applications' },
      { label: 'Mapping', tab: 'mapping' },
      { label: 'Matches', tab: 'matches' },
      { label: 'Documents', tab: 'documents' },
      { label: 'Workshops', tab: 'workshops' },
      { label: 'Close-out', tab: 'closeout' },
      { label: 'Cohorts', tab: 'cohorts' },
      { label: 'Resources', tab: 'resources' },
      { label: 'Notifications', tab: 'notifications' },
    ],
  },
  mentor: {
    title: 'Mentor',
    base: '/mentor',
    mode: 'hash',
    items: [
      { label: 'Overview', hash: 'overview' },
      { label: 'My mentees', hash: 'mentees' },
      { label: 'Documents', hash: 'documents' },
      { label: 'Workshops', hash: 'workshops' },
    ],
  },
  mentee: {
    title: 'Mentee',
    base: '/mentee',
    mode: 'hash',
    items: [
      { label: 'Overview', hash: 'overview' },
      { label: 'My mentor', hash: 'mentor' },
      { label: 'Check-ins', hash: 'checkins' },
      { label: 'Documents', hash: 'documents' },
      { label: 'Workshops', hash: 'workshops' },
      { label: 'Close-out', hash: 'closeout' },
    ],
  },
  reviewer: {
    title: 'Reviewer',
    base: '/review',
    mode: 'hash',
    items: [{ label: 'Assigned reviews', hash: 'reviews' }],
  },
}

export const HOME_FOR_ROLE = { admin: '/admin', mentor: '/mentor', mentee: '/mentee', reviewer: '/review' }
