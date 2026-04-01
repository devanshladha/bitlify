import Link from "next/link";

export default function Navbar({ onOpen }) {
    return (
        <header className="fixed top-4 z-50 w-full flex justify-center px-4 opacity-100">
            <div className="w-full max-w-5xl border border-white/10 backdrop-blur-md px-6 lg:px-10 py-3 rounded-full shadow-lg glass">

                <div className="flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2">
                    <div className="flex items-center gap-2 group cursor-pointer">
                        <span className="material-symbols-outlined text-white text-2xl">link</span>
                        <h2 className="text-white text-xl font-extrabold tracking-tight">Bitlify</h2>
                    </div>
                    </ Link>

                    <nav className="hidden md:flex items-center gap-10">
                        <a className="text-slate-400 hover:text-white text-sm font-medium transition-colors" href="#">Features</a>
                        <a className="text-slate-400 hover:text-white text-sm font-medium transition-colors" href="#">Pricing</a>
                        <a className="text-slate-400 hover:text-white text-sm font-medium transition-colors" href="#">Analytics</a>
                        <a className="text-slate-400 hover:text-white text-sm font-medium transition-colors" href="#">API</a>
                    </nav>

                    <div className="flex items-center gap-4">
                        <a href="/auth/signin"><button className="hidden sm:block text-slate-400 hover:text-white text-sm font-semibold px-4 py-2 transition-colors">
                            Log In
                        </button></a>
                        <a href="/auth/signup"><button className="bg-primary text-white text-sm font-bold px-5 py-2.5 rounded-full glow-button transition-all">
                            Try It Free
                        </button></a>
                    </div>
                </div>
            </div>
        </header>
    );
}