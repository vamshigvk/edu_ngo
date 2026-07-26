import React from 'react'

export default function About(){
  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="mb-12">
        <h1 className="text-5xl font-bold text-black">About Us</h1>
      </div>
      
      <div className="space-y-8 text-gray-800">
        <section>
          <p className="text-lg leading-relaxed">
            Launched in 2021, Project EduAccess is a non-profit initiative that aims to improve access to higher education for learners from marginalised communities in the Global South, and create opportunities for their professional and personal development. We currently operate in the South Asian countries of India, Sri Lanka and Afghanistan.
          </p>
        </section>

        <section>
          <p className="text-lg leading-relaxed">
            Both in South Asia and elsewhere, higher education institutions, leadership avenues and job opportunities are inaccessible to most potential learners due to entrenched fault lines of inequality in society. This lack of access may be the result of various barriers. Of these, issues tethered to systemic discrimination may require broad-based policy interventions from governments, institutions and employers. However, some other accessibility issues – particularly cost, information and dispositional barriers – can be resolved through concerted volunteer efforts. Therefore, through our tested volunteer model, we make modest attempts to address these barriers and improve inclusivity in education, leadership and professional opportunities.
          </p>
        </section>

        <section>
          <p className="text-lg leading-relaxed">
            We do this primarily by offering free mentorship support to marginalised South Asian learners (particularly those disadvantaged inter alia by social position, economic ability, and geography). We also advocate with public and private sector entities to make higher education accessible.
          </p>
        </section>

        <section className="bg-yellow-100 p-6 rounded-lg border-2 border-black">
          <h2 className="text-2xl font-bold text-black mb-4">Our Mission</h2>
          <p className="text-lg leading-relaxed text-black">
            To democratise access to higher education so that all individuals have quality educational opportunities, and in turn, better avenues for personal and professional growth and holistic development. We believe that concerted effort in this direction is a steppingstone to an equal society.
          </p>
        </section>
      </div>
    </div>
  )
}
