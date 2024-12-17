import { Job } from "@/types";
import axios from "axios";
import { createContext, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";

interface LokerAPIContextType {
  jobs: Job[];
  loading: boolean;
  fetchJobs: (query: string) => Promise<void>;
  filterLocation: { [key: string]: boolean };
  filterSource: { [key: string]: boolean };
  toggleLocationFilter: (location: string) => void;
  toggleSourceFilter: (source: string) => void;
  toggleAllLocationFilters: (checked: boolean) => void;
  toggleAllSourceFilters: (checked: boolean) => void;
  minSalary: number;
  maxSalary: number;
  selectedSalary: number[];
  setSelectedSalary: React.Dispatch<React.SetStateAction<number[]>>;
  searched: boolean;
}

const LokerAPIContext = createContext<LokerAPIContextType | undefined>(
  undefined
);

export default LokerAPIContext;

export const LokerAPIProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [minSalary, setMinSalary] = useState(0);
  const [maxSalary, setMaxSalary] = useState(0);
  const [selectedSalary, setSelectedSalary] = useState([0, 0]);
  const [filterLocation, setFilterLocation] = useState<{
    [key: string]: boolean;
  }>({});
  const [filterSource, setFilterSource] = useState<{ [key: string]: boolean }>(
    {}
  );

  const navigate = useNavigate();
  async function fetchJobs(query: string) {
    setSearched(false);
    setFilterSource({});
    setFilterLocation({});
    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:5000/api/search",
        { query },
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      );
      const data = response.data as Job[];

      console.log({data});
      // Filter out jobs with salary "Secret" and set minSalary and maxSalary
      const salaries = data
        .filter((job) => job.salary !== "Secret")
        .map((job) => job.salary);

      let min = Infinity;
      let max = -Infinity;
      salaries.forEach((salary) => {
        const parts = salary.replace("–", "-").split("-").map((part) => {
          console.log(part);
          return parseInt(part.replace("Rp", "").replace(/\s/g, "").replace(/\./g, ""), 10)
        });
        min = Math.min(min, ...parts);
        max = Math.max(max, ...parts);
      });

      console.log(min, max);

      setMinSalary(min);
      setMaxSalary(max);
      setSelectedSalary([min, max]);

      setJobs(data);

      // Set all filterLocation and filterSource to true
      const locations = data.reduce((acc, job) => {
        acc[job.location] = true;
        return acc;
      }, {} as { [key: string]: boolean });

      const sources = data.reduce((acc, job) => {
        acc[job.source] = true;
        return acc;
      }, {} as { [key: string]: boolean });

      setFilterLocation(locations);
      setFilterSource(sources);
      setSearched(true);

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

  const toggleLocationFilter = (location: string) => {
    setFilterLocation((prev) => ({
      ...prev,
      [location]: !prev[location],
    }));
  };

  const toggleSourceFilter = (source: string) => {
    setFilterSource((prev) => ({
      ...prev,
      [source]: !prev[source],
    }));
  };

  const toggleAllLocationFilters = (checked: boolean) => {
    setFilterLocation((prev) => {
      const newFilters = { ...prev };
      Object.keys(newFilters).forEach((key) => {
        newFilters[key] = checked;
      });
      return newFilters;
    });
  };

  const toggleAllSourceFilters = (checked: boolean) => {
    setFilterSource((prev) => {
      const newFilters = { ...prev };
      Object.keys(newFilters).forEach((key) => {
        newFilters[key] = checked;
      });
      return newFilters;
    });
  };

  return (
    <LokerAPIContext.Provider
      value={{
        jobs,
        loading,
        fetchJobs,
        filterLocation,
        filterSource,
        toggleLocationFilter,
        toggleSourceFilter,
        toggleAllLocationFilters,
        toggleAllSourceFilters,
        searched,
        minSalary,
        maxSalary,
        selectedSalary,
        setSelectedSalary,
      }}
    >
      {children}
    </LokerAPIContext.Provider>
  );
};

export const useLokerAPI = () => {
  const context = useContext(LokerAPIContext);
  if (!context) {
    throw new Error("useLokerAPI must be used within a LokerAPIProvider");
  }
  return context;
};
