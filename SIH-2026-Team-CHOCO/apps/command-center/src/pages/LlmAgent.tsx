import { useState, useRef, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@sih/ui-kit';
import { Bot, Send, User, Loader2 } from 'lucide-react';

export function LlmAgent() {
  const [messages, setMessages] = useState([
    { role: 'user', content: 'Find all mule accounts that received money from victim ID CC-2026-0042 in the last 24 hours.' },
    { role: 'agent', content: 'I have queried the Neo4j intelligence graph. Found 3 Level-1 mule accounts linked to that victim:\n\n• **Acct 8829...441** (HDFC) - Received ₹45,000\n• **Acct 1102...993** (SBI) - Received ₹12,500\n• **Acct 7741...220** (ICICI) - Received ₹5,000\n\nReady for freeze commands.' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsTyping(true);
    
    // Simulate LLM delay and response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'agent', 
        content: `I've analyzed the pattern for "${userMsg}". The graph neural network indicates a 92% probability this is part of the broader Jamtara syndicate. I have escalated this to the Active Alerts feed.` 
      }]);
      setIsTyping(false);
    }, 2000);
  };

  return (
    <div className="space-y-6 max-w-[1200px] mx-auto h-[calc(100vh-140px)] flex flex-col">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight">AI Analyst</h1>
      </div>
      <Card className="flex-1 flex flex-col shadow-sm overflow-hidden border border-line">
        <CardHeader className="border-b border-line bg-surface-2/95 backdrop-blur-md pb-4">
          <CardTitle className="flex items-center text-accent">
            <Bot className="w-5 h-5 mr-2" />
            Intelligence Graph Agent
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4" ref={scrollRef}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm ${msg.role === 'user' ? 'bg-surface-2 border border-line' : 'bg-accent'}`}>
                {msg.role === 'user' ? <User className="w-4 h-4 text-muted" /> : <Bot className="w-4 h-4 text-white" />}
              </div>
              <div className={`p-3 rounded-lg text-sm max-w-[80%] whitespace-pre-wrap ${msg.role === 'user' ? 'bg-accent text-white shadow-sm' : 'bg-surface border border-line text-ink'}`}>
                {msg.content}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-accent flex items-center justify-center shrink-0 shadow-sm">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="bg-surface p-3 rounded-lg text-sm border border-line flex items-center text-muted">
                <Loader2 className="w-4 h-4 mr-2 animate-spin text-accent" />
                Graph agent is thinking...
              </div>
            </div>
          )}
        </CardContent>
        <div className="p-4 bg-surface-2/95 backdrop-blur-md border-t border-line flex gap-2">
          <input 
            type="text" 
            placeholder="Ask the AI to query the graph database..." 
            className="flex-1 bg-surface border border-line rounded-md px-4 py-2 text-sm text-ink focus:outline-none focus:border-accent"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isTyping}
          />
          <Button 
            variant="default" 
            className="shrink-0 bg-accent hover:bg-accent-2 text-white"
            onClick={handleSend}
            disabled={isTyping || !input.trim()}
          >
            <Send className="w-4 h-4 mr-2" /> Send
          </Button>
        </div>
      </Card>
    </div>
  );
}
