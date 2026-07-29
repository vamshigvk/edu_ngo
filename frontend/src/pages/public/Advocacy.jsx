import React from 'react'
import { Page, PageTitle, Prose, Button } from '../../components/public/ui'

export default function Advocacy(){
  return (
    <Page>
      <PageTitle>advocacy for inclusion</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          We advocate with public and private sector entities to make higher education and opportunities
          truly accessible for all.
        </p>
      </Prose>
      <div className="mt-8">
        <Button to="/contact-us">get in touch to know more</Button>
      </div>
    </Page>
  )
}
