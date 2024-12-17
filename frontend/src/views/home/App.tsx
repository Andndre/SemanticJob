import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/context/AuthContext";
import { Search, MapPin, DollarSign, SearchIcon } from "lucide-react";
import { useForm } from "react-hook-form";
import { formSchema, FormValues } from "./App.search.zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { useLokerAPI } from "@/context/LokerAPIContext";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { LoadingSpinner } from "@/components/custom/LoadingSpinner";
import vintage from "@/images/undraw_vintage.svg";
import notfound from "@/images/undraw_page_not_found.svg";
import { Checkbox } from "@/components/ui/checkbox";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { DualRangeSlider } from "@/components/ui/dual-range-slider";
import { convertToRupiah } from "@/lib/utils";

function App() {
  const auth = useAuth();

  return (
    <>
      <main className="flex-1">
        <nav className="p-4 flex justify-end items-center w-full border-b border-b-gray-700">
          <p>
            Anda login sebagai{" "}
            <strong className="font-bold">{auth.user}</strong>
          </p>
        </nav>
        <div className="p-4 text-center pt-28 w-full max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold">
            Sistem Pencarian Lowongan Pekerjaan
          </h1>
          <div className="pt-9"></div>
          <FormSearch />
        </div>
        <div className="p-4 text-center pt-8 w-full max-w-6xl mx-auto">
          <LokerList />
        </div>
      </main>
    </>
  );
}

function FormSearch() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  });
  const lokerAPI = useLokerAPI();

  async function onSubmit(values: FormValues) {
    console.log(values);
    await lokerAPI.fetchJobs(values.query);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex gap-3">
        <FormField
          name="query"
          control={form.control}
          render={({ field }) => (
            <FormItem className="flex-1 w-full">
              <FormControl>
                <Input
                  className="bg-gray-100"
                  placeholder="Search Job"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">
          <Search />
          <span className="sr-only">Search</span>
        </Button>
      </form>
    </Form>
  );
}

function LokerList() {
  const {
    filterLocation,
    loading,
    filterSource,
    jobs,
    toggleLocationFilter,
    toggleSourceFilter,
    toggleAllLocationFilters,
    toggleAllSourceFilters,
    searched,
    minSalary,
    maxSalary,
    selectedSalary,
    setSelectedSalary,
  } = useLokerAPI();
  const [allLocationsChecked, setAllLocationsChecked] = useState(true);
  const [allSourcesChecked, setAllSourcesChecked] = useState(true);
  const [includeSecretSalary, setIncludeSecretSalary] = useState(true);

  const handleLocationChange = (location: string) => {
    toggleLocationFilter(location);
  };

  const handleSourceChange = (source: string) => {
    toggleSourceFilter(source);
  };

  const handleAllLocationsChange = () => {
    setAllLocationsChecked(!allLocationsChecked);
    toggleAllLocationFilters(!allLocationsChecked);
  };

  const handleAllSourcesChange = () => {
    setAllSourcesChecked(!allSourcesChecked);
    toggleAllSourceFilters(!allSourcesChecked);
  };

  const handleIncludeSecretSalaryChange = () => {
    setIncludeSecretSalary(!includeSecretSalary);
  };

  if (loading) {
    return (
      <div className="flex justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  const isEmpty = jobs.every(
    (job) => !filterLocation[job.location] || !filterSource[job.source]
  );

  if (isEmpty && !searched) {
    return (
      <div className="text-center max-w-4xl mx-auto">
        <img src={vintage} alt="No data" className="w-1/2 mx-auto" />
        <p className="text-gray-500 mt-4">
          Tidak ada data yang ditemukan, silahkan cari lowongan pekerjaan yang
          lain.
        </p>
      </div>
    );
  }

  console.log(isEmpty)
  if (!isEmpty) {
    console.log(jobs)
  }

  return (
    <div className="flex flex-col md:flex-row gap-3 w-full text-start">
      <div className="flex flex-col gap-3 md:w-1/4 w-full">
        <h2 className="text-lg font-bold">Filter</h2>
        <Card>
          <CardContent className="pt-6">
            <h3 className="font-bold">Location</h3>
            <div className="flex items-center">
              <Checkbox
                checked={allLocationsChecked}
                onCheckedChange={handleAllLocationsChange}
              />
              <label className="ml-2">All Locations</label>
            </div>
            {Object.keys(filterLocation).map((location) => (
              <div key={location} className="flex items-center">
                <Checkbox
                  checked={filterLocation[location]}
                  onCheckedChange={() => handleLocationChange(location)}
                />
                <label className="ml-2">{location}</label>
              </div>
            ))}
            <h3 className="font-bold mt-4">Source</h3>
            <div className="flex items-center">
              <Checkbox
                checked={allSourcesChecked}
                onCheckedChange={handleAllSourcesChange}
              />
              <label className="ml-2">All Sources</label>
            </div>
            {Object.keys(filterSource).map((source) => (
              <div key={source} className="flex items-center">
                <Checkbox
                  checked={filterSource[source]}
                  onCheckedChange={() => handleSourceChange(source)}
                />
                <label className="ml-2">{source}</label>
              </div>
            ))}
            {
              !isEmpty && (
                <>
                  <h3 className="font-bold mt-4">Salary</h3>
                  <DualRangeSlider
                    className="mt-8"
                    label={(value) => `${(value || 0) / 1000000}Jt`}
                    min={minSalary}
                    max={maxSalary}
                    value={selectedSalary}
                    onValueChange={setSelectedSalary}
                    step={100000}
                  />
                  <div className="flex items-center mt-4">
                    <Checkbox
                      checked={includeSecretSalary}
                      onCheckedChange={handleIncludeSecretSalaryChange}
                    />
                    <label className="ml-2">Include Secret Salary</label>
                  </div>
                </>
              )
            }
          </CardContent>
        </Card>
      </div>
      <div className="flex flex-col gap-3 w-full flex-1">
        <h2 className="text-lg font-bold">Hasil Pencarian</h2>
        {isEmpty && (
          <div>
            <img src={notfound} alt="No data" className="w-1/2 mx-auto" />
          </div>
        )}
        {jobs.map((job, index) => {
          if (filterLocation[job.location] && filterSource[job.source]) {
            const parts = job.salary.split("-").map((part) => {
              return parseInt(part, 10)
            });

            const jobMinSalary = parts[0] || 0;
            const jobMaxSalary = parts[1] || jobMinSalary;

            if (
              (job.salary === "Secret" && includeSecretSalary) ||
              (jobMinSalary >= selectedSalary[0] && jobMinSalary <= selectedSalary[1]) ||
              (jobMaxSalary >= selectedSalary[0] && jobMaxSalary <= selectedSalary[1])
            ) {
              return (
                <a
                  href={job.job_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  key={"job" + index}
                >
                  <Card className="cursor-pointer hover:shadow-lg transition-shadow duration-300">
                    <CardHeader>
                      <CardTitle>{job.title}</CardTitle>
                      <CardDescription>{job.company}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center space-x-2">
                        <MapPin className="w-4 h-4 text-gray-500" />
                        <p>{job.location}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <DollarSign className="w-4 h-4 text-gray-500" />
                        {job.salary === "Secret" ? (
                          <Badge variant={"destructive"}>{job.salary}</Badge>
                        ) : (
                          <p>{convertToRupiah(job.salary)}</p>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        <SearchIcon className="w-4 h-4 text-gray-500" />
                        <p>{job.source}</p>
                      </div>
                      <Button className="mt-4" variant="outline">
                        Apply Now
                      </Button>
                    </CardContent>
                  </Card>
                </a>
              );
            }
          }
          return null;
        })}
      </div>
    </div>
  );
}

export default App;
