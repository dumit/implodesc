'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Eye, EyeOff, Key, AlertCircle, CheckCircle } from 'lucide-react';

interface APIKeyInputProps {
  sessionId: string | null;
  onKeysSet?: (services: Record<string, boolean>) => void;
}

export function APIKeyInput({ sessionId, onKeysSet }: APIKeyInputProps) {
  const [showKeys, setShowKeys] = useState(false);
  const [openaiKey, setOpenaiKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    if (!sessionId) {
      setStatus('error');
      setMessage('No active session. Please start an analysis first.');
      return;
    }

    if (!openaiKey && !anthropicKey) {
      setStatus('error');
      setMessage('Please provide at least one API key.');
      return;
    }

    setIsSubmitting(true);
    setStatus('idle');

    try {
      const apiKeys: Record<string, string> = {};
      if (openaiKey) apiKeys.openai = openaiKey;
      if (anthropicKey) apiKeys.anthropic = anthropicKey;

      const response = await fetch('http://127.0.0.1:8001/api/v1/analysis/api-keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          api_keys: apiKeys
        })
      });

      if (!response.ok) {
        throw new Error('Failed to set API keys');
      }

      const data = await response.json();
      setStatus('success');
      setMessage(data.message);
      
      if (onKeysSet) {
        onKeysSet(data.services_available);
      }
    } catch (error) {
      console.error('Error setting API keys:', error);
      setStatus('error');
      setMessage('Failed to set API keys. Please check your keys and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClear = () => {
    setOpenaiKey('');
    setAnthropicKey('');
    setStatus('idle');
    setMessage('');
  };

  return (
    <Card className="border-dashed">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Key className="h-5 w-5" />
          Optional: Provide Your API Keys
        </CardTitle>
        <CardDescription>
          For enhanced AI-powered analysis, provide your own OpenAI or Anthropic API keys. 
          Without keys, we'll use basic analysis patterns.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="openai-key" className="text-sm font-medium">
              OpenAI API Key (Optional)
            </label>
            <div className="relative">
              <Input
                id="openai-key"
                type={showKeys ? "text" : "password"}
                placeholder="sk-..."
                value={openaiKey}
                onChange={(e) => setOpenaiKey(e.target.value)}
                disabled={isSubmitting}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3"
                onClick={() => setShowKeys(!showKeys)}
              >
                {showKeys ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="anthropic-key" className="text-sm font-medium">
              Anthropic API Key (Optional)
            </label>
            <div className="relative">
              <Input
                id="anthropic-key"
                type={showKeys ? "text" : "password"}
                placeholder="your-anthropic-key..."
                value={anthropicKey}
                onChange={(e) => setAnthropicKey(e.target.value)}
                disabled={isSubmitting}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3"
                onClick={() => setShowKeys(!showKeys)}
              >
                {showKeys ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
          </div>
        </div>

        {/* Status Message */}
        {message && (
          <div className={`flex items-center gap-2 p-3 rounded-lg text-sm ${
            status === 'success' 
              ? 'bg-green-50 text-green-800' 
              : status === 'error'
              ? 'bg-red-50 text-red-800'
              : 'bg-blue-50 text-blue-800'
          }`}>
            {status === 'success' && <CheckCircle className="h-4 w-4" />}
            {status === 'error' && <AlertCircle className="h-4 w-4" />}
            {message}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button 
            onClick={handleSubmit}
            disabled={isSubmitting || (!openaiKey && !anthropicKey)}
            className="flex-1"
          >
            {isSubmitting ? 'Setting Keys...' : 'Set API Keys'}
          </Button>
          
          {(openaiKey || anthropicKey) && (
            <Button 
              variant="outline" 
              onClick={handleClear}
              disabled={isSubmitting}
            >
              Clear
            </Button>
          )}
        </div>

        {/* Information */}
        <div className="text-xs text-muted-foreground space-y-1">
          <p>• API keys are stored temporarily for your session only</p>
          <p>• Keys are not saved permanently or shared</p>
          <p>• Get OpenAI keys at: <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="underline">platform.openai.com</a></p>
          <p>• Get Anthropic keys at: <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer" className="underline">console.anthropic.com</a></p>
        </div>
      </CardContent>
    </Card>
  );
}