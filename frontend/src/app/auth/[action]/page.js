"use client";
import { useParams } from "next/navigation";
import Signin from "@/components/Signin";
import Signup from "@/components/Signup";
import ForgotPassword from "@/components/ForgotPassword";

export default function AuthPage() {
    const params = useParams();
    return (
        <div className="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden ">
            {
                /* Sign In Modal */
                params.action === "signin" && <Signin />
            }
            {
                /* Sign Up Modal */
                params.action === "signup" && <Signup />
            }
            {
                /* Forgot Password */
                params.action === "forgot" && <ForgotPassword />
            }
            {
                /* Fallback for unsupported auth action */
                !["signin", "signup", "forgot"].includes(params.action) && (
                    <div className="w-full p-8 text-center">
                        <p className="text-slate-400">Unknown auth action. Use /auth/signin, /auth/signup, or /auth/forgot.</p>
                    </div>
                )
            }
        </div>
    );
}