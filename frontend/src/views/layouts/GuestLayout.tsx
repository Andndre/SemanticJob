import { SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

export default function GuestLayout() {
	return (
		<SidebarProvider>
			<Outlet	/>
		</SidebarProvider>
	);
}
