import React from 'react'
import { Page, PageTitle, Prose, SectionTitle } from '../../components/public/ui'

const PILLARS = [
  {
    name: 'Equity',
    points: [
      'Creating interventions and initiatives that specifically target South Asian learners who are disadvantaged by social position, economic ability, and geography, inter alia.',
      'Making information, guidance, mentorship, and support easily available to our registered learners.',
      'Providing free of cost mentorship to learners.',
      'Organising open-for-all webinars accessible even to non-registered learners.',
    ],
  },
  {
    name: 'Excellence',
    points: [
      'Providing relevant information and top-notch mentorship, general guidance and support on entry into higher education institutions to our registered learners.',
      'Providing a platform for capacity-building to our registered learners, particularly in respect of community and professional leadership.',
      'Providing career counselling support and an easily accessible repository of opportunities for professional growth to our registered learners.',
      'Recruiting experienced mentors from diverse backgrounds, who can provide informed and specific guidance to our registered learners.',
    ],
  },
  {
    name: 'Expansion',
    points: [
      'Scaling up capacity with time, making mentorship and support available for as many opportunities and across as many Global South countries as possible.',
      'Creating a programme to support high-school learners from marginalised communities in the Global South.',
    ],
  },
]

export default function OurApproach(){
  return (
    <Page>
      <PageTitle>our approach</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          We offer one-on-one mentorship to marginalised learners from the Global South seeking entry into
          higher education institutions and opportunities for professional and personal development. Our
          programme adopts the following 3E Approach:
        </p>
      </Prose>

      <div className="mt-12 space-y-10">
        {PILLARS.map((p) => (
          <div key={p.name} className="border-l-2 border-yellow-400 pl-6">
            <SectionTitle>{p.name}</SectionTitle>
            <ul className="mt-4 space-y-3 text-neutral-300 leading-relaxed list-disc list-inside">
              {p.points.map((pt, i) => <li key={i}>{pt}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </Page>
  )
}
