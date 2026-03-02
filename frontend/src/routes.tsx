import React from "react";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/register";
import { Homepage } from "./pages/homepage";
import { PricingPage } from "./pages/pricing";
import { MetadataPage } from "./pages/MetadataPage";

export const routes = [
  { path: "/", component: Homepage },
  { path: "/pricing", component: PricingPage },
  { path: "/register", component: RegisterPage },
  { path: "/login", component: LoginPage },
  { path: "/submission/metadata", component: MetadataPage },
  { path: "/home", component: Homepage },
];
