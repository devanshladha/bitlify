import ClientWrapper from "@/components/ClientWrapper";
export default function PublicLayout({ children }) {
    return (
        <ClientWrapper>
            {children}
        </ClientWrapper>
    )
}