import { Job } from "@/types";
import axios from "axios";
import { createContext, useContext, useState } from "react";
import { useNavigate } from 'react-router-dom';

interface LokerAPIContextType {
	jobs: Job[];
	loading: boolean;
	fetchJobs: (query: string) => Promise<void>;
}

const LokerAPIContext = createContext<LokerAPIContextType | undefined>(undefined);

export default LokerAPIContext;

export const LokerAPIProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [jobs, setJobs] = useState<Job[]>([]);
	const [loading, setLoading] = useState(false);
	const navigate = useNavigate();

	async function fetchJobs(query: string) {
		setLoading(true);
		try {
			const response = await axios.post("http://localhost:5000/api/search", { query }, {
				headers: {
					"Content-Type": "application/json",
				},
				withCredentials: true,
			});
			const data = response.data as Job[];
			setJobs(data);
		} catch (error) {
			if (axios.isAxiosError(error) && error.response?.status === 401) {
				navigate("/auth/login");
			} else {
				console.error("Failed to fetch jobs:", error);
			}
		} finally {
			setLoading(false);
		}
	}

	return <LokerAPIContext.Provider value={{ jobs, loading, fetchJobs }}>{children}</LokerAPIContext.Provider>;
}

export const useLokerAPI = () => {
	const context = useContext(LokerAPIContext);
	if (!context) {
		throw new Error("useLokerAPI must be used within a LokerAPIProvider");
	}
	return context;
}
