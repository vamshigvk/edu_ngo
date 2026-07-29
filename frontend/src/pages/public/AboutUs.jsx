import React from 'react'
import { Page, PageTitle, Prose, LinkCard } from '../../components/public/ui'

export default function AboutUs(){
  return (
    <Page>
      <PageTitle>about us</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Launched in 2021, Project EduAccess is a non-profit initiative that aims to improve access to
          higher education for learners from marginalised communities in the Global South, and create
          opportunities for their professional and personal development. We currently operate in the South
          Asian countries of India, Sri Lanka and Afghanistan.
        </p>
        <p>
          Both in South Asia and elsewhere, higher education institutions, leadership avenues and job
          opportunities are inaccessible to most potential learners due to entrenched fault lines of
          inequality in society. This lack of access may be the result of various barriers. Of these, issues
          tethered to systemic discrimination may require broad-based policy interventions from governments,
          institutions and employers. However, some other accessibility issues – particularly cost,
          information and dispositional barriers – can be resolved through concerted volunteer efforts.
          Therefore, through our tested volunteer model, we make modest attempts to address these barriers and
          improve inclusivity in education, leadership and professional opportunities.
        </p>
        <p>
          We do this primarily by offering free mentorship support to marginalised South Asian learners
          (particularly those disadvantaged inter alia by social position, economic ability, and geography).
          We also advocate with public and private sector entities to make higher education accessible.
        </p>
        <p>
          Our mission is to democratise access to higher education so that all individuals have quality
          educational opportunities, and in turn, better avenues for personal and professional growth and
          holistic development. We believe that concerted effort in this direction is a steppingstone to an
          equal society.
        </p>
      </Prose>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl">
        <LinkCard to="/our-approach" title="our approach">
          Our 3E approach focuses on Equity, Excellence and Expansion.
        </LinkCard>
        <LinkCard to="/team" title="our team">
          Project EduAccess is a collective journey of many dedicated individuals.
        </LinkCard>
      </div>
    </Page>
  )
}
