import React from 'react'
import { Page, PageTitle, Prose, SectionTitle, LinkCard, Button } from '../../components/public/ui'

const BENEFITS = [
  'personalised 1:1 mentorship on all aspects of university and scholarship applications;',
  'access to a network of expert mentors who have pursued postgraduate studies abroad;',
  'mentee-only workshops on all aspects of university application processes, including identifying degrees/universities/funding avenues, drafting CVs, personal statements and writing samples, and preparing for interviews;',
  'tailored support programmes for scholarships;',
  'interview and English language support programmes;',
  'affinity-based psychosocial support, and more.',
]

const ELIGIBILITY = [
  'you have completed, or are in the final year of, an undergraduate degree at a college/university in India;',
  'you are planning to apply for a postgraduate degree (including PhD) abroad (e.g. UK, USA, Australia, Europe); and',
  'you are disadvantaged by social position, economic ability, and/or geography (or other similar factors).',
]

export default function IndiaProgramme(){
  return (
    <Page>
      <PageTitle>India Graduate Mentorship Programme</PageTitle>

      <SectionTitle className="mt-10">about the mentorship programme</SectionTitle>
      <Prose className="mt-4 max-w-3xl">
        <p>
          The India Graduate Mentorship Programme (IGMP) is a mentoring initiative that seeks to help Indian
          learners from marginalised communities apply to universities abroad for graduate studies (masters
          and PhD). We provide both technical (depending on the course/discipline of interest to the mentee)
          as well as affinity-based mentorship to support our mentees holistically. We help learners with
          university and funding/scholarship applications, and also provide capacity-building support.
        </p>
        <p>
          The IGMP, launched in 2022, has been a resounding success, witnessing remarkable growth and helping
          hundreds of students secure admissions to top universities and prestigious scholarships. Our
          mentees have clocked over 800 admission offers from top universities like the University of Oxford,
          Harvard University, University of Cambridge, Yale University, New York University, SOAS University of
          London, London School of Economics and Political Science, University College London, and Johns
          Hopkins University, among others — and won 120+ prestigious fully-funded scholarships including the
          Rhodes, Chevening, Commonwealth Shared, Felix, Inlaks, Clarendon, Weidenfeld-Hoffmann and Erasmus
          Mundus scholarships.
        </p>
      </Prose>

      <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl">
        <LinkCard to="/apply/student" title="mentees">
          Being a mentee at Project EduAccess can be a transformative opportunity. Get comprehensive support
          and free, personalised 1:1 mentorship from graduates of top foreign universities.
        </LinkCard>
        <LinkCard to="/apply/mentor" title="mentors">
          Mentoring at Project EduAccess can be a rewarding experience! Share your expertise to positively
          impact students from historically marginalised and disadvantaged communities.
        </LinkCard>
      </div>

      <SectionTitle className="mt-12">benefits</SectionTitle>
      <ul className="mt-4 space-y-2 text-neutral-300 leading-relaxed list-disc list-inside max-w-3xl">
        {BENEFITS.map((b, i) => <li key={i}>{b}</li>)}
      </ul>

      <SectionTitle className="mt-12">eligibility</SectionTitle>
      <p className="mt-4 text-neutral-300 max-w-3xl">You are eligible to apply if:</p>
      <ul className="mt-3 space-y-2 text-neutral-300 leading-relaxed list-disc list-inside max-w-3xl">
        {ELIGIBILITY.map((e, i) => <li key={i}>{e}</li>)}
      </ul>

      <SectionTitle className="mt-12">application process</SectionTitle>
      <Prose className="mt-4 max-w-3xl">
        <p>
          If you meet the eligibility criteria, we encourage you to apply to be a mentee by filling the
          application form. Before doing so, please have ready your personal information (contact details,
          address, family income, etc.), details of your educational background, and supporting information
          such as your CV, plans of higher education, and choice of courses and universities.
        </p>
        <p className="text-neutral-400 text-sm">
          The India Graduate Mentorship Programme is completely free of cost. If anyone asks you for money
          claiming to be associated with us, please report them immediately to info@projecteduaccess.com.
        </p>
      </Prose>

      <div className="mt-10 flex flex-wrap gap-4">
        <Button to="/apply/student">apply as a mentee</Button>
        <Button to="/apply/mentor" variant="ghost">sign up as a mentor</Button>
      </div>
    </Page>
  )
}
