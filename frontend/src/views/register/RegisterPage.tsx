import { toast } from "sonner"
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { useForm } from "react-hook-form";
import { FormValues, formSchema } from './RegisterPage.zod';
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { LoadingSpinner } from "@/components/custom/LoadingSpinner";

function RegisterForm() {
  const auth = useAuth();

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  });

  async function onSubmit(values: FormValues) {
    const message = await auth.register(values.username, values.password);
    if (message.success) {
      toast.success(message.message);
    } else {
      toast.error(message.message);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          name="username"
          control={form.control}
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="Username" {...field} />
              </FormControl>
              <FormDescription>
                This is your public display name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          name="password"
          control={form.control}
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type='password' placeholder="Password" {...field} />
              </FormControl>
              <FormDescription>
                This is your secret password.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button className='w-full' type="submit">
          {auth.loading ? <LoadingSpinner/> : 'Register'}
        </Button>
      </form>
    </Form>
  )
}

export default function RegisterPage() {
  return (
    <div className='flex flex-col items-center justify-center h-screen p-4'>
      <Card className = 'w-full max-w-xl'>
        <CardHeader className='text-2xl font-bold'>Register</CardHeader>
        <CardContent>
          <RegisterForm />
        </CardContent>
        <CardFooter>
            <p>Already have an account? <a className='underline' href='/auth/login'>Login here</a>.</p>
        </CardFooter>
      </Card>
    </div>
  );
}
