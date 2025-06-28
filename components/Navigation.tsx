'use client'

import Link from 'next/link'
import { Button } from './ui/button'
import { Home, Building2, User, Wallet } from 'lucide-react'

export function Navigation() {
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Building2 className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">CryptoRealty</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-1 text-gray-700 hover:text-blue-600">
              <Home className="h-4 w-4" />
              <span>Home</span>
            </Link>
            
            <Link href="/properties" className="flex items-center space-x-1 text-gray-700 hover:text-blue-600">
              <Building2 className="h-4 w-4" />
              <span>Properties</span>
            </Link>

            <Link href="/wallet" className="flex items-center space-x-1 text-gray-700 hover:text-blue-600">
              <Wallet className="h-4 w-4" />
              <span>Wallet</span>
            </Link>

            <Link href="/profile" className="flex items-center space-x-1 text-gray-700 hover:text-blue-600">
              <User className="h-4 w-4" />
              <span>Profile</span>
            </Link>

            <Button className="bg-blue-600 hover:bg-blue-700">
              Connect Wallet
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
} 