import React from 'react'
import { Link } from 'react-router-dom'

function Hero(){
  return (
    <section className="bg-yellow-400 py-20">
      <div className="max-w-6xl mx-auto px-4 text-center">
        <h1 className="text-5xl font-bold text-black">Democratising access to education & opportunities</h1>
        <p className="mt-6 text-xl text-black">We help improve access to higher education, leadership and professional opportunities for individuals from marginalized communities in the Global South.</p>
        <div className="mt-8 flex justify-center gap-4">
          <Link to="/apply/student" className="px-8 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">Apply as Student</Link>
          <Link to="/apply/mentor" className="px-8 py-3 bg-black text-yellow-400 font-semibold rounded hover:bg-gray-900">Become a Mentor</Link>
        </div>
      </div>
    </section>
  )
}

export default function Home(){
  return (
    <div>
      <Hero />
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-3xl font-semibold text-black">Our Mission</h2>
        <p className="mt-4 text-lg text-gray-800">We work to democratise access to higher education so that all individuals have quality educational opportunities, and in turn, better avenues for personal and professional growth and holistic development.</p>
      </section>
    </div>
  )
}
