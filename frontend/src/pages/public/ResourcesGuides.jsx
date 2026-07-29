import React from 'react'
import { Page, PageTitle, Prose } from '../../components/public/ui'

const GUIDES = [
  'Guide for Writing your CV',
  'Guide for Drafting Personal Statements',
  'Guide for Drafting Statements of Purpose',
  'Guide for Writing Research Proposals',
  'Guide for References / LoRs',
]

export default function ResourcesGuides(){
  return (
    <Page>
      <p className="text-xs uppercase tracking-widest text-neutral-500 mb-3">resources</p>
      <PageTitle>Guides on Application Documents</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          In addition to running a mentorship programme and organising workshops, Project EduAccess regularly
          develops content such as guides and documents that aid potential applicants in their university and
          scholarship application processes. On this page, you will find guides that form a part of our series
          Guides on Application Documents.
        </p>
      </Prose>
      <ul className="mt-10 space-y-3 max-w-2xl">
        {GUIDES.map((g) => (
          <li key={g} className="border border-yellow-400/30 rounded-md p-4 text-neutral-200">{g}</li>
        ))}
      </ul>
    </Page>
  )
}
