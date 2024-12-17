import { z } from "zod";

const formSchema = z.object({
  username: z
    .string()
    .min(2, { message: "Username must be at least 2 characters long" })
    .max(50, { message: "Username must be at most 50 characters long" })
    .regex(/^\S*$/, { message: "Username must not contain spaces" }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .max(50, { message: "Password must be at most 50 characters long" }),
});

export { formSchema };
export type FormValues = z.infer<typeof formSchema>;
