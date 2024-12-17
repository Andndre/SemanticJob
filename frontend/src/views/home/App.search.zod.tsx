import { z } from "zod";

const formSchema = z.object({
	query: z
		.string()
		.min(1)
});

export { formSchema };
export type FormValues = z.infer<typeof formSchema>;
