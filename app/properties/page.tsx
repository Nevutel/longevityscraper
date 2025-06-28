'use client'

import { useState, useEffect } from 'react'
import { PropertySearch } from '../../components/PropertySearch'
import { PropertyCard } from '../../components/PropertyCard'
import { Button } from '../../components/ui/button'
import { Card, CardContent } from '../../components/ui/card'
import { Loader2, ChevronLeft, ChevronRight } from 'lucide-react'

interface Property {
  id: string
  title: string
  description: string
  priceUsd: number
  cryptoAmount?: number
  cryptoCurrency?: string
  address: string
  city: string
  country: string
  type: string
  propertyType: string
  bedrooms?: number
  bathrooms?: number
  squareFeet?: number
  images?: string[]
  createdAt: string
  updatedAt: string
}

export default function PropertiesPage() {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({})

  useEffect(() => {
    fetchProperties()
  }, [currentPage, searchQuery, filters])

  const fetchProperties = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/properties?page=${currentPage}&search=${searchQuery}`)
      const data = await response.json()
      setProperties(data.properties || [])
      setTotalPages(data.totalPages || 1)
    } catch (error) {
      console.error('Error fetching properties:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    setCurrentPage(1)
  }

  const handleFilter = (newFilters: any) => {
    setFilters(newFilters)
    setCurrentPage(1)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Properties</h1>
      
      <PropertySearch onSearch={handleSearch} onFilter={handleFilter} />
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {properties.map((property) => (
          <PropertyCard
            key={property.id}
            title={property.title}
            price={`$${property.priceUsd.toLocaleString()}`}
            location={`${property.city}, ${property.country}`}
            imageUrl={property.images?.[0]}
          />
        ))}
      </div>

      {properties.length === 0 && !loading && (
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-gray-500">No properties found.</p>
          </CardContent>
        </Card>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-4">
          <Button
            variant="outline"
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="h-4 w-4 mr-2" />
            Previous
          </Button>
          
          <span className="text-sm">
            Page {currentPage} of {totalPages}
          </span>
          
          <Button
            variant="outline"
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
          >
            Next
            <ChevronRight className="h-4 w-4 ml-2" />
          </Button>
        </div>
      )}
    </div>
  )
} 