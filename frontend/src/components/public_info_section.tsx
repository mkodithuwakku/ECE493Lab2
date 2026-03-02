import React from "react";
import { PublicInfoPayload, PublicItem } from "../services/public_info_types";

interface PublicInfoSectionProps {
  data: PublicInfoPayload;
}

function renderItems(items: PublicItem[], emptyLabel: string) {
  if (items.length === 0) {
    return <p>{emptyLabel}</p>;
  }

  return (
    <ul>
      {items.map((item, index) => (
        <li key={`${item.content}-${index}`}>{item.content}</li>
      ))}
    </ul>
  );
}

export function PublicInfoSection({ data }: PublicInfoSectionProps) {
  const warning = data.status === "partial" ? data.warning : undefined;
  const message = data.status === "ok" ? data.message : undefined;

  return (
    <section>
      <h2>Public Announcements</h2>
      {renderItems(data.announcements, "No public announcements available.")}

      <h2>Conference Information</h2>
      {renderItems(data.information, "No public conference information available.")}

      {message && <p>{message}</p>}
      {warning && <p>{warning}</p>}
    </section>
  );
}
