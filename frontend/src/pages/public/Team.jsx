import React from 'react'
import { Page, PageTitle, Prose } from '../../components/public/ui'

const TEAM = [
  'Sameer Rashid Bhat', 'Gayathree Devi KT', 'Misbah Reshi', 'Manzer', 'Anwesha Lahiri',
  'Surajkumar Thube', 'Trishant Simlai', 'Sahreen Shamim', 'Damni Kain', 'Suhail R Bhat',
  'Maria Shawl', 'Tejas Rao', 'Rakshanda Bhat', 'Imad ul Riyaz', 'Akumjung Pongen',
  'Rohini Rai', 'Aditi Premkumar', 'Sumit Turuk', 'Abdullah Azzam', 'Khushboo',
  'Khansa Maria', 'Ritheka Sundar',
]

export default function Team(){
  return (
    <Page>
      <PageTitle>our team</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>Project EduAccess is a collective journey of many dedicated individuals.</p>
      </Prose>
      <div className="mt-10 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {TEAM.map((name) => (
          <div key={name} className="border border-yellow-400/40 rounded-md p-4 text-center">
            <div className="mx-auto h-12 w-12 rounded-full bg-yellow-400/20 border border-yellow-400/40 mb-3" />
            <p className="text-sm text-neutral-200">{name}</p>
          </div>
        ))}
      </div>
    </Page>
  )
}
