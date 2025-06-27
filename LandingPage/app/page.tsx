import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
  Search,
  Database,
  TrendingUp,
  Shield,
  Zap,
  Brain,
  Heart,
  Activity,
  ChevronRight,
  Users,
  Clock,
  BarChart3,
} from "lucide-react"
import Image from "next/image"
import Link from "next/link"

export default function LongevityResearchLanding() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm bg-white/5">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">LongevityAI</span>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="#features" className="text-gray-300 hover:text-white transition-colors">
              Features
            </Link>
            <Link href="#research" className="text-gray-300 hover:text-white transition-colors">
              Research
            </Link>
            <Link href="#pricing" className="text-gray-300 hover:text-white transition-colors">
              Pricing
            </Link>
            <Link href="#about" className="text-gray-300 hover:text-white transition-colors">
              About
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Button variant="ghost" className="text-white hover:bg-white/10">
              Sign In
            </Button>
            <Button className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white">
              Get Started
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 blur-3xl"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center max-w-4xl mx-auto">
            <Badge className="mb-6 bg-emerald-500/20 text-emerald-300 border-emerald-500/30">
              <Zap className="w-4 h-4 mr-2" />
              AI-Powered Research Aggregation
            </Badge>
            <h1 className="text-5xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Unlock the Future of
              <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                {" "}
                Longevity Research
              </span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 leading-relaxed">
              Advanced AI webscraper that aggregates cutting-edge medical research from leading institutions worldwide.
              Stay ahead of breakthrough discoveries in anti-aging and longevity science.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <Button
                size="lg"
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white px-8 py-4 text-lg"
              >
                Start Free Trial
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-white/20 text-white hover:bg-white/10 px-8 py-4 text-lg bg-transparent"
              >
                Watch Demo
              </Button>
            </div>
            <div className="flex items-center justify-center space-x-8 text-gray-400">
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5" />
                <span>10,000+ Researchers</span>
              </div>
              <div className="flex items-center space-x-2">
                <Database className="w-5 h-5" />
                <span>500+ Sources</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="w-5 h-5" />
                <span>Real-time Updates</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Powerful Research Intelligence</h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Our advanced AI system continuously monitors and analyzes the latest breakthroughs in longevity research
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-lg flex items-center justify-center mb-4">
                  <Search className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">Intelligent Scraping</CardTitle>
                <CardDescription className="text-gray-300">
                  Advanced AI algorithms scan thousands of research papers, clinical trials, and medical journals daily
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mb-4">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">AI Analysis</CardTitle>
                <CardDescription className="text-gray-300">
                  Machine learning models identify key insights, trends, and breakthrough discoveries in longevity
                  research
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">Trend Prediction</CardTitle>
                <CardDescription className="text-gray-300">
                  Predictive analytics identify emerging research areas and potential breakthrough therapies
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-teal-500 to-green-500 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">Quality Filtering</CardTitle>
                <CardDescription className="text-gray-300">
                  Rigorous quality assessment ensures only peer-reviewed, high-impact research is included
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg flex items-center justify-center mb-4">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">Custom Dashboards</CardTitle>
                <CardDescription className="text-gray-300">
                  Personalized research dashboards tailored to your specific areas of interest and expertise
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="bg-white/5 border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all duration-300">
              <CardHeader>
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg flex items-center justify-center mb-4">
                  <Heart className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-white">Health Integration</CardTitle>
                <CardDescription className="text-gray-300">
                  Connect research findings to practical health applications and therapeutic interventions
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Research Highlights */}
      <section id="research" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Latest Research Insights</h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Stay updated with the most recent breakthroughs in longevity and anti-aging research
            </p>
          </div>
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div className="space-y-6">
              <Card className="bg-gradient-to-r from-emerald-500/10 to-cyan-500/10 border-emerald-500/20 backdrop-blur-sm">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-500/30">Cellular Aging</Badge>
                    <span className="text-sm text-gray-400">2 hours ago</span>
                  </div>
                  <CardTitle className="text-white">Breakthrough in Senescent Cell Removal</CardTitle>
                  <CardDescription className="text-gray-300">
                    New research from Harvard Medical School demonstrates a 40% improvement in cellular regeneration
                    using novel senolytic compounds.
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 border-purple-500/20 backdrop-blur-sm">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30">Gene Therapy</Badge>
                    <span className="text-sm text-gray-400">5 hours ago</span>
                  </div>
                  <CardTitle className="text-white">CRISPR Advances in Longevity Genes</CardTitle>
                  <CardDescription className="text-gray-300">
                    Stanford researchers successfully edited longevity-associated genes, showing promising results in
                    extending healthy lifespan in clinical trials.
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card className="bg-gradient-to-r from-orange-500/10 to-red-500/10 border-orange-500/20 backdrop-blur-sm">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge className="bg-orange-500/20 text-orange-300 border-orange-500/30">Metabolic Health</Badge>
                    <span className="text-sm text-gray-400">1 day ago</span>
                  </div>
                  <CardTitle className="text-white">NAD+ Boosting Compounds Show Promise</CardTitle>
                  <CardDescription className="text-gray-300">
                    Clinical trials reveal significant improvements in mitochondrial function and energy metabolism with
                    next-generation NAD+ precursors.
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 blur-2xl rounded-full"></div>
              <Image
                src="/placeholder.svg?height=500&width=600"
                alt="Research Visualization"
                width={600}
                height={500}
                className="relative z-10 rounded-2xl border border-white/10"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-4xl font-bold text-white">500+</div>
              <div className="text-gray-300">Research Sources</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-white">10,000+</div>
              <div className="text-gray-300">Papers Analyzed</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-white">50+</div>
              <div className="text-gray-300">Countries Covered</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-white">99.9%</div>
              <div className="text-gray-300">Uptime</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">Ready to Accelerate Your Longevity Research?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of researchers, clinicians, and biohackers who rely on our platform for the latest
              breakthroughs in anti-aging science.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
              <Input
                type="email"
                placeholder="Enter your email address"
                className="max-w-md bg-white/10 border-white/20 text-white placeholder:text-gray-400"
              />
              <Button
                size="lg"
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white px-8"
              >
                Start Free Trial
              </Button>
            </div>
            <p className="text-sm text-gray-400">No credit card required • 14-day free trial • Cancel anytime</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-lg flex items-center justify-center">
                  <Activity className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">LongevityAI</span>
              </div>
              <p className="text-gray-400">Advancing human longevity through AI-powered research intelligence.</p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    API
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Documentation
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Research</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Latest Studies
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Clinical Trials
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Biomarkers
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Interventions
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    About
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Blog
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-white/10 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">© 2024 LongevityAI. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link href="#" className="text-gray-400 hover:text-white transition-colors text-sm">
                Privacy Policy
              </Link>
              <Link href="#" className="text-gray-400 hover:text-white transition-colors text-sm">
                Terms of Service
              </Link>
              <Link href="#" className="text-gray-400 hover:text-white transition-colors text-sm">
                Cookie Policy
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
