import React from 'react'
import { Page, PageTitle, Prose, LinkCard } from '../../components/public/ui'

export default function OurWork(){
  return (
    <Page>
      <PageTitle>our work</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          We run free mentorship programmes to improve access to higher education and create opportunities of
          growth for learners from marginalised communities across the Global South. Explore our work by
          country.
        </p>
      </Prose>
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-3 gap-6">
        <LinkCard to="/india" title="india">
          Improving access to higher education and creating opportunities of growth for learners from
          marginalised communities in India.
        </LinkCard>
        <LinkCard to="/afghanistan" title="afghanistan">
          Improving access to higher education and creating opportunities of growth for individuals from
          Afghanistan.
        </LinkCard>
        <LinkCard to="/sri-lanka" title="sri lanka">
          Improving access to higher education and creating opportunities of growth for individuals from Sri
          Lanka.
        </LinkCard>
      </div>
    </Page>
  )
}
