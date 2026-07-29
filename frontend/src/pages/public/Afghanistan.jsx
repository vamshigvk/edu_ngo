import React from 'react'
import { Page, PageTitle, Prose, Button } from '../../components/public/ui'

export default function Afghanistan(){
  return (
    <Page>
      <PageTitle>afghanistan</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>Improving access to higher education and creating opportunities of growth for individuals from Afghanistan.</p>
        <p className="text-neutral-400 text-sm">in collaboration with our partners</p>
      </Prose>
      <div className="mt-8">
        <Button to="/our-work" variant="ghost">explore our programmes</Button>
      </div>
    </Page>
  )
}
