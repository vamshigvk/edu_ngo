import React from 'react'
import { Page, PageTitle, Prose } from '../../components/public/ui'

// Grouped by month, as on projecteduaccess.com/resources-from-online-workshops.
const WORKSHOPS = [
  ['June 2023', ['Alternative Sources of Funding – 4 June 2023']],
  ['May 2023', ['Oxford and Cambridge Society of India Scholarships – 5 May 2023']],
  ['April 2023', [
    'Rotary Scholarships – 22 April 2023',
    'Debesh-Kamal Scholarships – 15 April 2023',
    'Lady Meherbai D Tata Education Trust Scholarship – 9 April 2023',
    'Jharkhand Overseas Scholarship Scheme – 8 April 2023',
  ]],
  ['March 2023', [
    'LSE Graduate Support Scheme – 19 March 2023',
    'National Overseas Scholarship Scheme – 12 March 2023',
    'KC Mahindra Scholarships – 11 March 2023',
    'Narotam Sekhsaria Foundation Scholarship Programme – 4 March 2023',
    'Inlaks Shivdasani Foundation Scholarships – 1 March 2023',
  ]],
  ['February 2023', [
    'Aga Khan Foundation International Scholarship Programme – 26 February 2023',
    'JN Tata Endowment Loan Scholarship – 22 February 2023',
  ]],
  ['January 2023', [
    'Felix Scholarships – 19 January 2023',
    'Erasmus Mundus Scholarships – 21 January 2023',
  ]],
  ['December 2022', ['Scholarships for Indian Students at Oxford – 10 December 2022']],
  ['November 2022', [
    'Writing a PhD Research Proposal – 27 November 2022',
    'Weidenfeld-Hoffmann Scholarship – 26 November 2022',
    'Commonwealth Shared Scholarships – 23 November 2022',
    'Navigating Applications as a Person with Disabilities – 19 November 2022',
  ]],
  ['October 2022', [
    'Gates Cambridge Scholarship – 30 October 2022',
    'Writing your SoP / Personal Statements – 23 October 2022',
    'Scholarships & Funding for PhDs – 22 October 2022',
    'Writing your CV – 16 October 2022',
    'Applying for PhDs in Asia Pacific – 16 October 2022',
    "Applying for Master's Abroad – 15 October 2022",
    'Applying for PhDs in the US – 9 October 2022',
    'Overview of PhD Applications – 2 October 2022',
    'Chevening Scholarship – 1 October 2022',
  ]],
  ['September 2022', [
    'Studying Abroad for Kashmiri Students – 25 September 2022',
    'Commonwealth Scholarships – 24 September 2022',
    'Students from Northeast India – 4 September 2022',
  ]],
]

export default function ResourcesWorkshops(){
  return (
    <Page>
      <p className="text-xs uppercase tracking-widest text-neutral-500 mb-3">resources</p>
      <PageTitle>Resources from Online Workshops</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Project EduAccess regularly organises online public workshops on various aspects of university and
          scholarship applications. This page contains resources (recordings and presentations) from the
          public workshops we organised between September 2022 and June 2023.
        </p>
        <p>
          For resources from workshops organised after June 2023, please head to our YouTube channel:{' '}
          <a className="text-yellow-400 hover:text-yellow-300" href="https://www.youtube.com/@ProjectEduAccess" target="_blank" rel="noreferrer">
            youtube.com/@ProjectEduAccess
          </a>.
        </p>
      </Prose>

      <div className="mt-10 space-y-8">
        {WORKSHOPS.map(([month, items]) => (
          <div key={month}>
            <h3 className="text-xs uppercase tracking-widest text-yellow-400">{month}</h3>
            <ul className="mt-3 space-y-2">
              {items.map((w) => (
                <li key={w} className="text-sm text-neutral-300 border-l border-yellow-400/30 pl-4">{w}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </Page>
  )
}
