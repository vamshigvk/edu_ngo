import React from 'react'
import { Page, PageTitle, Prose, LinkCard } from '../../components/public/ui'

export default function Apply(){
  return (
    <Page>
      <PageTitle>apply</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Join Project EduAccess as a mentee to receive free, personalised 1:1 mentorship, or sign up as a
          mentor to support learners from marginalised communities. Choose how you'd like to get involved.
        </p>
      </Prose>
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl">
        <LinkCard to="/apply/student" title="apply as a mentee">
          Get comprehensive support and free 1:1 mentorship from graduates of top foreign universities for
          postgraduate degrees (including PhD).
        </LinkCard>
        <LinkCard to="/apply/mentor" title="become a mentor">
          Share your expertise and experience to positively impact the future of students from historically
          marginalised and disadvantaged communities.
        </LinkCard>
      </div>
    </Page>
  )
}
