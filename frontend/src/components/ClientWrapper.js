"use client";

import { useState } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";

export default function ClientWrapper({ children }) {
    const [open, setOpen] = useState(false);

    return (
        <>
            <Navbar />
            {children}
            <Footer />
        </>
    );
}