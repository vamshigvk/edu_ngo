import React from 'react'
import { Page, PageTitle, Prose, SectionTitle, Button } from '../../components/public/ui'

export default function SriLanka(){
  return (
    <Page>
      <PageTitle>sri lanka</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>Improving access to higher education and creating opportunities of growth for individuals from Sri Lanka.</p>
      </Prose>

      <SectionTitle className="mt-12">Sri Lanka Graduate Mentorship Programme</SectionTitle>
      <Prose className="mt-4 max-w-3xl">
        <p>
          Our brand new free mentorship programme to help Sri Lankan individuals who wish to pursue higher
          education abroad! Applications to be a Mentee are now open!
        </p>
      </Prose>
      <div className="mt-8">
        <Button to="/apply/student">learn more</Button>
      </div>
    </Page>
  )
}
