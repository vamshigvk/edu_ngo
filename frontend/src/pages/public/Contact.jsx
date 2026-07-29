import React, { useState } from 'react'
import { Page, PageTitle, SectionTitle, Prose, Button } from '../../components/public/ui'

export default function Contact(){
  const [email, setEmail] = useState('')
  const [done, setDone] = useState(false)

  return (
    <Page>
      <PageTitle>stay updated with the latest opportunities</PageTitle>
      <Prose className="mt-8 max-w-3xl">
        <p>
          Join our community and receive information about scholarships, fellowships, workshops and other
          opportunities right in your inbox.
        </p>
      </Prose>

      <form
        className="mt-6 flex flex-col sm:flex-row gap-3 max-w-xl"
        onSubmit={(e) => { e.preventDefault(); setDone(true) }}
      >
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email here"
          className="flex-1 bg-neutral-900 border border-yellow-400/40 rounded px-4 py-3 text-neutral-100 outline-none focus:border-yellow-400"
        />
        <Button type="submit">sign up</Button>
      </form>
      {done && <p className="mt-3 text-sm text-yellow-400">Thanks — you're on the list!</p>}

      <div className="mt-14 grid grid-cols-1 sm:grid-cols-3 gap-8">
        <div>
          <SectionTitle>collaborate with us</SectionTitle>
          <Prose className="mt-3">
            <p>
              We believe in working together to make a difference. If you are interested in collaborating with
              us, get in touch now.
            </p>
          </Prose>
          <a className="mt-3 inline-block text-yellow-400 hover:text-yellow-300 text-sm" href="mailto:info@projecteduaccess.com">click to get in touch</a>
        </div>
        <div>
          <SectionTitle>social with us</SectionTitle>
          <Prose className="mt-3">
            <p>Connect with us on Instagram, Facebook, Twitter and LinkedIn for regular posts, updates, and a lot more!</p>
          </Prose>
        </div>
        <div>
          <SectionTitle>looking for support</SectionTitle>
          <Prose className="mt-3">
            <p>We offer several resources to support individuals from marginalised backgrounds. If you need additional support, we're an email away!</p>
          </Prose>
          <a className="mt-3 inline-block text-yellow-400 hover:text-yellow-300 text-sm" href="mailto:info@projecteduaccess.com">click to get in touch</a>
        </div>
      </div>
    </Page>
  )
}
