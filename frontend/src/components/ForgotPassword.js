"use client";

export default function ForgotPassword() {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="w-full max-w-[450px] glass backdrop-blur-3xl rounded-2xl p-8 shadow-2xl glass-border">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold mb-2 tracking-tight">Reset Password</h1>
                    <p className="text-slate-500 dark:text-slate-400 text-sm">Enter your email to receive a password reset link.</p>
                </div>
                <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
                    <div>
                        <label className="block text-sm font-semibold mb-2 text-slate-700 dark:text-slate-300" htmlFor="email">Email Address</label>
                        <input className="w-full px-4 py-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-background-dark focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all placeholder:text-slate-500" id="email" placeholder="name@company.com" type="email" />
                    </div>
                    <button className="w-full h-12 bg-primary hover:bg-primary/90 text-white rounded-lg font-bold text-lg transition-all shadow-xl shadow-primary/10" type="submit">
                        Send reset email
                    </button>
                </form>
                <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 text-center">
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                        Remembered your password?
                        <a className="text-primary font-bold hover:underline ml-1" href="/auth/signin">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
