import React from 'react'
import { Page, PageTitle, Prose, SectionTitle, LinkCard } from '../../components/public/ui'

export default function India(){
  return (
    <Page>
      <PageTitle>india</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Improving access to higher education and creating opportunities of growth for learners from
          marginalised communities in India.
        </p>
      </Prose>

      <SectionTitle className="mt-12">our work</SectionTitle>
      <Prose className="mt-4 max-w-3xl">
        <p>
          At Project EduAccess - India, we are committed to the goal of empowering learners from marginalised
          and historically disadvantaged communities in India. We do this by working towards increasing their
          representation in higher education and creating opportunities for their personal and professional
          development.
        </p>
        <p>
          In 2022, we launched a large-scale graduate mentorship programme to support learners from
          marginalised groups with their applications to universities and scholarship bodies for postgraduate
          study. Over the last three years, we have mentored 2000+ mentees through a network of 600+ expert
          mentors. Our mentees have made it to top universities in the world, including the University of
          Oxford, University of Cambridge, Harvard University, Yale University, Columbia University, University
          of Melbourne, New York University, SOAS University of London, London School of Economics and
          Political Science, University College London, and Johns Hopkins University, among others. They have
          also won prestigious fully-funded scholarships like the Rhodes Scholarship, Chevening Scholarship,
          Commonwealth Shared Scholarship, Clarendon Scholarship, Weidenfeld-Hoffmann Scholarship, Felix
          Scholarship, Inlaks Scholarship, Charles Wallace India Trust Scholarship, and the Oxford-India
          Centre for Sustainable Development Scholarship, among others.
        </p>
      </Prose>

      <SectionTitle className="mt-12">programmes</SectionTitle>
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-6">
        <LinkCard to="/india-graduate-mentorship-programme" title="India Graduate Mentorship Programme">
          Flagship initiative to help Indian individuals from disadvantaged backgrounds apply for graduate
          studies and scholarships abroad, including universities in the UK, US, Europe and Australia.
        </LinkCard>
        <LinkCard to="/contact-us" title="PRISM Fellowship at NCBS">
          Promoting Research &amp; Inclusion in STEM through a fully-funded, residential research programme
          hosted at NCBS for life science students from disadvantaged backgrounds in India.
        </LinkCard>
        <LinkCard to="/contact-us" title="PRISM National Fellowship">
          Promoting Research &amp; Inclusion in STEM through a fully-funded, residential research programme at
          labs across India for life science students from disadvantaged backgrounds.
        </LinkCard>
      </div>
    </Page>
  )
}
