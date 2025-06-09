import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, BarChart3, Globe, Leaf } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <section className="text-center py-20">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          AI-Driven Supply Chain{' '}
          <span className="text-primary">Analysis</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Understand the complete journey of any product with comprehensive 
          supply chain analysis, carbon footprint calculations, and interactive visualizations.
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild size="lg">
            <Link href="/analyze">
              Start Analysis
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
          <Button variant="outline" size="lg" asChild>
            <Link href="/about">Learn More</Link>
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <h2 className="text-3xl font-bold text-center mb-12">
          Comprehensive Supply Chain Insights
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <Globe className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Global Supply Mapping</CardTitle>
              <CardDescription>
                Track materials and processes across the entire supply chain
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Visualize the complete journey from raw materials to finished products,
                including all intermediate steps and transportation routes.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Leaf className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Carbon Footprint Analysis</CardTitle>
              <CardDescription>
                Calculate environmental impact with precision
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Get detailed carbon footprint calculations based on real emission factors
                and industry-standard methodologies.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <BarChart3 className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Interactive Visualizations</CardTitle>
              <CardDescription>
                Explore data through engaging, interactive charts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Interactive charts, flow diagrams, and geographic maps make
                complex supply chain data easy to understand.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-20 bg-muted/30 rounded-lg">
        <h2 className="text-3xl font-bold mb-4">
          Ready to Analyze Your Product?
        </h2>
        <p className="text-lg text-muted-foreground mb-8 max-w-xl mx-auto">
          Get started with our AI-powered analysis tool and uncover the hidden
          complexities of your supply chain.
        </p>
        <Button asChild size="lg">
          <Link href="/analyze">
            Start Your Analysis
            <ArrowRight className="ml-2 h-4 w-4" />
          </Link>
        </Button>
      </section>
    </div>
  );
}