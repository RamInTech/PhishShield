import { motion } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  Shield,
  Mail,
  Globe,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  XCircle,
  BarChart3,
  Activity,
  ArrowLeft,
  RefreshCw
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const Dashboard = () => {
  const navigate = useNavigate();
  const [isScanning, setIsScanning] = useState(false);
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Chart animation will be handled by framer-motion
  }, []);

  const recentScans = [
    {
      id: 1,
      type: "email",
      subject: "Urgent: Account Verification Required",
      classification: "phishing",
      confidence: 98.5,
      timestamp: "2 minutes ago"
    },
    {
      id: 2,
      type: "url",
      url: "secure-banking-update.com",
      classification: "phishing",
      confidence: 94.2,
      timestamp: "5 minutes ago"
    },
    {
      id: 3,
      type: "email",
      subject: "Weekly Newsletter",
      classification: "safe",
      confidence: 99.1,
      timestamp: "8 minutes ago"
    },
    {
      id: 4,
      type: "url",
      url: "google.com",
      classification: "safe",
      confidence: 99.9,
      timestamp: "12 minutes ago"
    }
  ];

  const getClassificationIcon = (classification: string) => {
    switch (classification) {
      case "safe":
        return <CheckCircle className="h-4 w-4 text-green-400" />;
      case "suspicious":
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />;
      case "phishing":
      case "spam":
        return <XCircle className="h-4 w-4 text-red-400" />;
      default:
        return <AlertTriangle className="h-4 w-4 text-gray-400" />;
    }
  };

  const getClassificationColor = (classification: string) => {
    switch (classification) {
      case "safe":
        return "bg-green-400/10 text-green-400 border-green-400/20";
      case "suspicious":
        return "bg-yellow-400/10 text-yellow-400 border-yellow-400/20";
      case "phishing":
      case "spam":
        return "bg-red-400/10 text-red-400 border-red-400/20";
      default:
        return "bg-gray-400/10 text-gray-400 border-gray-400/20";
    }
  };

  const handleScan = () => {
    setIsScanning(true);
    setTimeout(() => setIsScanning(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-secondary">
      {/* Header */}
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="border-b border-border/50 bg-glass backdrop-blur-glass"
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate('/')}
                className="hover:bg-accent"
              >
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div className="flex items-center gap-3">
                <Shield className="h-8 w-8 text-primary" />
                <div>
                  <h1 className="text-2xl font-bold text-foreground">PhishShield Dashboard</h1>
                  <p className="text-sm text-muted-foreground">Real-time threat monitoring</p>
                </div>
              </div>
            </div>
            
            <Button
              onClick={handleScan}
              disabled={isScanning}
              className="bg-primary hover:bg-primary/90"
            >
              {isScanning ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Activity className="h-4 w-4 mr-2" />
              )}
              {isScanning ? 'Scanning...' : 'Run Scan'}
            </Button>
          </div>
        </div>
      </motion.header>

      <div className="container mx-auto px-6 py-8">
        {/* Stats Overview */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="grid md:grid-cols-4 gap-6 mb-8"
        >
          {[
            { label: "Total Scans Today", value: "1,247", icon: Activity, trend: "+12.3%" },
            { label: "Threats Blocked", value: "89", icon: Shield, trend: "+5.2%" },
            { label: "Emails Analyzed", value: "892", icon: Mail, trend: "+8.1%" },
            { label: "URLs Checked", value: "355", icon: Globe, trend: "+15.7%" }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              whileHover={{ y: -5 }}
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 bg-glass border-glass backdrop-blur-glass">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                    <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                    <p className="text-sm text-green-400 flex items-center gap-1">
                      <TrendingUp className="h-3 w-3" />
                      {stat.trend}
                    </p>
                  </div>
                  <stat.icon className="h-8 w-8 text-primary" />
                </div>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Recent Activity */}
          <motion.div
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-2"
          >
            <Card className="p-6 bg-glass border-glass backdrop-blur-glass">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-foreground">Recent Scans</h2>
                <Badge variant="outline" className="text-primary border-primary/20">
                  Live
                </Badge>
              </div>
              
              <div className="space-y-4">
                {recentScans.map((scan, index) => (
                  <motion.div
                    key={scan.id}
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border border-border/50 hover:bg-accent/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      {scan.type === "email" ? (
                        <Mail className="h-5 w-5 text-blue-400" />
                      ) : (
                        <Globe className="h-5 w-5 text-green-400" />
                      )}
                      <div>
                        <p className="font-medium text-foreground">
                          {scan.type === "email" ? scan.subject : scan.url}
                        </p>
                        <p className="text-sm text-muted-foreground">{scan.timestamp}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <div className="flex items-center gap-1">
                          {getClassificationIcon(scan.classification)}
                          <Badge className={getClassificationColor(scan.classification)}>
                            {scan.classification}
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">
                          {scan.confidence}% confidence
                        </p>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </Card>
          </motion.div>

          {/* Threat Analysis */}
          <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="space-y-6"
          >
            {/* Classification Breakdown */}
            <Card className="p-6 bg-glass border-glass backdrop-blur-glass">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Today's Classifications
              </h3>
              
              <div className="space-y-4">
                {[
                  { label: "Safe", count: 1089, percentage: 87.3, color: "bg-green-400" },
                  { label: "Spam", count: 79, percentage: 6.3, color: "bg-yellow-400" },
                  { label: "Phishing", count: 79, percentage: 6.4, color: "bg-red-400" }
                ].map((item, index) => (
                  <motion.div
                    key={item.label}
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ delay: 0.8 + index * 0.1 }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-foreground">{item.label}</span>
                      <span className="text-sm text-muted-foreground">{item.count}</span>
                    </div>
                    <Progress value={item.percentage} className="h-2" />
                  </motion.div>
                ))}
              </div>
            </Card>

            {/* Security Score */}
            <Card className="p-6 bg-glass border-glass backdrop-blur-glass">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Security Score
              </h3>
              
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 1, type: "spring", stiffness: 200 }}
                  className="relative w-32 h-32 mx-auto mb-4"
                >
                  <svg className="w-32 h-32 transform -rotate-90">
                    <circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="none"
                      className="text-border"
                    />
                    <motion.circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="8"
                      fill="none"
                      strokeLinecap="round"
                      className="text-primary"
                      initial={{ strokeDasharray: "0 351.86" }}
                      animate={{ strokeDasharray: "320.5 351.86" }}
                      transition={{ delay: 1.2, duration: 2 }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-2xl font-bold text-foreground">91%</span>
                  </div>
                </motion.div>
                
                <p className="text-sm text-muted-foreground">
                  Excellent protection level
                </p>
              </div>
            </Card>

            {/* Quick Actions */}
            <Card className="p-6 bg-glass border-glass backdrop-blur-glass">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Quick Actions
              </h3>
              
              <div className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <BarChart3 className="h-4 w-4 mr-2" />
                  View Detailed Reports
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Mail className="h-4 w-4 mr-2" />
                  Gmail Integration
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Shield className="h-4 w-4 mr-2" />
                  Security Settings
                </Button>
              </div>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;