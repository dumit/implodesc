'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ArrowLeft, Loader2, Search } from 'lucide-react';
import Link from 'next/link';
import { APIKeyInput } from '@/components/APIKeyInput';
import { SupplyChainVisualization } from '@/components/SupplyChainVisualization';

export default function AnalyzePage() {
  const [itemName, setItemName] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [clarifications, setClarifications] = useState<any[]>([]);
  const [clarificationAnswers, setClarificationAnswers] = useState<Record<string, string>>({});
  const [sessionId, setSessionId] = useState<string>('');
  const [step, setStep] = useState<'input' | 'clarifications' | 'results'>('input');
  const [availableServices, setAvailableServices] = useState<Record<string, boolean>>({});
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const handleStartAnalysis = async () => {
    if (!itemName.trim()) return;
    
    setIsAnalyzing(true);
    
    try {
      const response = await fetch('http://127.0.0.1:8001/api/v1/analysis/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: {
            item_name: itemName,
            description: `Analysis of ${itemName}`,
            quantity: 1
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to start analysis');
      }

      const data = await response.json();
      setSessionId(data.session_id);
      setClarifications(data.clarifications);
      setStep('clarifications');
    } catch (error) {
      console.error('Error starting analysis:', error);
      alert('Failed to start analysis. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSubmitClarifications = async () => {
    if (!sessionId) return;
    
    setIsAnalyzing(true);
    
    try {
      // Submit clarifications
      const clarificationsList = clarifications.map(q => ({
        question_id: q.id,
        answer: clarificationAnswers[q.id] || ''
      }));

      const response = await fetch('http://127.0.0.1:8001/api/v1/analysis/clarify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          clarifications: clarificationsList
        })
      });

      if (!response.ok) {
        throw new Error('Failed to submit clarifications');
      }

      // Wait for analysis to complete, then get results
      const resultResponse = await fetch(`http://127.0.0.1:8001/api/v1/analysis/${sessionId}/result`);
      
      if (!resultResponse.ok) {
        throw new Error('Failed to get analysis results');
      }

      const resultData = await resultResponse.json();
      setAnalysisResult(resultData);
      setStep('results');
    } catch (error) {
      console.error('Error submitting clarifications:', error);
      alert('Failed to complete analysis. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
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
        {step === 'input' && (
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
            
            {/* AI Services Status */}
            {sessionId && Object.keys(availableServices).length > 0 && (
              <div className="text-xs text-center text-muted-foreground mt-2">
                Available AI services: {' '}
                {availableServices.openai && <span className="text-green-600">OpenAI</span>}
                {availableServices.openai && availableServices.anthropic && ', '}
                {availableServices.anthropic && <span className="text-green-600">Anthropic</span>}
                {!availableServices.openai && !availableServices.anthropic && 
                  <span className="text-orange-600">Mock analysis (provide API keys for AI)</span>
                }
              </div>
            )}
          </CardContent>
        </Card>
        )}

        {step === 'clarifications' && (
        <Card>
          <CardHeader>
            <CardTitle>Clarification Questions</CardTitle>
            <CardDescription>
              Please answer these questions to help us provide a more accurate analysis of {itemName}.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {clarifications.map((q) => (
              <div key={q.id} className="space-y-2">
                <label className="text-sm font-medium">
                  {q.question} {q.required && <span className="text-red-500">*</span>}
                </label>
                {q.options ? (
                  <select 
                    className="w-full p-2 border rounded-md"
                    value={clarificationAnswers[q.id] || ''}
                    onChange={(e) => setClarificationAnswers(prev => ({
                      ...prev,
                      [q.id]: e.target.value
                    }))}
                  >
                    <option value="">Select an option...</option>
                    {q.options.map((option: string) => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                ) : (
                  <Input 
                    placeholder="Enter your answer..." 
                    value={clarificationAnswers[q.id] || ''}
                    onChange={(e) => setClarificationAnswers(prev => ({
                      ...prev,
                      [q.id]: e.target.value
                    }))}
                  />
                )}
              </div>
            ))}
            
            <div className="flex gap-2 pt-4">
              <Button variant="outline" onClick={() => setStep('input')} disabled={isAnalyzing}>
                Back
              </Button>
              <Button onClick={handleSubmitClarifications} className="flex-1" disabled={isAnalyzing}>
                {isAnalyzing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  'Continue Analysis'
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
        )}

        {step === 'results' && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
            <CardDescription>
              Supply chain analysis for {itemName}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {analysisResult ? (
                <>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h3 className="font-semibold text-green-800">Analysis Complete!</h3>
                    <p className="text-green-700">
                      Session ID: {sessionId}
                    </p>
                  </div>

                  {/* Supply Chain Visualization */}
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-semibold mb-4">Supply Chain Flow</h4>
                    <SupplyChainVisualization analysisResult={analysisResult} />
                  </div>

                  {/* Environmental Impact */}
                  {analysisResult.analysis_result?.environmental_impact && (
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold mb-2">Environmental Impact</h4>
                      <p><strong>Carbon Footprint:</strong> {analysisResult.analysis_result.environmental_impact.total_carbon_footprint_kg} kg CO₂e</p>
                      <p><strong>Highest Impact Stage:</strong> {analysisResult.analysis_result.environmental_impact.highest_impact_stage}</p>
                      {analysisResult.analysis_result.environmental_impact.improvement_opportunities?.length > 0 && (
                        <div className="mt-2">
                          <strong>Improvement Opportunities:</strong>
                          <ul className="list-disc list-inside mt-1">
                            {analysisResult.analysis_result.environmental_impact.improvement_opportunities.map((opp: string, idx: number) => (
                              <li key={idx} className="text-sm">{opp}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {/* AI Analysis Summary */}
                  {analysisResult.analysis_result?.summary && (
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold mb-2">AI Analysis Summary</h4>
                      <pre className="text-xs bg-gray-50 p-2 rounded overflow-auto max-h-96 whitespace-pre-wrap">
                        {analysisResult.analysis_result.summary}
                      </pre>
                    </div>
                  )}

                  {/* Clarifications Used */}
                  {analysisResult.clarifications_used && (
                    <div className="p-4 border rounded-lg">
                      <h4 className="font-semibold mb-2">Analysis Parameters</h4>
                      {Object.entries(analysisResult.clarifications_used).map(([key, value]) => (
                        <p key={key} className="text-sm"><strong>{key}:</strong> {value as string}</p>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <p className="text-yellow-700">Loading analysis results...</p>
                </div>
              )}
              
              <Button onClick={() => { 
                setStep('input'); 
                setItemName(''); 
                setAnalysisResult(null);
                setClarificationAnswers({});
                setClarifications([]);
                setSessionId('');
              }} className="w-full">
                Start New Analysis
              </Button>
            </div>
          </CardContent>
        </Card>
        )}

        {/* API Key Input */}
        {sessionId && step === 'input' && (
          <APIKeyInput 
            sessionId={sessionId}
            onKeysSet={(services) => setAvailableServices(services)}
          />
        )}

        {step === 'input' && (
        /* Example Products */
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
        )}
      </div>
    </div>
  );
}