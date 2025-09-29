import { motion } from "framer-motion";
import LoginForm from "@/components/LoginForm";
import FloatingOrbs from "@/components/FloatingOrbs";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-secondary flex items-center justify-center p-4 relative overflow-hidden">
      <FloatingOrbs />
      
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="w-full max-w-md z-10"
      >
        <LoginForm />
      </motion.div>
    </div>
  );
};

export default Index;
