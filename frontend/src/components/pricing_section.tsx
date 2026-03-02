import React from "react";
import { PricingPayload } from "../services/pricing_types";

interface PricingSectionProps {
  data: PricingPayload;
}

export function PricingSection({ data }: PricingSectionProps) {
  return (
    <section>
      <h2>Registration Prices</h2>
      <table>
        <thead>
          <tr>
            <th>Attendance Type</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>
          {data.prices.map((price, index) => (
            <tr key={`${price.attendance_type}-${index}`}>
              <td>{price.attendance_type}</td>
              <td>${price.amount.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {data.status === "partial" && <p>{data.warning}</p>}
    </section>
  );
}
