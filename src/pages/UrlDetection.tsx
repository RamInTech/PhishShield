import { motion } from "framer-motion";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Shield,
  Link,
  ArrowLeft,
  Bot,
  Zap,
  Eye,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Globe
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

const UrlDetection = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<{
    classification: 'safe' | 'phishing' | 'suspicious';
    confidence: number;
    threats: string[];
    analysis: string;
    domainInfo: {
      age: string;
      registrar: string;
      ssl: boolean;
    };
  } | null>(null);

const analyzeUrl = async () => {
    setIsAnalyzing(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/analyze/url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      setResult({
        classification: data.classification,
        confidence: data.confidence,
        threats: data.threats.map((t: any) => t.description),
        analysis: data.analysis,
        domainInfo: data.domain_info
      });
    } catch (error) {
      console.error('Error analyzing URL:', error);
      setResult(null);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getClassificationColor = (classification: string) => {
    switch (classification) {
      case 'safe':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'suspicious':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'phishing':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getClassificationIcon = (classification: string) => {
    switch (classification) {
      case 'safe':
        return <CheckCircle className="h-5 w-5 text-green-400" />;
      case 'suspicious':
        return <AlertTriangle className="h-5 w-5 text-yellow-400" />;
      case 'phishing':
        return <XCircle className="h-5 w-5 text-red-400" />;
      default:
        return <AlertTriangle className="h-5 w-5 text-gray-400" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5 relative overflow-hidden">
      {/* Animated background particles */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-primary/10 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [-20, 20, -20],
              x: [15, -15, 15],
              opacity: [0.2, 0.6, 0.2],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              delay: i * 0.3,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      {/* Navigation */}
      <motion.nav
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="relative z-10 flex items-center justify-between p-6"
      >
        <motion.div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => navigate('/')}
          whileHover={{ scale: 1.05 }}
        >
          <Shield className="h-8 w-8 text-primary" />
          <span className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            PhishShield
          </span>
        </motion.div>
        
        <Button
          onClick={() => navigate('/dashboard')}
          variant="outline"
          className="flex items-center gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Button>
      </motion.nav>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-6 py-8">
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold mb-4">
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              URL Phishing
            </span>
            <br />
            <span className="text-foreground">Detection</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Advanced ML-powered analysis for identifying malicious websites and phishing URLs
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Input Section */}
          <motion.div
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="bg-glass border-glass backdrop-blur-glass h-full">
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <Link className="h-6 w-6 text-primary" />
                  URL Analysis Input
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <Input
                    placeholder="Enter URL to analyze (e.g., https://example.com)"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="bg-background/50 border-border/50 text-lg p-4"
                  />
                  
                  {url && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="p-4 bg-muted/20 rounded-lg border border-border/30"
                    >
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Globe className="h-4 w-4" />
                        Preview: {url}
                      </div>
                    </motion.div>
                  )}
                </div>

                <Button
                  onClick={analyzeUrl}
                  disabled={isAnalyzing || !url.trim()}
                  className="w-full bg-primary hover:bg-primary/90 disabled:opacity-50"
                  size="lg"
                >
                  {isAnalyzing ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="flex items-center gap-2"
                    >
                      <Bot className="h-5 w-5" />
                      Analyzing URL...
                    </motion.div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <Zap className="h-5 w-5" />
                      Analyze URL
                    </div>
                  )}
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <Card className="bg-glass border-glass backdrop-blur-glass h-full">
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <Eye className="h-6 w-6 text-primary" />
                  Analysis Results
                </CardTitle>
              </CardHeader>
              
              <CardContent>
                {!result && !isAnalyzing && (
                  <div className="text-center py-12 text-muted-foreground">
                    <Bot className="h-16 w-16 mx-auto mb-4 opacity-50" />
                    <p className="text-lg">Enter a URL to see AI analysis results</p>
                  </div>
                )}

                {isAnalyzing && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-12"
                  >
                    <motion.div
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="mb-6"
                    >
                      <Bot className="h-16 w-16 mx-auto text-primary" />
                    </motion.div>
                    <p className="text-lg font-medium mb-2">AI Analysis in Progress</p>
                    <p className="text-sm text-muted-foreground">
                      Scanning domain reputation and security indicators...
                    </p>
                  </motion.div>
                )}

                {result && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    {/* Classification Result */}
                    <div className="text-center p-6 rounded-lg border border-border/50">
                      <div className="flex items-center justify-center gap-3 mb-4">
                        {getClassificationIcon(result.classification)}
                        <Badge className={`px-3 py-1 text-lg ${getClassificationColor(result.classification)}`}>
                          {result.classification.toUpperCase()}
                        </Badge>
                      </div>
                      <div className="text-3xl font-bold text-foreground mb-2">
                        {result.confidence}% Confidence
                      </div>
                      <p className="text-muted-foreground">{result.analysis}</p>
                    </div>

                    {/* Domain Information */}
                    <div className="space-y-3">
                      <h4 className="font-semibold text-foreground">Domain Information:</h4>
                      <div className="grid grid-cols-1 gap-3">
                        <div className="flex justify-between p-3 bg-muted/20 rounded-lg">
                          <span className="text-muted-foreground">Domain Age:</span>
                          <span className="text-foreground font-medium">{result.domainInfo?.age ?? 'N/A'}</span>
                        </div>
                        <div className="flex justify-between p-3 bg-muted/20 rounded-lg">
                          <span className="text-muted-foreground">Registrar:</span>
                          <span className="text-foreground font-medium">{result.domainInfo?.registrar ?? 'N/A'}</span>
                        </div>
                        <div className="flex justify-between p-3 bg-muted/20 rounded-lg">
                          <span className="text-muted-foreground">SSL Certificate:</span>
                          <span className={`font-medium ${result.domainInfo?.ssl ? 'text-green-400' : 'text-red-400'}`}> 
                            {result.domainInfo?.ssl === true ? 'Valid' : result.domainInfo?.ssl === false ? 'Missing' : 'N/A'}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Threat Indicators */}
                    {result.threats.length > 0 && (
                      <div className="space-y-3">
                        <h4 className="font-semibold text-foreground">Risk Indicators:</h4>
                        {result.threats.map((threat, index) => (
                          <motion.div
                            key={index}
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            transition={{ delay: index * 0.1 }}
                            className="flex items-center gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20"
                          >
                            <AlertTriangle className="h-4 w-4 text-red-400 flex-shrink-0" />
                            <span className="text-sm text-foreground">{threat}</span>
                          </motion.div>
                        ))}
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex gap-3">
                      <Button
                        onClick={() => {
                          setResult(null);
                          setUrl('');
                        }}
                        variant="outline"
                        className="flex-1"
                      >
                        Analyze Another
                      </Button>
                      <Button
                        onClick={() => navigate('/dashboard')}
                        className="flex-1"
                      >
                        Save to Dashboard
                      </Button>
                    </div>
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default UrlDetection;