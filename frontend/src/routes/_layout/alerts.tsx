import { createFileRoute } from "@tanstack/react-router"
import { AlertTriangle, BellRing } from "lucide-react"

import { alerts } from "@/components/HealSync/data"
import { StatusBadge } from "@/components/HealSync/status"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export const Route = createFileRoute("/_layout/alerts")({
  component: AlertsPage,
  head: () => ({
    meta: [{ title: "Alerts | HealSync AI" }],
  }),
})

function AlertsPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge>Prediction and threshold alerts</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">Alerts</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Prioritize medicine shortages, staffing issues, disease spikes, and
          laboratory risks before they disrupt care delivery.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {["Medicine", "Staffing", "Disease", "Equipment"].map((type) => (
          <Card key={type}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle className="text-base">{type}</CardTitle>
              <BellRing className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent className="text-3xl font-semibold">
              {alerts.filter((alert) => alert.type === type).length}
            </CardContent>
          </Card>
        ))}
      </section>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-amber-500" />
            Active Alert Queue
          </CardTitle>
          <CardDescription>
            Each alert includes the predicted issue and the operational reason
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {alerts.map((alert) => (
            <div key={alert.title} className="rounded-lg border p-4">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p className="font-medium">{alert.title}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {alert.detail}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Badge variant="outline">{alert.type}</Badge>
                  <StatusBadge value={alert.severity} />
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
