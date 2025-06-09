import { auth } from '@clerk/nextjs';
import { redirect } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BarChart3, Plus, History } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { userId } = auth();

  if (!userId) {
    redirect('/sign-in');
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Manage your supply chain analyses and insights
          </p>
        </div>
        <Button asChild>
          <Link href="/analyze">
            <Plus className="h-4 w-4 mr-2" />
            New Analysis
          </Link>
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              Quick Start
            </CardTitle>
            <CardDescription>
              Start a new supply chain analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link href="/analyze">Start Analysis</Link>
            </Button>
          </CardContent>
        </Card>

        {/* Recent Analyses */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Recent Analyses
            </CardTitle>
            <CardDescription>
              View your recent supply chain analyses
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              No analyses yet. Start your first analysis to see results here.
            </p>
            <Button variant="outline" size="sm" disabled>
              View All
            </Button>
          </CardContent>
        </Card>

        {/* Analytics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Analytics
            </CardTitle>
            <CardDescription>
              View aggregated insights across analyses
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Analytics will appear once you complete analyses.
            </p>
            <Button variant="outline" size="sm" disabled>
              View Insights
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Getting Started */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Getting Started</CardTitle>
          <CardDescription>
            Learn how to make the most of Implodesc's supply chain analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                1
              </div>
              <div>
                <h4 className="font-medium">Start an Analysis</h4>
                <p className="text-sm text-muted-foreground">
                  Enter a product name to begin analyzing its supply chain
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                2
              </div>
              <div>
                <h4 className="font-medium">Provide Clarifications</h4>
                <p className="text-sm text-muted-foreground">
                  Answer AI-generated questions to improve analysis accuracy
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium">
                3
              </div>
              <div>
                <h4 className="font-medium">Explore Results</h4>
                <p className="text-sm text-muted-foreground">
                  View interactive visualizations and detailed insights
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}