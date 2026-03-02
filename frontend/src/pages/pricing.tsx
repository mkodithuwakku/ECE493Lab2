import React, { useEffect, useState } from "react";
import { PricingSection } from "../components/pricing_section";
import { fetchPricing } from "../services/pricing_client";
import {
  NO_PRICING_MESSAGE,
  RETRIEVAL_ERROR_MESSAGE,
} from "../services/pricing_messages";
import { MessageResponse, PricingPayload } from "../services/pricing_types";

type LoadState =
  | { status: "loading" }
  | { status: "ready"; data: PricingPayload }
  | { status: "error"; message: string };

export function PricingPage() {
  const [state, setState] = useState<LoadState>({ status: "loading" });

  useEffect(() => {
    let active = true;

    fetchPricing()
      .then((payload) => {
        if (!active) {
          return;
        }

        if ((payload as MessageResponse).message) {
          setState({ status: "error", message: (payload as MessageResponse).message });
          return;
        }

        setState({ status: "ready", data: payload as PricingPayload });
      })
      .catch(() => {
        if (active) {
          setState({ status: "error", message: RETRIEVAL_ERROR_MESSAGE });
        }
      });

    return () => {
      active = false;
    };
  }, []);

  if (state.status === "loading") {
    return <p>Loading registration prices...</p>;
  }

  if (state.status === "error") {
    const message = state.message || NO_PRICING_MESSAGE;
    return <p>{message}</p>;
  }

  return <PricingSection data={state.data} />;
}
