import { motion } from "framer-motion";
import { Shield, Mail, Globe, ArrowRight, CheckCircle, AlertTriangle, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";

const Homepage = () => {
  const navigate = useNavigate();
  const particlesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Particles will be animated with framer-motion instead
  }, []);

  const features = [
    {
      icon: Mail,
      title: "Email Classification",
      description: "Advanced ML models classify emails as ham, spam, phishing, or safe",
      color: "text-blue-400"
    },
    {
      icon: Globe,
      title: "URL Analysis",
      description: "Real-time website scanning for phishing, safe, or suspicious content",
      color: "text-green-400"
    },
    {
      icon: Shield,
      title: "Gmail Integration",
      description: "Seamless integration with Gmail for instant threat detection",
      color: "text-purple-400"
    }
  ];

  const stats = [
    { label: "Emails Analyzed", value: "2.5M+", icon: Mail },
    { label: "Threats Blocked", value: "98.7%", icon: Shield },
    { label: "False Positives", value: "<0.1%", icon: CheckCircle }
  ];

  return (
    <div className="min-h-screen bg-gradient-secondary relative overflow-hidden">
      {/* Animated background particles */}
      <div ref={particlesRef} className="absolute inset-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-primary/20 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [-30, 0, -30],
              x: [20, -20, 20],
              rotate: [0, 360],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              delay: i * 0.2,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      {/* Navigation */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="relative z-50 p-6"
      >
        <div className="container mx-auto flex items-center justify-between">
          <motion.div
            className="flex items-center gap-3"
            whileHover={{ scale: 1.05 }}
          >
            <Shield className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              PhishShield
            </span>
          </motion.div>
          
          <Button
            onClick={() => navigate('/dashboard')}
            className="bg-primary hover:bg-primary/90"
          >
            Dashboard
          </Button>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="relative z-10 container mx-auto px-6 py-20"
      >
        <div className="text-center max-w-4xl mx-auto">
          <motion.h1
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-6xl md:text-7xl font-bold mb-6"
          >
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              Advanced
            </span>
            <br />
            <span className="text-foreground">Phishing Detection</span>
          </motion.h1>

          <motion.p
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="text-xl text-muted-foreground mb-8 leading-relaxed"
          >
            Protect your organization with cutting-edge machine learning that detects
            phishing emails and malicious websites in real-time.
          </motion.p>

          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.9 }}
            className="flex gap-4 justify-center"
          >
            <Button
              size="lg"
              onClick={() => navigate('/email-detection')}
              className="bg-primary hover:bg-primary/90 group"
            >
              Analyze Email
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button
              size="lg"
              onClick={() => navigate('/url-detection')}
              className="bg-primary hover:bg-primary/90 group"
            >
              Analyze URL
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              onClick={() => navigate('/dashboard')}
            >
              View Dashboard
            </Button>
          </motion.div>
        </div>

        {/* Stats Cards */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.1 }}
          className="grid md:grid-cols-3 gap-6 mt-20"
        >
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              whileHover={{ y: -5 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <Card className="p-6 text-center bg-glass border-glass backdrop-blur-glass">
                <stat.icon className="h-8 w-8 mx-auto mb-3 text-primary" />
                <div className="text-3xl font-bold text-foreground mb-1">
                  {stat.value}
                </div>
                <div className="text-muted-foreground">{stat.label}</div>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </motion.section>

      {/* Features Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="relative z-10 container mx-auto px-6 py-20"
      >
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            Comprehensive Protection
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Multiple layers of AI-powered security to keep your organization safe
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ y: 50, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              whileHover={{ y: -10 }}
            >
              <Card className="p-8 h-full bg-glass border-glass backdrop-blur-glass">
                <feature.icon className={`h-12 w-12 mb-4 ${feature.color}`} />
                <h3 className="text-xl font-semibold mb-3 text-foreground">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Classification Preview */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        className="relative z-10 container mx-auto px-6 py-20"
      >
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            Real-time Classification
          </h2>
          <p className="text-xl text-muted-foreground">
            See how PhishShield categorizes threats instantly
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="space-y-4"
          >
            <h3 className="text-2xl font-semibold text-foreground mb-6">Email Classification</h3>
            {[
              { type: "Safe", icon: CheckCircle, color: "text-green-400", bg: "bg-green-400/10" },
              { type: "Spam", icon: AlertTriangle, color: "text-yellow-400", bg: "bg-yellow-400/10" },
              { type: "Phishing", icon: XCircle, color: "text-red-400", bg: "bg-red-400/10" }
            ].map((item, index) => (
              <motion.div
                key={item.type}
                initial={{ x: -50, opacity: 0 }}
                whileInView={{ x: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className={`flex items-center gap-3 p-4 rounded-lg ${item.bg} border border-border/50`}
              >
                <item.icon className={`h-5 w-5 ${item.color}`} />
                <span className="font-medium text-foreground">{item.type}</span>
              </motion.div>
            ))}
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.02 }}
            className="space-y-4"
          >
            <h3 className="text-2xl font-semibold text-foreground mb-6">URL Analysis</h3>
            {[
              { type: "Safe", icon: CheckCircle, color: "text-green-400", bg: "bg-green-400/10" },
              { type: "Suspicious", icon: AlertTriangle, color: "text-yellow-400", bg: "bg-yellow-400/10" },
              { type: "Phishing", icon: XCircle, color: "text-red-400", bg: "bg-red-400/10" }
            ].map((item, index) => (
              <motion.div
                key={item.type}
                initial={{ x: 50, opacity: 0 }}
                whileInView={{ x: 0, opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className={`flex items-center gap-3 p-4 rounded-lg ${item.bg} border border-border/50`}
              >
                <item.icon className={`h-5 w-5 ${item.color}`} />
                <span className="font-medium text-foreground">{item.type}</span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </motion.section>
    </div>
  );
};

export default Homepage;