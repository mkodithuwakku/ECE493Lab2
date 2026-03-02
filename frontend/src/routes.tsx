import React from "react";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/register";
import { Homepage } from "./pages/homepage";
import { PricingPage } from "./pages/pricing";

export const routes = [
  { path: "/", component: Homepage },
  { path: "/pricing", component: PricingPage },
  { path: "/register", component: RegisterPage },
  { path: "/login", component: LoginPage },
  { path: "/home", component: Homepage },
];
