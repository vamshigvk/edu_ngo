import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import { Page, PageTitle, Prose, SectionTitle, LinkCard } from '../../components/public/ui'

export default function Resources(){
  const [resources, setResources] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load(){
      try {
        const { data } = await api.get('/api/public/resources', { params: { limit: 1000 } })
        setResources(Array.isArray(data) ? data : [])
      } catch {
        // Non-fatal: the static resource categories below still render.
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <Page>
      <PageTitle>resources</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          In addition to running the mentorship programme, Project EduAccess creates informational content for
          the benefit of prospective applicants. On this page, you will find resources that are helpful for
          your university and scholarship applications. This page will be updated with new content as and when
          available.
        </p>
      </Prose>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
        <LinkCard to="/resources/guides" title="Guides on Application Documents">
          Guides for writing your CV, personal statements, statements of purpose, research proposals and
          references/LoRs.
        </LinkCard>
        <LinkCard to="/resources/workshops" title="Resources from Online Workshops">
          Recordings and presentations from our public workshops on scholarships and university applications.
        </LinkCard>
        <LinkCard to="/resources/kashmir" title="Resources from In-person Workshop at Kashmir University">
          Training material from our three-day in-person workshop on studying abroad at the University of
          Kashmir.
        </LinkCard>
        <LinkCard to="/contact-us" title="Chevening Interview Guide">
          Our guide to preparing for the Chevening Scholarship interview.
        </LinkCard>
      </div>

      {/* Platform-managed resources (from the database), if any */}
      {!loading && resources.length > 0 && (
        <div className="mt-16">
          <SectionTitle>latest resources</SectionTitle>
          <ul className="mt-6 space-y-3">
            {resources.map((r) => (
              <li key={r.id} className="border border-yellow-400/30 rounded-md p-4">
                <a href={r.url || '#'} target="_blank" rel="noreferrer" className="text-yellow-400 hover:text-yellow-300 font-medium">
                  {r.title}
                </a>
                {r.type && <span className="ml-2 text-[10px] uppercase tracking-widest text-neutral-500">{r.type}</span>}
                {r.description && <p className="mt-1 text-sm text-neutral-400">{r.description}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </Page>
  )
}
