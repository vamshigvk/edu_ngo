import React from 'react'
import { HeroRuleTitle, Page, LinkCard, Button, Stat } from '../../components/public/ui'

const STATS = [
  { value: '2,500+', label: 'mentees supported' },
  { value: '600+', label: 'mentors from top universities' },
  { value: '300,000+', label: 'hours of mentorship' },
  { value: '800+', label: 'admissions to top universities' },
  { value: '120+', label: 'scholarships' },
  { value: '₹82,500,000+', label: 'worth of scholarships' },
]

const TILES = [
  { title: 'about us', to: '/about-us', text: 'We are a non-profit aimed at increasing inclusivity in education & opportunities.' },
  { title: 'our work', to: '/our-work', text: 'Free mentorship programmes across India, Sri Lanka and Afghanistan.' },
  { title: 'resources', to: '/resources', text: 'Guides and workshop recordings to support your university and scholarship applications.' },
  { title: 'advocacy', to: '/advocacy', text: 'We advocate to make higher education and opportunities truly accessible for all.' },
]

export default function Home(){
  return (
    <div>
      {/* Hero */}
      <section className="py-20 md:py-28 px-4">
        <div className="max-w-5xl mx-auto">
          <HeroRuleTitle>democratising access to education &amp; opportunities</HeroRuleTitle>
          <p className="mt-10 max-w-3xl mx-auto text-center text-lg text-neutral-300 leading-relaxed">
            We help improve access to higher education, leadership and professional opportunities for
            individuals from marginalized communities in the Global South.
          </p>
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <Button to="/apply/student">apply as a mentee</Button>
            <Button to="/apply/mentor" variant="ghost">become a mentor</Button>
          </div>
        </div>
      </section>

      {/* Stats band (from the site's impact promo) */}
      <section className="bg-yellow-400">
        <div className="max-w-6xl mx-auto px-4 py-12">
          <p className="text-center text-black font-medium mb-8">
            Applications to our India Graduate Mentorship Programme are now open.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
            {STATS.map((s) => <Stat key={s.label} value={s.value} label={s.label} />)}
          </div>
        </div>
      </section>

      {/* Four tiles */}
      <Page>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {TILES.map((t) => (
            <LinkCard key={t.title} to={t.to} title={t.title}>{t.text}</LinkCard>
          ))}
        </div>
      </Page>
    </div>
  )
}
