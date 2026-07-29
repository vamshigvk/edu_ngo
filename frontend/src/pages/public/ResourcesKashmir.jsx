import React from 'react'
import { Page, PageTitle, Prose, SectionTitle } from '../../components/public/ui'

const SESSIONS = [
  'Introduction to Graduate Studies',
  'Writing your CV',
  'Personal Statements & Statements of Purpose (SoP)',
  'Funding and Scholarships',
  'PhD Applications',
]

const DAYS = [
  ['Day 1: Social Sciences', SESSIONS],
  ['Day 2: Science, Technology, Engineering & Mathematics (STEM)', SESSIONS],
  ['Day 3: Humanities', SESSIONS],
]

export default function ResourcesKashmir(){
  return (
    <Page>
      <p className="text-xs uppercase tracking-widest text-neutral-500 mb-3">resources</p>
      <PageTitle>Workshop on Studying Abroad at Kashmir University</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Project EduAccess, in collaboration with the Centre for Career Planning and Counselling, University
          of Kashmir organised a free, three-day in-person workshop on studying abroad. This workshop was
          generously supported by the Thatcher Development Award of Somerville College, University of Oxford,
          and was held from 29–31 August 2022 at the University of Kashmir.
        </p>
        <p>
          The aim of the workshop was to equip students interested in pursuing studies abroad with all the
          necessary knowledge and skills required to make an application — including sessions on CV writing,
          personal statement/statements of purpose writing, drafting of application essays and research
          proposals, and finding scholarship and funding opportunities. On this page, you will find all the
          resources and training material from the workshop.
        </p>
      </Prose>

      <div className="mt-10 space-y-8">
        {DAYS.map(([day, sessions]) => (
          <div key={day}>
            <SectionTitle>{day}</SectionTitle>
            <ul className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2">
              {sessions.map((s) => (
                <li key={s} className="text-sm text-neutral-300 border border-yellow-400/25 rounded px-3 py-2">{s}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </Page>
  )
}
