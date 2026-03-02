import React from "react";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/register";
import { Homepage } from "./pages/homepage";
import { PricingPage } from "./pages/pricing";
import { MetadataPage } from "./pages/MetadataPage";
import { SubmissionProgressPage } from "./pages/SubmissionProgressPage";

export const routes = [
  { path: "/", component: Homepage },
  { path: "/pricing", component: PricingPage },
  { path: "/register", component: RegisterPage },
  { path: "/login", component: LoginPage },
  { path: "/submission/metadata", component: MetadataPage },
  { path: "/submission/progress", component: SubmissionProgressPage },
  { path: "/home", component: Homepage },
];
