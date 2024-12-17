import { z } from "zod";

const formSchema = z.object({
	query: z
		.string()
		.min(1, { message: "Username must be at least 2 characters long" })
});

export { formSchema };
export type FormValues = z.infer<typeof formSchema>;
