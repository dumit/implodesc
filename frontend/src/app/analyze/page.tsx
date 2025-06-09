'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ArrowLeft, Loader2, Search } from 'lucide-react';
import Link from 'next/link';

export default function AnalyzePage() {
  const [itemName, setItemName] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleStartAnalysis = async () => {
    if (!itemName.trim()) return;
    
    setIsAnalyzing(true);
    // TODO: Implement actual analysis logic
    setTimeout(() => {
      setIsAnalyzing(false);
      // Navigate to results or clarification page
    }, 2000);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Link>
        </Button>
        <div>
          <h1 className="text-3xl font-bold">Supply Chain Analysis</h1>
          <p className="text-muted-foreground">
            Enter a product to analyze its complete supply chain
          </p>
        </div>
      </div>

      {/* Analysis Input */}
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              What would you like to analyze?
            </CardTitle>
            <CardDescription>
              Enter any product name to start the AI-driven supply chain analysis.
              We'll ask clarifying questions to provide the most accurate results.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="item-name" className="text-sm font-medium">
                Product Name
              </label>
              <Input
                id="item-name"
                placeholder="e.g., iPhone 15, Cotton T-shirt, Steel beam..."
                value={itemName}
                onChange={(e) => setItemName(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleStartAnalysis();
                  }
                }}
                disabled={isAnalyzing}
              />
            </div>
            
            <Button 
              onClick={handleStartAnalysis}
              disabled={!itemName.trim() || isAnalyzing}
              className="w-full"
              size="lg"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Starting Analysis...
                </>
              ) : (
                'Start Analysis'
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Example Products */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4">Popular Analyses</h3>
          <div className="grid gap-3">
            {[
              'Cotton T-shirt',
              'Smartphone',
              'Electric vehicle battery',
              'Steel construction beam',
              'Coffee beans',
              'Solar panel'
            ].map((example) => (
              <Button
                key={example}
                variant="outline"
                size="sm"
                onClick={() => setItemName(example)}
                disabled={isAnalyzing}
                className="justify-start"
              >
                {example}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}