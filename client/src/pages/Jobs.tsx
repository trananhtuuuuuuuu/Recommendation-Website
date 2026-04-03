import { useState } from "react";
import { Briefcase, MapPin, Clock, Shield, Filter, ChevronDown, Sparkles, Users, X, Loader2, ChevronUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from "react-router-dom";

const jobs = [
  {
    id: 1, title: "Senior Frontend Developer", company: "TechCorp", location: "Remote",
    type: "Full-time", salary: "$120K - $160K", posted: "2 days ago",
    skills: ["React", "TypeScript", "Tailwind"], privacyLevel: "High",
    description: "Build privacy-focused web applications with modern frameworks.",
  },
  {
    id: 2, title: "Data Privacy Engineer", company: "SecureAI", location: "San Francisco, CA",
    type: "Full-time", salary: "$140K - $180K", posted: "1 day ago",
    skills: ["Python", "Cryptography", "ML"], privacyLevel: "Maximum",
    description: "Design and implement privacy-preserving machine learning systems.",
  },
  {
    id: 3, title: "Backend Developer", company: "CloudShield", location: "New York, NY",
    type: "Contract", salary: "$100K - $130K", posted: "3 days ago",
    skills: ["Node.js", "PostgreSQL", "Docker"], privacyLevel: "High",
    description: "Develop secure APIs and microservices for enterprise clients.",
  },
  {
    id: 4, title: "UI/UX Designer", company: "DesignFirst", location: "Remote",
    type: "Part-time", salary: "$80K - $110K", posted: "5 days ago",
    skills: ["Figma", "User Research", "Prototyping"], privacyLevel: "Standard",
    description: "Create intuitive and accessible user interfaces for privacy tools.",
  },
  {
    id: 5, title: "Security Analyst", company: "CyberGuard", location: "Austin, TX",
    type: "Full-time", salary: "$110K - $150K", posted: "1 week ago",
    skills: ["Penetration Testing", "SIEM", "Compliance"], privacyLevel: "Maximum",
    description: "Monitor and analyze security threats across infrastructure.",
  },
];

const privacyColor: Record<string, string> = {
  Standard: "bg-warning/10 text-warning",
  High: "bg-primary/10 text-primary",
  Maximum: "bg-success/10 text-success",
};

// Mock AI analysis results
function generateMockAnalysis(jobId: number) {
  const analyses: Record<number, { matchPercent: number; pros: string[]; cons: string[]; suggestions: string[] }> = {
    1: {
      matchPercent: 87,
      pros: ["Strong React & TypeScript skills match", "Remote work aligns with your preference", "Salary range matches expectations"],
      cons: ["Tailwind experience is intermediate", "No privacy-specific project experience listed"],
      suggestions: ["Add privacy-related projects to your portfolio", "Highlight any Tailwind CSS certifications or advanced usage"],
    },
    2: {
      matchPercent: 62,
      pros: ["Python skills are a strong match", "Interest in ML aligns well"],
      cons: ["No cryptography experience listed on CV", "Location requires relocation or remote negotiation"],
      suggestions: ["Take a short course on differential privacy", "Add any data anonymization projects to your CV", "Mention any security-related coursework"],
    },
    3: {
      matchPercent: 78,
      pros: ["Node.js and PostgreSQL match your stack", "Docker experience is listed on your CV"],
      cons: ["Contract position — no long-term benefits", "Requires on-site presence in NY"],
      suggestions: ["Emphasize microservices architecture experience", "Highlight any API security best practices you've implemented"],
    },
    4: {
      matchPercent: 45,
      pros: ["Part-time flexibility is a plus"],
      cons: ["No Figma or UX research skills on your CV", "Design role differs significantly from your development background"],
      suggestions: ["Consider if a career pivot is intended", "If interested, build a small UX case study for your portfolio"],
    },
    5: {
      matchPercent: 71,
      pros: ["Security interest aligns with privacy focus", "Compliance knowledge is transferable"],
      cons: ["No penetration testing experience", "SIEM tools not listed on your CV"],
      suggestions: ["Get a CompTIA Security+ or CEH certification", "Add any vulnerability assessment experience to your profile"],
    },
  };
  return analyses[jobId] || { matchPercent: 50, pros: ["General skills match"], cons: ["Limited specific experience"], suggestions: ["Tailor your CV to this role"] };
}

export default function Jobs() {
  const navigate = useNavigate();
  const [compareAll, setCompareAll] = useState(false);
  const [comparingAll, setComparingAll] = useState(false);
  const [allResults, setAllResults] = useState<Record<number, ReturnType<typeof generateMockAnalysis>>>({});
  const [singleLoading, setSingleLoading] = useState<number | null>(null);
  const [singleResults, setSingleResults] = useState<Record<number, ReturnType<typeof generateMockAnalysis>>>({});
  const [expandedSuggestion, setExpandedSuggestion] = useState<number | null>(null);

  const handleCompareAll = () => {
    setComparingAll(true);
    setSingleResults({});
    setExpandedSuggestion(null);
    // Simulate AI processing
    setTimeout(() => {
      const results: Record<number, ReturnType<typeof generateMockAnalysis>> = {};
      jobs.forEach(job => { results[job.id] = generateMockAnalysis(job.id); });
      setAllResults(results);
      setCompareAll(true);
      setComparingAll(false);
    }, 1500);
  };

  const handleSingleSuggestion = (jobId: number) => {
    if (singleResults[jobId]) {
      setExpandedSuggestion(expandedSuggestion === jobId ? null : jobId);
      return;
    }
    setSingleLoading(jobId);
    setTimeout(() => {
      setSingleResults(prev => ({ ...prev, [jobId]: generateMockAnalysis(jobId) }));
      setExpandedSuggestion(jobId);
      setSingleLoading(null);
    }, 1000);
  };

  const getResult = (jobId: number) => compareAll ? allResults[jobId] : singleResults[jobId];

  const clearAll = () => {
    setCompareAll(false);
    setAllResults({});
    setSingleResults({});
    setExpandedSuggestion(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-bold text-foreground">Job Listings</h1>
          <p className="text-sm text-muted-foreground mt-1">Browse privacy-verified opportunities</p>
        </div>
        <div className="flex items-center gap-2">
          {(compareAll || Object.keys(singleResults).length > 0) && (
            <Button variant="ghost" size="sm" onClick={clearAll} className="gap-1 text-xs text-muted-foreground">
              <X className="w-3 h-3" /> Clear AI
            </Button>
          )}
          <Button
            onClick={handleCompareAll}
            disabled={comparingAll}
            className="gap-2 bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90"
          >
            {comparingAll ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            {comparingAll ? "Analyzing..." : "AI Compare All Jobs"}
          </Button>
          <Button variant="outline" className="gap-2">
            <Filter className="w-4 h-4" /> Filters <ChevronDown className="w-3 h-3" />
          </Button>
        </div>
      </div>

      <div className="space-y-3">
        {jobs.map((job, i) => {
          const result = getResult(job.id);
          const isExpanded = expandedSuggestion === job.id;

          return (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card rounded-xl p-5 hover:shield-glow transition-all group"
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <h3 className="font-display font-semibold text-foreground group-hover:text-primary transition-colors">
                      {job.title}
                    </h3>
                    <Badge className={`text-[10px] ${privacyColor[job.privacyLevel]}`}>
                      <Shield className="w-3 h-3 mr-1" /> {job.privacyLevel}
                    </Badge>
                    {result && (
                      <Badge className={`text-[10px] font-bold ${
                        result.matchPercent >= 80 ? "bg-success/15 text-success" :
                        result.matchPercent >= 60 ? "bg-warning/15 text-warning" :
                        "bg-destructive/15 text-destructive"
                      }`}>
                        <Sparkles className="w-3 h-3 mr-1" /> {result.matchPercent}% Match
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">{job.description}</p>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                    <span className="flex items-center gap-1"><Briefcase className="w-3 h-3" /> {job.company}</span>
                    <span className="flex items-center gap-1"><MapPin className="w-3 h-3" /> {job.location}</span>
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {job.posted}</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {job.skills.map(s => (
                      <span key={s} className="px-2 py-0.5 text-[10px] font-medium rounded-md bg-secondary text-secondary-foreground">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="text-right shrink-0 space-y-2">
                  <p className="font-display font-semibold text-foreground text-sm">{job.salary}</p>
                  <p className="text-xs text-muted-foreground">{job.type}</p>
                  <div className="flex flex-col gap-1.5 mt-2">
                    <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90">
                      Apply
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="gap-1 text-xs"
                      onClick={() => navigate(`/jobs/${job.id}/applicants`)}
                    >
                      <Users className="w-3 h-3" /> Applicants
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="gap-1 text-xs border-primary/30 text-primary hover:bg-primary/10"
                      disabled={singleLoading === job.id}
                      onClick={() => handleSingleSuggestion(job.id)}
                    >
                      {singleLoading === job.id ? (
                        <Loader2 className="w-3 h-3 animate-spin" />
                      ) : (
                        <Sparkles className="w-3 h-3" />
                      )}
                      {result ? (isExpanded ? "Hide" : "Show") + " Suggestions" : "AI Suggestion"}
                      {result && (isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />)}
                    </Button>
                  </div>
                </div>
              </div>

              {/* AI Suggestion Panel */}
              <AnimatePresence>
                {result && isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="mt-4 pt-4 border-t border-border grid sm:grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <h4 className="text-xs font-semibold text-success flex items-center gap-1">✅ Pros</h4>
                        <ul className="space-y-1">
                          {result.pros.map((p, idx) => (
                            <li key={idx} className="text-xs text-muted-foreground">• {p}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="space-y-2">
                        <h4 className="text-xs font-semibold text-destructive flex items-center gap-1">⚠️ Cons</h4>
                        <ul className="space-y-1">
                          {result.cons.map((c, idx) => (
                            <li key={idx} className="text-xs text-muted-foreground">• {c}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="space-y-2">
                        <h4 className="text-xs font-semibold text-primary flex items-center gap-1">💡 Suggestions</h4>
                        <ul className="space-y-1">
                          {result.suggestions.map((s, idx) => (
                            <li key={idx} className="text-xs text-muted-foreground">• {s}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
