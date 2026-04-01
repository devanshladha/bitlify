export default function Home() {
  return (
    
    <div className="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden pt-6">

      <main className="flex-1 flex flex-col">
        
        <section className="relative pt-24 pb-20 px-6 lg:pt-32 lg:pb-32 overflow-hidden">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-primary/10 blur-[120px] rounded-full pointer-events-none opacity-50"></div>
          <div className="max-w-4xl mx-auto text-center relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 mb-8">
              <span className="flex h-2 w-2 rounded-full bg-primary"></span>
              <span className="text-primary text-[10px] font-bold uppercase tracking-widest">New: Custom Domains</span>
            </div>
            <h1 className="text-5xl lg:text-7xl font-extrabold text-white mb-6 leading-[1.1] tracking-tight">
              Shorten Your Links, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-400">Amplify Your Impact</span>
            </h1>
            <p className="text-slate-400 text-lg lg:text-xl max-w-2xl mx-auto mb-10 leading-relaxed font-light">
              Transform long, cluttered URLs into powerful, trackable, and branded short links in seconds. Elevate your digital presence with enterprise-grade analytics.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
              <button className="w-full sm:w-auto px-8 py-4 bg-primary text-white font-bold rounded-xl glow-button text-lg">
                Get Started for Free
              </button>
              <button className="w-full sm:w-auto px-8 py-4 glass text-white font-bold rounded-xl hover:bg-white/5 transition-all text-lg flex items-center justify-center gap-2">
                View Demo <span className="material-symbols-outlined text-xl">arrow_right_alt</span>
              </button>
            </div>
            
            <div className="max-w-2xl mx-auto glass p-2 rounded-2xl shadow-2xl relative">
              <div className="flex flex-col sm:flex-row items-stretch gap-2">
                <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-white/5 rounded-xl border border-white/5 focus-within:border-primary/50 transition-all">
                  <span className="material-symbols-outlined text-slate-500">link</span>
                  <input className="bg-transparent border-none focus:outline-none focus:ring-0 text-white placeholder:text-slate-500 w-full text-sm lg:text-base" placeholder="Paste your long URL here..." type="text" />
                </div>
                <button className="bg-primary hover:bg-primary/90 text-white font-bold px-8 py-3 rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 group">
                  Shorten <span className="material-symbols-outlined text-xl group-hover:translate-x-1 transition-transform">bolt</span>
                </button>
              </div>
              <div className="absolute -bottom-10 left-0 right-0 text-center">
                <p className="text-slate-500 text-xs font-medium uppercase tracking-widest">No credit card required • Unlimited clicks</p>
              </div>
            </div>
          </div>
        </section>
        
        <section className="py-24 px-6 lg:px-20 bg-background-dark">
          <div className="max-w-7xl mx-auto">
            <div className="mb-16 text-center lg:text-left">
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4 tracking-tight">Powerful Features for Modern Links</h2>
              <p className="text-slate-400 max-w-xl">Every tool you need to manage, secure, and analyze your link's performance across the web.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              
              <div className="glass p-8 rounded-3xl hover:bg-white/[0.05] transition-all group border-white/[0.05]">
                <div className="bg-primary/10 w-12 h-12 rounded-2xl flex items-center justify-center mb-6 border border-primary/20 group-hover:bg-primary transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-white transition-colors">label</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Custom Aliases</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Create branded links that people trust and remember. Perfect for social bios and marketing campaigns.
                </p>
              </div>
              
              <div className="glass p-8 rounded-3xl hover:bg-white/[0.05] transition-all group border-white/[0.05]">
                <div className="bg-primary/10 w-12 h-12 rounded-2xl flex items-center justify-center mb-6 border border-primary/20 group-hover:bg-primary transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-white transition-colors">lock</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-3">PIN Protected</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Secure your sensitive links with password protection and gate your content effectively.
                </p>
              </div>
              
              <div className="glass p-8 rounded-3xl hover:bg-white/[0.05] transition-all group border-white/[0.05]">
                <div className="bg-primary/10 w-12 h-12 rounded-2xl flex items-center justify-center mb-6 border border-primary/20 group-hover:bg-primary transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-white transition-colors">bar_chart</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Real-time Analytics</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Track every click with deep insights into geographic location, device types, and referral sources.
                </p>
              </div>
              
              <div className="glass p-8 rounded-3xl hover:bg-white/[0.05] transition-all group border-white/[0.05]">
                <div className="bg-primary/10 w-12 h-12 rounded-2xl flex items-center justify-center mb-6 border border-primary/20 group-hover:bg-primary transition-colors">
                  <span className="material-symbols-outlined text-primary group-hover:text-white transition-colors">timer</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Link Expiry</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Set links to automatically expire after a specific date or a predetermined number of clicks.
                </p>
              </div>
            </div>
          </div>
        </section>
        
        <section className="py-24 px-6">
          <div className="max-w-5xl mx-auto glass rounded-[3rem] p-12 text-center border-primary/20 bg-gradient-to-b from-primary/[0.02] to-transparent">
            <h2 className="text-3xl lg:text-5xl font-bold text-white mb-6">Ready to scale your influence?</h2>
            <p className="text-slate-400 text-lg mb-10 max-w-xl mx-auto">Join thousands of creators and businesses already using Bitlify to optimize their digital footprint.</p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button className="bg-primary hover:bg-primary/90 text-white font-bold px-10 py-4 rounded-xl text-lg glow-button w-full sm:w-auto transition-all">
                Get Started Free
              </button>
              <button className="text-white font-bold px-10 py-4 rounded-xl text-lg hover:bg-white/5 w-full sm:w-auto transition-all">
                Contact Sales
              </button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
