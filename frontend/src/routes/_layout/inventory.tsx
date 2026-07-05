import { createFileRoute } from "@tanstack/react-router"
import { PackageCheck, Pill, Truck } from "lucide-react"

import { inventory, recommendations } from "@/components/HealSync/data"
import { StatusBadge } from "@/components/HealSync/status"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export const Route = createFileRoute("/_layout/inventory")({
  component: InventoryPage,
  head: () => ({
    meta: [{ title: "Inventory | HealSync AI" }],
  }),
})

function InventoryPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge>Medicine supply chain</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">
          Inventory
        </h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Track current stock, predicted days of cover, and redistribution
          actions across PHCs and CHCs.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Pill className="h-4 w-4 text-primary" />
              At-risk SKUs
            </CardTitle>
          </CardHeader>
          <CardContent className="text-3xl font-semibold">7</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Truck className="h-4 w-4 text-primary" />
              Transfers pending
            </CardTitle>
          </CardHeader>
          <CardContent className="text-3xl font-semibold">3</CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <PackageCheck className="h-4 w-4 text-primary" />
              Expiring soon
            </CardTitle>
          </CardHeader>
          <CardContent className="text-3xl font-semibold">12</CardContent>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Stock Watchlist</CardTitle>
          <CardDescription>
            Forecast-driven list of medicines and diagnostic supplies
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {inventory.map((item) => (
            <div
              key={item.item}
              className="grid gap-3 rounded-lg border p-4 md:grid-cols-[1.2fr_0.8fr_0.5fr_0.5fr]"
            >
              <div>
                <p className="font-medium">{item.item}</p>
                <p className="text-sm text-muted-foreground">{item.group}</p>
              </div>
              <p className="text-sm text-muted-foreground">{item.hospital}</p>
              <p className="text-sm">{item.daysLeft} days</p>
              <StatusBadge value={item.risk} />
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Redistribution Recommendations</CardTitle>
          <CardDescription>
            Suggested transfers based on stock, demand forecast, and distance
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {recommendations.map((recommendation) => {
            const Icon = recommendation.icon
            return (
              <div
                key={recommendation.action}
                className="rounded-lg border p-4"
              >
                <div className="flex gap-3">
                  <Icon className="mt-1 h-4 w-4 text-primary" />
                  <div>
                    <p className="font-medium">{recommendation.action}</p>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {recommendation.from} to {recommendation.to}.{" "}
                      {recommendation.reason}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </CardContent>
      </Card>
    </div>
  )
}
