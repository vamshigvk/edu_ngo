import React from 'react'
import { Outlet } from 'react-router-dom'
import PublicHeader from '../public/PublicHeader'
import PublicFooter from '../public/PublicFooter'

export default function PublicLayout(){
  return (
    <div className="min-h-screen flex flex-col bg-black text-neutral-100">
      <PublicHeader />
      <main className="flex-1">
        <Outlet />
      </main>
      <PublicFooter />
    </div>
  )
}
