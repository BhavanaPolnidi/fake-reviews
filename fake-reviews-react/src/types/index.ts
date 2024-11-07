import { z } from "zod";
export enum ProductCategory {
  Apparel = 0,
  Automotive = 1,
  Baby = 2,
  Beauty = 3,
  Books = 4,
  Camera = 5,
  Electronics = 6,
  Furniture = 7,
  Grocery = 8,
  "Health & Personal Care" = 9,
  Home = 10,
  "Home Entertainment" = 11,
  "Home Improvement" = 12,
  Jewelry = 13,
  Kitchen = 14,
  "Lawn and Garden" = 15,
  Luggage = 16,
  "Musical Instruments" = 17,
  "Office Products" = 18,
  Outdoors = 19,
  PC = 20,
  "Pet Products" = 21,
  Shoes = 22,
  Sports = 23,
  Tools = 24,
  Toys = 25,
  "Video DVD" = 26,
  "Video Games" = 27,
  Watches = 28,
  Wireless = 29,
}

export const formSchema = z.object({
  product_title: z
    .string()
    .min(1, { message: "Product title cannot be empty" }),
  review_title: z.string().min(1, { message: "review title cannot be empty" }),
  review_text: z.string().min(1, { message: "Review text cannot be empty" }),
  rating: z
    .string()
    .regex(/^[0-5]$/, { message: "Rating should be between 0 and 5" }),
  verified_purchase: z.enum(["Yes", "No"], {
    required_error: "You need to select if purchase is verified.",
  }),
  product_category: z.enum(
    [
      "Apparel",
      "Automotive",
      "Baby",
      "Beauty",
      "Books",
      "Camera",
      "Electronics",
      "Furniture",
      "Grocery",
      "Health & Personal Care",
      "Home",
      "Home Entertainment",
      "Home Improvement",
      "Jewelry",
      "Kitchen",
      "Lawn and Garden",
      "Luggage",
      "Musical Instruments",
      "Office Products",
      "Outdoors",
      "PC",
      "Pet Products",
      "Shoes",
      "Sports",
      "Tools",
      "Toys",
      "Video DVD",
      "Video Games",
      "Watches",
      "Wireless",
    ],
    { message: "Product category is required" }
  ),
});

export type ReviewPayload = {
  product_title: string;
  review_title: string;
  review_text: string;
  rating: string;
  verified_purchase: 0 | 1;
  product_category: [0 | 1];
};
