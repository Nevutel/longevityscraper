import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Search, Bell, ChevronDown, ArrowRight, TrendingUp, Shield, Zap, Menu } from "lucide-react"
import Link from "next/link"

export default function ResearchHubLanding() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      {/* Header */}
      <header className="border-b border-gray-100 bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">R</span>
            </div>
            <div>
              <div className="font-bold text-gray-900 text-lg">ResearchHub</div>
              <div className="text-sm text-gray-500">Medical AI</div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <div className="flex items-center space-x-1 text-gray-700 hover:text-blue-600 cursor-pointer">
              <span>Research Areas</span>
              <ChevronDown className="w-4 h-4" />
            </div>
            <Link href="#sources" className="text-gray-700 hover:text-blue-600">
              Sources
            </Link>
            <Link href="#about" className="text-gray-700 hover:text-blue-600">
              About
            </Link>
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            <Search className="w-5 h-5 text-gray-500 cursor-pointer hover:text-blue-600" />
            <div className="relative">
              <Bell className="w-5 h-5 text-gray-500 cursor-pointer hover:text-blue-600" />
              <div className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full"></div>
            </div>
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-6">Subscribe</Button>
            <Menu className="w-5 h-5 text-gray-500 md:hidden cursor-pointer" />
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 lg:py-32">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-4xl mx-auto">
            {/* Badge */}
            <Badge className="mb-8 bg-blue-50 text-blue-600 border-blue-200 hover:bg-blue-100 px-4 py-2">
              <Zap className="w-4 h-4 mr-2" />
              Latest in Longevity Research
            </Badge>

            {/* Main Headline */}
            <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                Immortal Report
              </span>
              <br />
              <span className="text-gray-900">New Research Hub</span>
            </h1>

            {/* Description */}
            <p className="text-xl text-gray-600 mb-12 leading-relaxed max-w-3xl mx-auto">
              Stay informed with the latest breakthroughs in anti-aging, longevity, and senescence research. Curated
              summaries from top medical journals and research institutions worldwide.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg">
                Explore Research
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-gray-300 text-gray-700 hover:bg-gray-50 px-8 py-4 text-lg bg-transparent"
              >
                Subscribe to Updates
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="pb-20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <Card className="border border-gray-200 hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-8 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Daily Updates</h3>
                <p className="text-gray-600">
                  Fresh research findings delivered daily from leading institutions worldwide
                </p>
              </CardContent>
            </Card>

            <Card className="border border-gray-200 hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-8 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Peer Reviewed</h3>
                <p className="text-gray-600">
                  Only high-quality, peer-reviewed research from trusted scientific sources
                </p>
              </CardContent>
            </Card>

            <Card className="border border-gray-200 hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-8 text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Zap className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Summarized</h3>
                <p className="text-gray-600">Complex research simplified into digestible insights using advanced AI</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Research Areas Section */}
      <section className="py-20 bg-blue-50/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Research Areas</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Comprehensive coverage across all major longevity research domains
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {[
              "Cellular Senescence",
              "Gene Therapy",
              "Metabolic Health",
              "Stem Cell Research",
              "Biomarkers",
              "Clinical Trials",
              "Therapeutic Interventions",
              "Aging Mechanisms",
            ].map((area, index) => (
              <Card key={index} className="border border-gray-200 hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-2">{area}</h3>
                  <p className="text-sm text-gray-600">Latest research and breakthroughs</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center max-w-4xl mx-auto">
            <div className="space-y-2">
              <div className="text-3xl font-bold text-blue-600">500+</div>
              <div className="text-gray-600">Research Sources</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-blue-600">10,000+</div>
              <div className="text-gray-600">Papers Analyzed</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-blue-600">50+</div>
              <div className="text-gray-600">Countries</div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-blue-600">Daily</div>
              <div className="text-gray-600">Updates</div>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-20 bg-blue-600">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Stay Updated</h2>
            <p className="text-blue-100 mb-8 text-lg">
              Get the latest longevity research delivered to your inbox weekly
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <input
                type="email"
                placeholder="Enter your email address"
                className="px-4 py-3 rounded-lg border-0 text-gray-900 placeholder:text-gray-500 flex-1 max-w-md"
              />
              <Button className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3">Subscribe</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">R</span>
                </div>
                <div>
                  <div className="font-bold text-gray-900">ResearchHub</div>
                  <div className="text-sm text-gray-500">Medical AI</div>
                </div>
              </div>
              <p className="text-gray-600">Advancing longevity research through AI-powered insights.</p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Research</h3>
              <ul className="space-y-2 text-gray-600">
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Latest Studies
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Clinical Trials
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Biomarkers
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Interventions
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-600">
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    API
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Blog
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Help Center
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 mb-4">Company</h3>
              <ul className="space-y-2 text-gray-600">
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    About
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Contact
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-blue-600">
                    Privacy
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-200 mt-12 pt-8 text-center text-gray-600">
            <p>© 2024 ResearchHub Medical AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
