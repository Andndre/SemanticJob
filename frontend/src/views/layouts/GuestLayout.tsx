import { PageLoadingSpinner } from "@/components/custom/LoadingSpinner";
import { useAuth } from "@/context/AuthContext";
import { LokerAPIProvider } from "@/context/LokerAPIContext";
import { Outlet, useNavigate } from "react-router-dom";

export default function GuestLayout() {
	const { loading, user } = useAuth();
	const navigate = useNavigate();

	if (loading) {
		return <PageLoadingSpinner/>;
	}

	if (!user) {
		navigate('/auth/login', { replace: true });
		return null;
	}

	return (
		<LokerAPIProvider>
			<Outlet	/>
		</LokerAPIProvider>
	);
}
