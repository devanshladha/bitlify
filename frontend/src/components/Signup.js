"use client";

export default function Signup() {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="w-full max-w-[450px] glass backdrop-blur-3xl rounded-2xl p-8 shadow-2xl glass-border">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold mb-2 tracking-tight">Create account</h1>
                    <p className="text-slate-500 dark:text-slate-400 text-sm">Start creating branded short links for your business</p>
                </div>
                <div className="space-y-4">
                    <button className="w-full flex items-center justify-center gap-3 h-12 rounded-lg bg-gradient-to-r from-primary to-blue-600 hover:from-blue-600 hover:to-primary text-white font-bold transition-all shadow-lg shadow-primary/20">
                        Continue with Google
                    </button>
                    <div className="relative flex py-3 items-center">
                        <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                        <span className="flex-shrink mx-4 text-xs font-semibold text-slate-400 uppercase tracking-widest">OR</span>
                        <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                    </div>
                    <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
                        <div>
                            <label className="block text-sm font-semibold mb-2 text-slate-700 dark:text-slate-300" htmlFor="name">Full Name</label>
                            <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="name" placeholder="Jane Doe" type="text" />
                        </div>
                        <div>
                            <label className="block text-sm font-semibold mb-2 text-slate-700 dark:text-slate-300" htmlFor="email">Email Address</label>
                            <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="email" placeholder="name@company.com" type="email" />
                        </div>
                        <div>
                            <label className="block text-sm font-semibold mb-2 text-slate-700 dark:text-slate-300" htmlFor="password">Password</label>
                            <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="password" placeholder="••••••••" type="password" />
                        </div>
                        <button className="w-full h-12 bg-primary hover:bg-primary/90 text-white rounded-lg font-bold text-lg transition-all shadow-xl shadow-primary/10 mt-2" type="submit">
                            Sign Up
                        </button>
                    </form>
                </div>
                <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 text-center">
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                        Already have an account?
                        <a className="text-primary font-bold hover:underline ml-1" href="/auth/signin">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
