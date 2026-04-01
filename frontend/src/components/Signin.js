"use client";

export default function Signin() {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="w-full max-w-[450px] glass backdrop-blur-3xl rounded-2xl p-8 shadow-2xl glass-border">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold mb-2 tracking-tight">Welcome back</h1>
                    <p className="text-slate-500 dark:text-slate-400 text-sm">Sign in to manage your short links</p>
                </div>
                <div className="space-y-4">
                    <button className="w-full flex items-center justify-center gap-3 h-12 rounded-lg bg-gradient-to-r from-primary to-blue-600 hover:from-blue-600 hover:to-primary text-white font-bold transition-all shadow-lg shadow-primary/20">
                        <svg className="w-5 h-5" viewBox="0 0 24 24">
                            <path d="M21.35,11.1H12.18V13.83H18.69C18.36,17.64 15.19,19.27 12.19,19.27C8.92,19.27 6.23,16.59 6.23,13.31C6.23,10.03 8.92,7.35 12.19,7.35C14.07,7.35 15.52,8.12 16.5,8.97L18.4,7.07C16.94,5.71 14.75,4.62 12.19,4.62C7.39,4.62 3.5,8.51 3.5,13.31C3.5,18.11 7.39,22 12.19,22C16.99,22 21.35,18.5 21.35,13.31C21.35,12.45 21.27,11.72 21.35,11.1Z" fill="currentColor"></path>
                        </svg>
                        Continue with Google
                    </button>
                    <div className="relative flex py-3 items-center">
                        <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                        <span className="flex-shrink mx-4 text-xs font-semibold text-slate-400 uppercase tracking-widest">OR</span>
                        <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                    </div>
                    <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
                        <div>
                            <label className="block text-sm font-semibold mb-2 text-slate-700 dark:text-slate-300" htmlFor="email">Email Address</label>
                            <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="email" placeholder="name@company.com" type="email" />
                        </div>
                        <div>
                            <div className="flex justify-between mb-2">
                                <label className="text-sm font-semibold text-slate-700 dark:text-slate-300" htmlFor="password">Password</label>
                                <a className="text-xs font-bold text-primary hover:underline" href="#">Forgot password?</a>
                            </div>
                            <div className="relative">
                                <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="password" placeholder="••••••••" type="password" />
                                <button className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200" type="button">
                                    <span className="material-symbols-outlined text-xl">visibility</span>
                                </button>
                            </div>
                        </div>
                        <button className="w-full h-12 bg-primary hover:bg-primary/90 text-white rounded-lg font-bold text-lg transition-all shadow-xl shadow-primary/10 mt-2" type="submit">
                            Sign In
                        </button>
                    </form>
                </div>
                <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 text-center">
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                        Don't have an account?
                        <a className="text-primary font-bold hover:underline ml-1" href="#">Sign up for free</a>
                    </p>
                </div>
            </div>
        </div>
    );
}