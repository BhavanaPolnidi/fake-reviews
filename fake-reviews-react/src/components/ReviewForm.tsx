import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { BeatLoader } from "react-spinners";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "./ui/textarea";
import { ProductCategory } from "@/types";
import { formSchema } from "@/types";
import { useState } from "react";

function ReviewForm() {
  const [prediction, setPrediction] = useState<string | null>(null);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      product_title: "",
      product_category: undefined,
      review_title: "",
      review_text: "",
      rating: "",
      verified_purchase: undefined,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>): Promise<void> {
    const res = await fetch(
      `${import.meta.env.VITE_APP_FLASK_API_URL}/predict`,
      {
        method: "POST",
        body: JSON.stringify(values),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const data = await res.json();
    setPrediction(data.prediction);
  }

  return (
    <Card className="w-[50vw] mx-auto my-2">
      <CardHeader>
        <CardTitle>Review Assessment</CardTitle>
        <CardDescription>
          Know Genuinity of a review in one-click.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {form.formState.isSubmitting && (
          <BeatLoader className="m-auto w-fit" color="#0f172a" />
        )}
        {prediction && (
          <div className="p-4 bg-gray-100 rounded-md">
            <p className="text-lg font-semibold">{prediction}</p>
          </div>
        )}
        {!form.formState.isSubmitting && !prediction && (
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
              <FormField
                control={form.control}
                name="product_title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter Title Of Product" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="review_title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Review Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter Review Title" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="review_text"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Review</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Type Review Here..."
                        className="resize-none"
                        rows={4}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="rating"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Rating</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter Rating 0 to 5"
                        type="number"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="verified_purchase"
                render={({ field }) => (
                  <FormItem className="">
                    <FormLabel>Is It Verified Purchase ?</FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        className="flex space-x-3"
                      >
                        <FormItem className="flex items-center space-x-2 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="Yes" />
                          </FormControl>
                          <FormLabel className="font-normal">Yes</FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-2 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="No" />
                          </FormControl>
                          <FormLabel className="font-normal">No</FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="product_category"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Category</FormLabel>
                    <Select onValueChange={(value) => field.onChange(value)}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select Product Category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {Object.entries(ProductCategory)
                          .filter(([key]) => isNaN(Number(key))) // Filter out numeric keys
                          .map(([key, value]) => (
                            <SelectItem key={value} value={key}>
                              {key}
                            </SelectItem>
                          ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" disabled={form.formState.isSubmitting}>
                Submit
              </Button>
            </form>
          </Form>
        )}
      </CardContent>
    </Card>
  );
}

export default ReviewForm;
