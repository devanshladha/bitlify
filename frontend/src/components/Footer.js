export default function Footer() {
    return (
        <footer className="py-12 px-6 lg:px-20 border-t border-white/5 border-t border-white/5 bg-background-dark">
            <div className="editorial-container">
                <div className="flex flex-col md:flex-row justify-between items-start gap-12">
                    <div className="max-w-xs">
                        <h2 className="text-white text-3xl font-extrabold mb-6">Bitlify</h2>
                        <p className="text-slate-500 text-sm ">
                            The premium destination for those who understand that every link is a part of their legacy.
                        </p>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-16">
                        <div>
                            <h4 className="text-white text-[10px] uppercase tracking-[0.3em] font-bold mb-6">Explore</h4>
                            <ul className="space-y-3 text-slate-500 text-xs uppercase tracking-widest">
                                <li><a className="hover:text-primary transition-colors" href="#">Manifesto</a></li>
                                <li><a className="hover:text-primary transition-colors" href="#">The Lab</a></li>
                                <li><a className="hover:text-primary transition-colors" href="#">Library</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="text-white text-[10px] uppercase tracking-[0.3em] font-bold mb-6">Connect</h4>
                            <ul className="space-y-3 text-slate-500 text-xs uppercase tracking-widest">
                                <li><a className="hover:text-primary transition-colors" href="#">Twitter</a></li>
                                <li><a className="hover:text-primary transition-colors" href="#">Instagram</a></li>
                                <li><a className="hover:text-primary transition-colors" href="#">Github</a></li>
                            </ul>
                        </div>
                        <div className="col-span-2 md:col-span-1">
                            <h4 className="text-white text-[10px] uppercase tracking-[0.3em] font-bold mb-6">Legal</h4>
                            <ul className="space-y-3 text-slate-500 text-xs uppercase tracking-widest">
                                <li><a className="hover:text-primary transition-colors" href="#">Privacy</a></li>
                                <li><a className="hover:text-primary transition-colors" href="#">Terms</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div className="mt-24 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p className="text-slate-600 text-[10px] uppercase tracking-widest">© 2024 Bitlify Inc. — All Rights Reserved.</p>
                    <div className="flex gap-6">
                        <span className="text-slate-700 text-[10px] uppercase tracking-[0.4em]">Designed for Creators</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}