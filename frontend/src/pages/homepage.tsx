import React, { useEffect, useState } from "react";
import { PublicInfoSection } from "../components/public_info_section";
import { fetchPublicInfo } from "../services/public_info_client";
import {
  NO_PUBLIC_INFO_MESSAGE,
  RETRIEVAL_ERROR_MESSAGE,
  WEBSITE_UNAVAILABLE_MESSAGE,
} from "../services/public_info_messages";
import { ErrorResponse, PublicInfoPayload } from "../services/public_info_types";

type LoadState =
  | { status: "loading" }
  | { status: "ready"; data: PublicInfoPayload }
  | { status: "error"; message: string };

export function Homepage() {
  const [state, setState] = useState<LoadState>({ status: "loading" });

  useEffect(() => {
    let active = true;

    fetchPublicInfo()
      .then((payload) => {
        if (!active) {
          return;
        }

        if ((payload as ErrorResponse).message) {
          const message = (payload as ErrorResponse).message;
          setState({ status: "error", message });
          return;
        }

        const data = payload as PublicInfoPayload;
        setState({ status: "ready", data });
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
    return <p>Loading public conference information...</p>;
  }

  if (state.status === "error") {
    const message = state.message || WEBSITE_UNAVAILABLE_MESSAGE;
    return <p>{message}</p>;
  }

  const data = state.data;

  if (
    data.status === "ok" &&
    data.announcements.length === 0 &&
    data.information.length === 0
  ) {
    return <p>{data.message || NO_PUBLIC_INFO_MESSAGE}</p>;
  }

  return <PublicInfoSection data={data} />;
}
