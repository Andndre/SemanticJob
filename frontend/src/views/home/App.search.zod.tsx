import { z } from "zod";

const formSchema = z.object({
	query: z
		.string()
		.min(1),
	type: z.enum(["scraping", "graphdb"]),
});

export { formSchema };
export type FormValues = z.infer<typeof formSchema>;
